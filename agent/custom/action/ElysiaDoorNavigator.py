from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any

from maa.context import Context
from maa.custom_action import CustomAction
from maa.define import NeuralNetworkResult

from ..utils.Logger import Logger


USABLE_GATE_LABELS = {
    "elysia_star",
    "aomie",
    "zhenwo",
    "kongmeng",
    "jielv",
    "luoxuan",
    "tianhui",
    "fanxing",
    "wuxian",
    "chana",
    "huangjin",
    "jiushi",
    "xvguang",
    "fusheng",
    "BOSS",
}

LABEL_ALIAS = {
    "鏖灭": "aomie",
    "真我": "zhenwo",
    "空梦": "kongmeng",
    "戒律": "jielv",
    "螺旋": "luoxuan",
    "天慧": "tianhui",
    "繁星": "fanxing",
    "无限": "wuxian",
    "刹那": "chana",
    "黄金": "huangjin",
    "救世": "jiushi",
    "旭光": "xvguang",
    "浮生": "fusheng",
    "爱愿妖精": "elysia_star",
    "真我·爱莉希雅": "zhenwo",
    "BOSS": "BOSS",
}

ROLE_PRIORITY_LABELS = {
    "次生银翼": ["huangjin", "kongmeng", "jiushi", "fanxing", "fusheng"],
    "镇×偃月叩晓": ["huangjin", "kongmeng", "jiushi", "fanxing", "fusheng"],
    "窈窕谍影": ["huangjin", "kongmeng", "fanxing", "jiushi", "fusheng"],
    "嗨♪爱愿妖精♪": ["huangjin", "kongmeng", "luoxuan", "fanxing", "jiushi", "chana"],
    "逆命魔龙·降临！": ["huangjin", "kongmeng", "jiushi", "fanxing", "aomie"],
    "位面武器·失序时空": ["zhenwo", "huangjin", "kongmeng", "jiushi", "fanxing", "fusheng"],
    "一客逍游": ["huangjin", "fanxing", "jiushi", "fusheng", "kongmeng"],
    "咚！炽愿吉星": ["huangjin", "kongmeng", "fanxing", "jiushi", "chana"],
    "天光驰彻": ["huangjin", "kongmeng", "fanxing", "jiushi", "fusheng"],
    "诡戏千役[友情出演！]": ["huangjin", "kongmeng", "aomie", "fanxing", "jiushi"],
    "孑遗千星": ["huangjin", "kongmeng", "jiushi", "fanxing", "fusheng"],
    "天命难逃": ["huangjin", "jiushi", "fanxing", "kongmeng", "fusheng"],
    "瞒天乐游·曙影": ["huangjin", "kongmeng", "fanxing", "jiushi", "fusheng"],
    "破弃弧光·逐影": ["huangjin", "aomie", "jiushi", "fanxing", "kongmeng"],
    "破弃孤光·逐影": ["huangjin", "aomie", "jiushi", "fanxing", "kongmeng"],
    "享乐狂宴·邀影": ["huangjin", "kongmeng", "fanxing", "jiushi", "fusheng"],
    "深空定锚·曙光": ["huangjin", "kongmeng", "jiushi", "fanxing", "fusheng"],
    "浮生·渡尘之羽": ["aomie", "jiushi", "huangjin", "fanxing", "fusheng"],
    "月下誓约·予爱以心": ["huangjin", "jiushi", "fanxing", "kongmeng", "fusheng"],
}


@dataclass(frozen=True)
class GateTarget:
    label: str
    center_x: int
    center_y: int
    score: float


