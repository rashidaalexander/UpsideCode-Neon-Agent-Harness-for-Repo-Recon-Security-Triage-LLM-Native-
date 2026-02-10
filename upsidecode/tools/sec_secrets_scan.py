from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import re
from upsidecode.core.tools import ToolSpec
from upsidecode.core.policy import resolve_under_root

_PATTERNS = [
    ("PRIVATE_KEY", re.compile(r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("GITHUB_TOKEN", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,255}")),
    ("SLACK_TOKEN", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,48}")),
    ("AWS_KEY", re.compile(r"AKIA[0-9A-Z]{16}")),
]

def _scan_one(path: Path, max_bytes: int) -> List[Dict[str, Any]]:
    data = path.read_bytes()
    if len(data) > max_bytes:
        return []
    text = data.decode("utf-8", errors="replace")
    hits=[]
    for name, rx in _PATTERNS:
        for m in rx.finditer(text):
            hits.append({"file": str(path), "rule": name, "snippet": text[max(0,m.start()-30):m.end()+30]})
    return hits

def _run(args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    root = Path(ctx["cfg"]["workspace_root"])
    target = resolve_under_root(root, Path(str(args.get("path","."))))
    max_bytes = int(ctx["cfg"]["max_file_bytes"])
    include = set(args.get("include", [".py",".env",".txt",".json",".yml",".yaml",".toml",".md"]))

    files=[]
    if target.is_file():
        files=[target]
    else:
        for fp in target.rglob("*"):
            if fp.is_file() and (fp.suffix in include or fp.name==".env"):
                files.append(fp)

    hits=[]
    for fp in files[:2500]:
        hits.extend(_scan_one(fp, max_bytes))
    return {"ok": True, "target": str(target), "files_scanned": len(files), "hit_count": len(hits), "hits": hits}

TOOL = ToolSpec("sec.secrets_scan", "Defensive secrets scan for common token patterns.", "low", _run)
