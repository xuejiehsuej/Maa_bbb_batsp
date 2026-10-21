from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any

from maa.context import Context
from maa.custom_action import CustomAction

from ..utils.Logger import Logger


@dataclass(frozen=True)
class CardSlot:
    index: int
    name: str
    roi: tuple[int, int, int, int]
    click_x: int
    click_y: int


CARD_SLOTS = [
    CardSlot(0, "left", (110, 160, 290, 360), 320, 360),
    CardSlot(1, "middle", (440, 160, 290, 360), 650, 360),
    CardSlot(2, "right", (770, 160, 290, 360), 980, 360),
]

TITLE_ALIAS = {
    "刹那": "刹那",
    "鏖灭": "鏖灭",
    "空梦": "空梦",
    "黄金": "黄金",
    "救世": "救世",
    "繁星": "繁星",
    "浮生": "浮生",
    "戒律": "戒律",
    "螺旋": "螺旋",
    "天慧": "天慧",
    "无限": "无限",
    "旭光": "旭光",
    "真我": "真我",
}

DESCRIPTION_HINTS = {
    "闪避": "刹那",
    "时空": "刹那",
    "低生命": "鏖灭",
    "生命值较低": "鏖灭",
    "银币": "空梦",
    "商店": "空梦",
    "全伤害": "黄金",
    "连击": "救世",
    "武器技": "救世",
    "元素穿透": "繁星",
    "分支攻击": "浮生",
    "必杀技": "真我",
}


