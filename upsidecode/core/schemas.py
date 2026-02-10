from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal
import time

Mode = Literal["shadow", "dry-run", "live"]

class SessionPerms(BaseModel):
    network: bool = False
    write_files: bool = False
    run_git: bool = True

class Config(BaseModel):
    mode: Mode = "shadow"
    workspace_root: str = "."
    allowlist_domains: List[str] = Field(default_factory=list)
    max_file_bytes: int = 2_000_000
    max_steps: int = 24
    perms: SessionPerms = SessionPerms()

class ToolCall(BaseModel):
    tool: str
    args: Dict[str, Any] = Field(default_factory=dict)

class Plan(BaseModel):
    objective: str
    steps: List[ToolCall]

class RunSummary(BaseModel):
    run_id: str
    created_at: str
    objective: str
    mode: Mode
    perms: SessionPerms
    steps: int
    outcomes: List[Dict[str, Any]]

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")
