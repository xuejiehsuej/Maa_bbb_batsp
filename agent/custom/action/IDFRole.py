from maa.context import Context
from maa.custom_action import CustomAction
import json
import os
from ..utils.Logger import Logger

from ..utils.RoleConfiguration import ROLE_CONFIG

"""
在战斗中识别角色
v1.0.0
作者 overflow
"""


class RecognitionRole(CustomAction):
    def _attack_template(self, role_name: str, role_info: dict) -> str | None:
        attack_template = role_info.get("attack_template")
        if attack_template:
            return attack_template
        default_template = f"自动战斗索引/{role_name}.png"
        default_path = os.path.join("resource", "base", "image", default_template)
        if os.path.exists(default_path):
            return default_template
        return None

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        image = context.tasker.controller.post_screencap().wait().get()
        print(f"识别角色 ")

        for role_name, role_info in ROLE_CONFIG.items():
            attack_template = self._attack_template(role_name, role_info)
            if not attack_template:
                print(f"识别角色 {role_name} 跳过，缺少战斗中按钮模板")
                continue
            print(f"识别角色 {role_name}")
            result = context.run_recognition(
                entry="在战斗中检查角色",
                image=image,
                pipeline_override={
                    "在战斗中检查角色": {
                        "recognition": {
                            "param": {
                                "template": attack_template,
                                "threshold": 0.8,
                            },
                        }
                    }
                },
            )
            context.run_action("攻击_action")  # 攻击一下,防止发呆
            if result and result.hit:
                context.override_pipeline(
                    {
                        "识别人物": {"enabled": False},
                        "战斗程序": {
                            "action": "Custom",
                            "custom_action": role_info["cls_name"],
                            "custom_action_param": {"role": role_name},
                        },
                    }
                )
                print(f"识别角色 {role_name} 成功")
                return CustomAction.RunResult(success=True)
        context.override_pipeline(
            {
                "识别人物": {"enabled": False},
                "战斗程序": {
                    "action": "Custom",
                    "custom_action": "AstralRingFight",
                    "custom_action_param": {"role": "星环通用"},
                },
            }
        )
        print(f"识别角色 失败,使用星环通用逻辑")

        return CustomAction.RunResult(success=True)
