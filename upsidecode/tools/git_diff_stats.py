from __future__ import annotations
from typing import Dict, Any
import subprocess
from upsidecode.core.tools import ToolSpec

def _run(args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    if not ctx["cfg"]["perms"]["run_git"]:
        return {"ok": False, "error": "git_disabled_by_policy"}
    r = subprocess.run(["git","diff","--stat"], capture_output=True, text=True, timeout=15)
    return {"ok": True, "stat": (r.stdout or "").strip()}

TOOL = ToolSpec("git.diff_stats", "Show git diff stats (read-only).", "low", _run)
