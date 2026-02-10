from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import re
from upsidecode.core.tools import ToolSpec
from upsidecode.core.policy import resolve_under_root

def _run(args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    root = Path(ctx["cfg"]["workspace_root"])
    target = resolve_under_root(root, Path(args.get("path",".") or "."))
    pattern = str(args.get("pattern",""))
    if not pattern:
        return {"ok": False, "error": "missing_pattern"}
    rx = re.compile(pattern)
    hits=[]
    for fp in target.rglob("*"):
        if not fp.is_file() or fp.stat().st_size > int(ctx["cfg"]["max_file_bytes"]):
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if rx.search(line):
                hits.append({"file": str(fp.relative_to(target)), "line": i, "text": line[:240]})
                if len(hits) >= 200:
                    return {"ok": True, "hits": hits, "truncated": True}
    return {"ok": True, "hits": hits, "truncated": False}

TOOL = ToolSpec("repo.search", "Regex search in repo (bounded).", "low", _run)
