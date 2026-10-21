from __future__ import annotations

import time

from maa.context import Context
from maa.custom_action import CustomAction

from ..utils.Logger import Logger


class ElysiaWeeklyReductionSetup(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        self.context = context
        self.logger = Logger("ElysiaWeeklyReductionSetup", context)

        try:
            if not (self._is_buff_page() or self._is_role_page()):
                return CustomAction.RunResult(success=False)

            if self._is_buff_page():
                self.logger.ui("乐土减负：已进入减负准备页，开始检查挑战难度。", "cyan")
                self._ensure_difficulty()
                self.logger.ui("乐土减负：挑战难度检查完成，准备进入女武神选择界面。", "cyan")
                self.context.run_task("乐土刷级-减负模式-点击进入女武神选择界面")
                time.sleep(1.0)

            if not self._is_role_page():
                return CustomAction.RunResult(success=False)

            self.logger.ui("乐土减负：已进入女武神选择界面，开始检查并切换角色。", "cyan")
            self._ensure_role()
            self.logger.ui("乐土减负：角色检查完成，准备正式进入战斗。", "green")
            self.context.run_task("乐土刷级-减负模式-点击进入战斗")
            time.sleep(0.8)
            return CustomAction.RunResult(success=True)
        finally:
            self.logger.destroy()

    def _ensure_difficulty(self) -> None:
        selected_node = self.context.get_node_data("乐土刷级-减负模式-已选中挑战难度") or {}
        if selected_node.get("enabled") is False:
            self.logger.ui("乐土减负：当前配置为沿用已解锁最高难度，本轮跳过切换。", "cyan")
            return

        if self.context.run_task("乐土刷级-减负模式-已选中挑战难度"):
            self.logger.ui("乐土减负：当前挑战难度已符合设置。", "green")
            return

        self.context.run_task("乐土刷级-减负模式-点击选择挑战难度")
        time.sleep(0.6)
        if not self.context.run_task("乐土刷级-减负模式-已选中挑战难度"):
            raise RuntimeError("乐土减负：挑战难度切换后仍未命中目标难度。")

        self.logger.ui("乐土减负：已切换到目标挑战难度。", "green")

    def _ensure_role(self) -> None:
        if self.context.run_task("乐土刷级-浅层序列-检查当前女武神是否为选中女武神"):
            self.logger.ui("乐土减负：当前女武神已符合配置。", "green")
            return

        self.context.run_task("乐土刷级-浅层序列-未选择出战女武神流程")
        time.sleep(0.5)
        self.context.run_task("乐土刷级-浅层序列-未选择出战女武神流程-确认队伍")
        time.sleep(0.8)

        if not self.context.run_task("乐土刷级-浅层序列-检查当前女武神是否为选中女武神"):
            raise RuntimeError("乐土减负：女武神检查未通过，未切换到目标角色。")

        self.logger.ui("乐土减负：已切换到目标女武神并确认队伍。", "green")

    def _is_buff_page(self) -> bool:
        text = self._ocr_join((60, 40, 1160, 660))
        return any(keyword in text for keyword in ("关卡效果", "减负战斗", "预计通关积分", "开始战斗"))

    def _is_role_page(self) -> bool:
        text = self._ocr_join((40, 90, 1240, 630))
        return any(keyword in text for keyword in ("出战位", "支援位", "开始战斗"))

    def _ocr_join(self, roi: tuple[int, int, int, int]) -> str:
        image = self.context.tasker.controller.post_screencap().wait().get()
        detail = self.context.run_recognition(
            "乐土减负前置配置-OCR",
            image,
            {
                "乐土减负前置配置-OCR": {
                    "recognition": "OCR",
                    "roi": list(roi),
                    "expected": [".+"],
                }
            },
        )
        if not detail or not detail.raw or not isinstance(detail.raw, dict):
            return ""
        return "".join(
            str(item.get("text", "")).strip()
            for item in detail.raw.get("all") or []
            if str(item.get("text", "")).strip()
        )
