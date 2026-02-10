from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from upsidecode.core.tools import ToolSpec
from upsidecode.core.policy import resolve_under_root

def _run(args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    root = Path(ctx["cfg"]["workspace_root"])
    target = resolve_under_root(root, Path(args.get("path",".") or "."))
    max_items = int(args.get("max_items", 250))
    items=[]
    for p in target.rglob("*"):
        if p.is_dir():
            continue
        items.append(str(p.relative_to(target)))
        if len(items) >= max_items:
            break
    return {"ok": True, "path": str(target), "files": items, "truncated": len(items) >= max_items}

TOOL = ToolSpec("repo.tree", "List files under a directory (bounded).", "low", _run)
