from __future__ import annotations
from pathlib import Path
from urllib.parse import urlparse
from typing import Tuple

def resolve_under_root(root: Path, target: Path) -> Path:
    root = root.resolve()
    t = (root / target).resolve() if not target.is_absolute() else target.resolve()
    if not str(t).startswith(str(root)):
        raise ValueError("path_outside_workspace_root")
    return t

def check_domain(url: str, allowlist: list[str]) -> Tuple[bool, str]:
    host = urlparse(url).hostname or ""
    if allowlist and host not in allowlist:
        return False, "domain_not_allowlisted"
    return True, "ok"
