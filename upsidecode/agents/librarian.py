from __future__ import annotations
from ..core.llm import complete
from .prompts import LIBRARIAN_SYSTEM

def summarize(text: str) -> str:
    return complete(LIBRARIAN_SYSTEM, text[:12000])
