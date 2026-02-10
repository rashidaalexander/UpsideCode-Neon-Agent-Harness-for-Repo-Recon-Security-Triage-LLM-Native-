from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
import json
import yaml

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def read_yaml(p: Path) -> Dict[str, Any]:
    return yaml.safe_load(read_text(p)) or {}

def write_yaml(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")

def read_json(p: Path) -> Dict[str, Any]:
    return json.loads(read_text(p))

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def write_jsonl(p: Path, rows: list[dict]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