class ElysiaDoorNavigator(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        self.context = context
        self.logger = Logger("ElysiaDoorNavigator", context)
        self.params = self._parse_params(getattr(argv, "custom_action_param", None))
        self.mode = str(self.params.get("mode", "smart")).strip().lower() or "smart"
        self.role = str(self.params.get("role", "天命难逃")).strip() or "天命难逃"
        self.preferred_labels = self._resolve_preferred_labels(
            self.params.get("preferred_labels"),
            self.role,
        )

        self.logger.ui(
            f"乐土选门：开始导航（模式={self.mode}，角色={self.role}）",
            "cyan",
        )

        try:
            interacted = self._navigate_to_gate()
            if interacted:
                self.logger.ui("乐土选门：已完成交互，等待进入下一层或战斗。", "green")
            else:
                self.logger.ui("乐土选门：本轮未稳定完成交互，回退到旧寻路链兜底。", "orange")
            return CustomAction.RunResult(success=True)
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

    def _resolve_preferred_labels(self, raw_labels: Any, role: str) -> list[str]:
        labels: list[str] = []
        if isinstance(raw_labels, list):
            labels = [LABEL_ALIAS.get(str(item), str(item)) for item in raw_labels if item]
        elif isinstance(raw_labels, str) and raw_labels:
            labels = [LABEL_ALIAS.get(raw_labels, raw_labels)]

        if labels:
            return labels
        return ROLE_PRIORITY_LABELS.get(role, ["huangjin", "jiushi", "fanxing", "kongmeng", "fusheng"])

    def _navigate_to_gate(self) -> bool:
        if self._try_interact():
            return True

        last_targets: list[GateTarget] = []
        for attempt in range(8):
            targets = self._detect_targets()
            if targets:
                last_targets = targets
                chosen = self._choose_target(targets)
                self.logger.ui(
                    f"乐土选门：识别到 {len(targets)} 扇门，目标={chosen.label}，x={chosen.center_x}",
                    "cyan",
                )
                self._adjust_camera(chosen.center_x)
                if self._approach_target(chosen):
                    return True
            else:
                self.logger.ui(f"乐土选门：第 {attempt + 1} 次未识别到可用门，继续转视角。", "orange")

            self._scan_rotate(attempt)

        if last_targets and self.mode == "random":
            fallback = max(last_targets, key=lambda item: item.center_x)
            self.logger.ui(
                f"乐土选门：回退到最右门 {fallback.label}，执行最后一次靠近尝试。",
                "orange",
            )
            return self._approach_target(fallback)

        return False

    def _detect_targets(self) -> list[GateTarget]:
        image = self.context.tasker.controller.post_screencap().wait().get()
        detail = self.context.run_recognition("往世乐土_识别门", image)
        if not detail or not detail.hit:
            return []

        targets: list[GateTarget] = []
        for result in detail.all_results or []:
            if not isinstance(result, NeuralNetworkResult):
                continue
            if result.label not in USABLE_GATE_LABELS:
                continue
            if result.score < 0.45 or result.box is None:
                continue
            center_x = int(result.box.x + result.box.width / 2)
            center_y = int(result.box.y + result.box.height / 2)
            targets.append(
                GateTarget(
                    label=result.label,
                    center_x=center_x,
                    center_y=center_y,
                    score=float(result.score),
                )
            )

        targets.sort(key=lambda item: item.center_x)
        return targets

    def _choose_target(self, targets: list[GateTarget]) -> GateTarget:
        if self.mode == "random":
            return max(targets, key=lambda item: item.center_x)

        for preferred in self.preferred_labels:
            for target in targets:
                if target.label == preferred:
                    return target

        return max(targets, key=lambda item: item.center_x)

    def _adjust_camera(self, target_center_x: int) -> None:
        screen_center = 640
        delta = target_center_x - screen_center
        if abs(delta) < 120:
            return

        # Win32 下 swipe 会模拟拖拽，向右目标更偏右时适度拖拽镜头。
        start_x = 940 if delta > 0 else 340
        end_x = 690 if delta > 0 else 590
        self.context.tasker.controller.post_swipe(start_x, 360, end_x, 360, 260).wait()
        time.sleep(0.45)

    def _approach_target(self, target: GateTarget) -> bool:
        for step in range(8):
            if self._try_interact():
                return True

            offset = target.center_x - 640
            if offset < -180:
                self._hold_key(65, 220)  # A
            elif offset > 180:
                self._hold_key(68, 220)  # D

            forward_ms = 850 if step < 2 else 650
            self._hold_key(87, forward_ms)  # W
            time.sleep(0.25)

            if self._try_interact():
                return True

            refreshed = self._detect_targets()
            if refreshed:
                target = self._choose_target(refreshed)

        return False

    def _try_interact(self) -> bool:
        image = self.context.tasker.controller.post_screencap().wait().get()
        detail = self.context.run_recognition(
            "乐土刷级-减负模式-伪寻路-到达目的",
            image,
            {
                "乐土刷级-减负模式-伪寻路-到达目的": {
                    "expected": [
                        "前往",
                        "启动传送锚点",
                        "启动传送",
                        "传送锚点",
                    ]
                }
            },
        )
        if detail and detail.hit:
            self.context.tasker.controller.post_click_key(82).wait()
            time.sleep(1.2)
            return True
        return False

    def _scan_rotate(self, attempt: int) -> None:
        if attempt % 2 == 0:
            self.context.tasker.controller.post_swipe(1080, 360, 240, 360, 650).wait()
        else:
            self.context.tasker.controller.post_swipe(240, 360, 1080, 360, 650).wait()
        time.sleep(0.6)

    def _hold_key(self, key: int, duration_ms: int) -> None:
        self.context.tasker.controller.post_key_down(key).wait()
        time.sleep(max(duration_ms, 50) / 1000)
        self.context.tasker.controller.post_key_up(key).wait()
