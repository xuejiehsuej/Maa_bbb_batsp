"""
Second-part Astral Ring battle logic.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any

from maa.context import Context
from maa.custom_action import CustomAction

from ...utils.BattleCore import CombatActions


@dataclass(frozen=True)
class AstralRingProfile:
    ring: str
    opener: tuple[str, ...]
    builder: tuple[str, ...]
    burst: tuple[str, ...]
    switch_after: bool = True


ROLE_PROFILES: dict[str, AstralRingProfile] = {
    "星环通用": AstralRingProfile(
        ring="通用",
        opener=("lock", "qte1", "qte2", "skill"),
        builder=("attack", "attack", "branch", "skill"),
        burst=("star_ring", "ultimate", "attack", "attack", "branch"),
    ),
    "深空定锚·曙光": AstralRingProfile(
        ring="世界之星",
        opener=("lock", "qte1", "qte2", "skill"),
        builder=("attack", "attack", "branch", "skill"),
        burst=("star_ring", "ultimate", "attack", "attack", "branch"),
    ),
    "女武神·巡矢": AstralRingProfile(
        ring="世界之星",
        opener=("qte1", "skill"),
        builder=("attack", "attack", "skill", "branch"),
        burst=("star_ring", "qte2", "ultimate", "attack", "skill"),
    ),
    "女武神·重击": AstralRingProfile(
        ring="世界之星",
        opener=("qte2", "skill"),
        builder=("attack", "branch", "attack", "skill"),
        burst=("star_ring", "ultimate", "attack", "branch"),
    ),
    "享乐狂宴·邀影": AstralRingProfile(
        ring="命运之轮",
        opener=("lock", "skill", "attack"),
        builder=("attack", "branch", "skill", "attack"),
        burst=("star_ring", "ultimate", "branch", "attack", "skill"),
    ),
    "破弃弧光·逐影": AstralRingProfile(
        ring="命运之轮",
        opener=("qte1", "skill", "attack"),
        builder=("branch", "attack", "skill", "attack"),
        burst=("star_ring", "ultimate", "skill", "branch", "attack"),
    ),
    "瞒天乐游·曙影": AstralRingProfile(
        ring="天衍之杯",
        opener=("qte1", "qte2", "skill"),
        builder=("attack", "branch", "skill", "attack"),
        burst=("star_ring", "ultimate", "branch", "skill", "attack"),
    ),
    "孑遗千星": AstralRingProfile(
        ring="无存之仪",
        opener=("lock", "skill", "attack"),
        builder=("attack", "branch", "skill", "attack"),
        burst=("star_ring", "ultimate", "skill", "branch", "attack"),
    ),
    "诡戏千役[友情出演！]": AstralRingProfile(
        ring="命运之轮",
        opener=("qte1", "skill", "attack"),
        builder=("attack", "branch", "skill", "attack"),
        burst=("star_ring", "ultimate", "attack", "skill", "branch"),
    ),
    "嗨♪爱愿妖精♪": AstralRingProfile(
        ring="天衍之杯",
        opener=("qte1", "qte2", "skill"),
        builder=("attack", "attack", "branch", "skill"),
        burst=("star_ring", "ultimate", "branch", "attack", "skill"),
    ),
    "咚！炽愿吉星": AstralRingProfile(
        ring="升变之理",
        opener=("qte1", "skill", "attack"),
        builder=("attack", "branch", "skill", "attack"),
        burst=("star_ring", "ultimate", "attack", "branch", "skill"),
    ),
    "一客逍游": AstralRingProfile(
        ring="命运之轮",
        opener=("qte1", "skill", "attack"),
        builder=("branch", "attack", "skill", "attack"),
        burst=("star_ring", "ultimate", "branch", "skill", "attack"),
    ),
    "位面武器·失序时空": AstralRingProfile(
        ring="世界之星",
        opener=("qte1", "qte2", "skill"),
        builder=("attack", "attack", "branch", "skill"),
        burst=("star_ring", "ultimate", "skill", "attack", "branch"),
    ),
    "逆命魔龙·降临！": AstralRingProfile(
        ring="命运之轮",
        opener=("skill", "attack", "branch"),
        builder=("attack", "skill", "branch", "attack"),
        burst=("star_ring", "ultimate", "skill", "branch", "attack"),
    ),
    "窈窕谍影": AstralRingProfile(
        ring="命运之轮",
        opener=("qte1", "skill", "attack"),
        builder=("attack", "branch", "skill", "attack"),
        burst=("star_ring", "ultimate", "skill", "branch", "attack"),
    ),
    "镇×偃月叩晓": AstralRingProfile(
        ring="天衍之杯",
        opener=("qte1", "skill", "attack"),
        builder=("attack", "branch", "skill", "attack"),
        burst=("star_ring", "ultimate", "branch", "skill", "attack"),
    ),
    "次生银翼": AstralRingProfile(
        ring="世界之星",
        opener=("lock", "qte1", "skill"),
        builder=("attack", "attack", "branch", "skill"),
        burst=("star_ring", "ultimate", "attack", "branch", "skill"),
    ),
    "药菀谜影": AstralRingProfile(
        ring="世界之星",
        opener=("qte1", "skill", "attack"),
        builder=("attack", "branch", "skill", "attack"),
        burst=("star_ring", "ultimate", "skill", "attack", "branch"),
    ),
    "天光驰彻": AstralRingProfile(
        ring="天衍之杯",
        opener=("qte1", "skill", "attack"),
        builder=("attack", "branch", "attack", "skill"),
        burst=("star_ring", "ultimate", "branch", "attack", "skill"),
    ),
    "天命难逃": AstralRingProfile(
        ring="天衍之杯",
        opener=("lock", "skill", "attack"),
        builder=("attack", "attack", "skill", "branch"),
        burst=("star_ring", "ultimate", "attack", "attack", "branch"),
    ),
    "浮生·渡尘之羽": AstralRingProfile(
        ring="通用",
        opener=("lock", "skill", "attack"),
        builder=("attack", "attack", "branch", "skill"),
        burst=("ultimate", "attack", "attack", "branch"),
        switch_after=False,
    ),
    "月下誓约·予爱以心": AstralRingProfile(
        ring="命运之轮",
        opener=("qte1", "qte2", "skill"),
        builder=("attack", "branch", "skill", "attack"),
        burst=("star_ring", "ultimate", "skill", "branch", "attack"),
    ),
}

ROLE_ALIASES = {
    "爱愿妖精": "嗨♪爱愿妖精♪",
    "炽愿吉星": "咚！炽愿吉星",
    "破弃孤光·逐影": "破弃弧光·逐影",
    "女武神·重机": "女武神·重击",
    "嗨~爱愿妖精♥": "嗨♪爱愿妖精♪",
}


class AstralRingFight(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        params = self._parse_params(getattr(argv, "custom_action_param", None))
        role_name = ROLE_ALIASES.get(params.get("role", "星环通用"), params.get("role", "星环通用"))
        profile = ROLE_PROFILES.get(role_name, ROLE_PROFILES["星环通用"])
        self.context = context
        self.actions = CombatActions(context, role_name)
        self.delay = max(float(params.get("delay", 0.055)), 0.01)
        self.star_ring_delay = max(float(params.get("star_ring_delay", 0.25)), 0.0)
        self.hanabi_special = bool(params.get("hanabi_special", True))

        if not self.actions.check_status("战斗中"):
            return CustomAction.RunResult(success=False)

        self.actions.logger.info("星环轮转开始: %s / %s", role_name, profile.ring)
        self._run_sequence(profile.opener)
        self._run_sequence(profile.builder)
        self._run_sequence(profile.burst, check_before=True)
        if profile.switch_after:
            self._tap("qte1")
        return CustomAction.RunResult(success=True)

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

    def _run_sequence(self, sequence: tuple[str, ...], check_before: bool = False) -> None:
        if check_before and not self.actions.check_status("战斗中"):
            return
        for command in sequence:
            self._do(command)

    def _do(self, command: str) -> None:
        if command == "attack":
            self._tap("攻击_action")
        elif command == "branch":
            self._tap("长按攻击_action", 0.12)
        elif command == "skill":
            self._tap("技能_action", 0.10)
        elif command == "ultimate":
            self._tap("必杀_action", 0.16)
            self._handle_hanabi_ultimate_prompt()
        elif command == "star_ring":
            self._tap("协同者_action", self.star_ring_delay)
        elif command == "qte1":
            self._tap("qte1", 0.08)
        elif command == "qte2":
            self._tap("qte2", 0.08)
        elif command == "dodge":
            self._tap("闪避_action", 0.08)
        elif command == "lock":
            self._tap("锁定视角_action", 0.04)

    def _tap(self, node: str, extra_delay: float = 0.0) -> None:
        self.context.run_action(node)
        time.sleep(self.delay + extra_delay)

    def _handle_hanabi_ultimate_prompt(self) -> None:
        if not self.hanabi_special:
            return
        for _ in range(2):
            time.sleep(0.18)
            try:
                self.context.run_action("处于花火大招中")
            except Exception as exc:
                self.actions.logger.debug("花火大招处理跳过: %s", exc)
                return
