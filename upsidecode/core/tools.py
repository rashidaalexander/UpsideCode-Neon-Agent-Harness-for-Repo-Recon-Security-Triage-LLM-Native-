from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Callable
import importlib, pkgutil

@dataclass
class ToolSpec:
    name: str
    description: str
    risk: str
    run: Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]

def load_tools() -> dict[str, ToolSpec]:
    from upsidecode import tools as pkg
    reg: dict[str, ToolSpec] = {}
    for m in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
        mod = importlib.import_module(m.name)
        spec = getattr(mod, "TOOL", None)
        if isinstance(spec, ToolSpec):
            reg[spec.name] = spec
    return reg
