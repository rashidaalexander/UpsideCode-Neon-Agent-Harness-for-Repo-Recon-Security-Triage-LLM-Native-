from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from upsidecode.core.tools import ToolSpec
from upsidecode.core.policy import resolve_under_root

def _run(args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    root = Path(ctx["cfg"]["workspace_root"])
    p = resolve_under_root(root, Path(args.get("path","") or ""))
    max_bytes = int(ctx["cfg"]["max_file_bytes"])
    data = p.read_bytes()
    if len(data) > max_bytes:
        return {"ok": False, "error": "file_too_large", "bytes": len(data)}
    return {"ok": True, "path": str(p), "content": data.decode("utf-8", errors="replace")}

TOOL = ToolSpec("repo.read", "Read a file under workspace_root with size limits.", "low", _run)
