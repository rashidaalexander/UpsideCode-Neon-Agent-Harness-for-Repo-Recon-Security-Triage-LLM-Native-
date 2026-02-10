from __future__ import annotations
from typing import Dict, Any
import requests
from upsidecode.core.tools import ToolSpec
from upsidecode.core.policy import check_domain

def _run(args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    cfg = ctx["cfg"]
    url = str(args.get("url",""))
    if not url:
        return {"ok": False, "error": "missing_url"}
    ok, reason = check_domain(url, cfg.get("allowlist_domains", []))
    if not ok:
        return {"ok": False, "error": reason}
    if (not cfg["perms"]["network"]) or cfg["mode"] in ("shadow","dry-run"):
        return {"ok": True, "dry_run": True, "url": url, "preview": "synthetic_response"}
    r = requests.get(url, timeout=20, headers={"User-Agent":"upsidecode/0.1"})
    return {"ok": True, "url": url, "status": r.status_code, "preview": r.text[:1200]}

TOOL = ToolSpec("net.fetch", "Fetch an allowlisted URL (blocked in shadow/dry-run or without network permission).", "medium", _run)
