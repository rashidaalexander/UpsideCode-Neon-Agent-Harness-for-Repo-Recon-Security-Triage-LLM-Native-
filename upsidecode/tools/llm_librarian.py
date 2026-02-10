from __future__ import annotations
from typing import Dict, Any
import json
from upsidecode.core.tools import ToolSpec
from upsidecode.agents.librarian import summarize

def _run(args: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    out = summarize(json.dumps(args, indent=2))
    return {"ok": True, "summary": out}

TOOL = ToolSpec("llm.librarian", "LLM: summarize provided context (repo map/findings) into an overview + risks + next actions.", "low", _run)
