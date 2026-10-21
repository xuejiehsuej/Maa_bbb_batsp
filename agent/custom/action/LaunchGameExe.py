"""
Launch the Windows game executable directly.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from maa.context import Context
from maa.custom_action import CustomAction

from ..utils.Logger import Logger


REJECTED_EXE_NAMES = {
    "launcher.exe",
    "uninstall.exe",
    "crashreport.exe",
    "7z.exe",
    "hpatchz.exe",
    "qtwebengineprocess.exe",
    "vc_redist.x64.exe",
    "update.exe",
    "iconrefresher.exe",
    "apm4webcrashr.exe",
    "zfgamebrowser.exe",
}
PREFERRED_EXE_NAMES = (
    "BH3.exe",
    "BH3rd.exe",
    "Honkai Impact 3.exe",
    "HonkaiImpact3.exe",
)


class LaunchGameExe(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:
        logger = Logger("LaunchGameExe", context)
        params = self._parse_params(getattr(argv, "custom_action_param", None))
        configured_path = str(params.get("exe_path", "")).strip().strip('"')

        exe_path = self._resolve_game_exe(configured_path)
        if exe_path is None:
            logger.ui(
                "未找到崩坏三游戏主程序。请在启动任务里填写真实游戏 exe，或填写包含 BH3.exe 的游戏目录。不要填写 launcher.exe。",
                "red",
            )
            return CustomAction.RunResult(success=False)

        if exe_path.name.lower() in REJECTED_EXE_NAMES:
            logger.ui("已拒绝启动 launcher.exe，请填写真正的游戏主程序 exe。", "red")
            return CustomAction.RunResult(success=False)

        if self._is_process_running(exe_path.name):
            logger.ui(f"检测到 {exe_path.name} 已在运行，继续进入游戏流程。", "green")
            return CustomAction.RunResult(success=True)

        try:
            subprocess.Popen(
                [str(exe_path)],
                cwd=str(exe_path.parent),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                close_fds=True,
            )
        except OSError as exc:
            logger.ui(f"启动游戏失败：{exc}", "red")
            return CustomAction.RunResult(success=False)

        logger.ui(f"已启动游戏主程序：{exe_path.name}", "green")
        return CustomAction.RunResult(success=True)

    def _parse_params(self, raw: Any) -> dict[str, Any]:
        if isinstance(raw, dict):
            return raw
        if not raw:
            return {}
        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                return {}
            return parsed if isinstance(parsed, dict) else {}
        return {}

    def _resolve_game_exe(self, raw_path: str) -> Path | None:
        if not raw_path or "{" in raw_path or "}" in raw_path:
            return None

        expanded = Path(os.path.expandvars(os.path.expanduser(raw_path)))
        if expanded.is_file():
            return expanded if expanded.suffix.lower() == ".exe" else None
        if expanded.is_dir():
            return self._find_exe_in_dir(expanded)
        return None

    def _find_exe_in_dir(self, directory: Path) -> Path | None:
        games_dir = directory / "Games"
        for name in PREFERRED_EXE_NAMES:
            candidate = games_dir / name
            if candidate.is_file():
                return candidate

        for name in PREFERRED_EXE_NAMES:
            candidate = directory / name
            if candidate.is_file():
                return candidate

        for child in directory.rglob("*.exe"):
            if not child.is_file() or child.suffix.lower() != ".exe":
                continue
            if child.name.lower() in REJECTED_EXE_NAMES:
                continue
            if "updateprogram" in {part.lower() for part in child.parts}:
                continue
            return child
        return None

    def _is_process_running(self, process_name: str) -> bool:
        try:
            output = subprocess.check_output(
                ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
                text=True,
                encoding="gbk",
                errors="ignore",
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception:
            return False
        return process_name.lower() in output.lower()
