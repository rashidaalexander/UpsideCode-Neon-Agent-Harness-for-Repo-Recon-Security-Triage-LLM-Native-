from __future__ import annotations
from typing import List
import json
from ..core.llm import complete
from ..core.schemas import Plan
from .prompts import PLANNER_SYSTEM

def make_plan(objective: str, allowlist_tools: List[str], max_steps: int) -> Plan:
    raw = complete(PLANNER_SYSTEM, json.dumps({"objective": objective, "allowlist_tools": allowlist_tools, "max_steps": max_steps}, indent=2))
    return Plan.model_validate(json.loads(raw))