class ElysiaImprintSelector(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        self.context = context
        self.logger = Logger("ElysiaImprintSelector", context)
        self.params = self._parse_params(getattr(argv, "custom_action_param", None))
        self.mode = str(self.params.get("mode", "smart")).strip().lower() or "smart"
        self.role = str(self.params.get("role", "天命难逃")).strip() or "天命难逃"
        self.preferred_labels = self._normalize_labels(self.params.get("preferred_labels"))

        try:
            screen = self._detect_screen()
            if screen is None:
                return CustomAction.RunResult(success=False)

            # 初始英桀祝福继续交给原有稳定逻辑处理，新逻辑只负责“下一层传送锚点”三选一。
            if screen == "hero_blessing":
                self.logger.ui("乐土刻印卡片：检测到初始英桀祝福页，回退到原有稳定逻辑继续处理。", "cyan")
                return CustomAction.RunResult(success=False)

            cards = self._read_cards()
            if not cards:
                self.logger.ui("乐土刻印卡片：检测到传送锚点页，但本轮未稳定读到三选一卡片，回退旧逻辑兜底。", "orange")
                return CustomAction.RunResult(success=False)

            chosen = self._choose_card(cards)
            self.logger.ui(
                f"乐土刻印卡片：模式={self.mode}，角色={self.role}，选择 {chosen['slot'].name} -> {chosen['title'] or chosen['desc']}",
                "cyan",
            )

            if not self._click_card(chosen["slot"]):
                self.logger.ui("乐土刻印卡片：点击卡片未生效，回退旧逻辑兜底。", "orange")
                return CustomAction.RunResult(success=False)

            self._confirm_selection_if_needed()
            if self._detect_screen() is None:
                self.logger.ui("乐土刻印卡片：已完成本轮传送锚点选择。", "green")
                return CustomAction.RunResult(success=True)

            self.logger.ui("乐土刻印卡片：页面仍停留在卡片页，回退旧逻辑继续兜底。", "orange")
            return CustomAction.RunResult(success=False)
        finally:
            self.logger.destroy()

    def _parse_params(self, raw: Any) -> dict[str, Any]:
        if isinstance(raw, dict):
            return raw
        if not raw:
            return {}
        if isinstance(raw, str):
            try:
                data = json.loads(raw)
                return data if isinstance(data, dict) else {}
            except json.JSONDecodeError:
                return {}
        return {}

    def _normalize_labels(self, raw_labels: Any) -> list[str]:
        if isinstance(raw_labels, list):
            return [self._normalize_text(str(item)) for item in raw_labels if item]
        if isinstance(raw_labels, str) and raw_labels:
            return [self._normalize_text(raw_labels)]
        return []

    def _detect_screen(self) -> str | None:
        text = self._ocr_join((360, 60, 600, 190))
        normalized = self._normalize_text(text)
        if "请选择下一层传送锚点" in normalized:
            return "teleport_anchor"
        if "请选择英桀的刻印" in normalized:
            return "hero_blessing"
        return None

    def _read_cards(self) -> list[dict[str, Any]]:
        cards: list[dict[str, Any]] = []
        for slot in CARD_SLOTS:
            content = self._ocr_join(slot.roi)
            normalized = self._normalize_text(content)
            if not normalized:
                continue
            label = self._resolve_label(normalized)
            cards.append(
                {
                    "slot": slot,
                    "title": content.splitlines()[0] if content else "",
                    "desc": content,
                    "normalized": normalized,
                    "label": label,
                }
            )
        return cards

    def _resolve_label(self, text: str) -> str:
        for alias, label in TITLE_ALIAS.items():
            if self._normalize_text(alias) in text:
                return label
        for hint, label in DESCRIPTION_HINTS.items():
            if self._normalize_text(hint) in text:
                return label
        return ""

    def _choose_card(self, cards: list[dict[str, Any]]) -> dict[str, Any]:
        if self.mode == "random":
            return max(cards, key=lambda item: item["slot"].index)

        for preferred in self.preferred_labels:
            for card in cards:
                if card["label"] and self._normalize_text(card["label"]) == preferred:
                    return card
                if preferred and preferred in card["normalized"]:
                    return card

        return max(cards, key=lambda item: item["slot"].index)

    def _click_card(self, slot: CardSlot) -> bool:
        self.context.tasker.controller.post_click(slot.click_x, slot.click_y).wait()
        time.sleep(0.6)
        return True

    def _confirm_selection_if_needed(self) -> None:
        confirm = self._find_text_in_roi((950, 600, 300, 100), ["选择刻印", "前往", "启动传送锚点"])
        if confirm is None:
            return
        x, y, w, h = confirm["box"]
        self.context.tasker.controller.post_click(x + w // 2, y + h // 2).wait()
        time.sleep(0.8)

    def _find_text_in_roi(self, roi: tuple[int, int, int, int], patterns: list[str]) -> dict[str, Any] | None:
        image = self.context.tasker.controller.post_screencap().wait().get()
        detail = self.context.run_recognition(
            "乐土刻印卡片-OCR-匹配",
            image,
            {
                "乐土刻印卡片-OCR-匹配": {
                    "recognition": "OCR",
                    "roi": list(roi),
                    "expected": [".+"],
                }
            },
        )
        if not detail or not detail.raw or not isinstance(detail.raw, dict):
            return None

        for item in detail.raw.get("all") or []:
            text = self._normalize_text(str(item.get("text", "")))
            if not text:
                continue
            if any(self._normalize_text(pattern) in text for pattern in patterns):
                return {"text": text, "box": item.get("box", [0, 0, 0, 0])}
        return None

    def _ocr_join(self, roi: tuple[int, int, int, int]) -> str:
        image = self.context.tasker.controller.post_screencap().wait().get()
        detail = self.context.run_recognition(
            "乐土刻印卡片-OCR",
            image,
            {
                "乐土刻印卡片-OCR": {
                    "recognition": "OCR",
                    "roi": list(roi),
                    "expected": [".+"],
                }
            },
        )
        if not detail or not detail.raw or not isinstance(detail.raw, dict):
            return ""
        texts = [str(item.get("text", "")).strip() for item in detail.raw.get("all") or [] if str(item.get("text", "")).strip()]
        return "\n".join(texts)

    @staticmethod
    def _normalize_text(text: str) -> str:
        return (
            text.replace(" ", "")
            .replace("\r", "")
            .replace("\n", "")
            .replace("[", "")
            .replace("]", "")
            .replace("「", "")
            .replace("」", "")
            .replace("·", "")
            .strip()
        )
