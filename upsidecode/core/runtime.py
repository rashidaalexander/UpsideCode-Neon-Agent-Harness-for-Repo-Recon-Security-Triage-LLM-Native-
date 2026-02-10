from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import uuid
import threading

from .schemas import Config, Plan, RunSummary, now_iso
from .tools import load_tools
from .io import write_json, write_jsonl

def _run_plan_sync(plan: Plan, cfg: Config, run_dir: Path) -> Dict[str, Any]:
    reg = load_tools()
    telemetry: List[dict] = []
    outcomes: List[dict] = []

    ctx = {"cfg": cfg.model_dump(), "run_dir": str(run_dir)}
    steps = plan.steps[: min(cfg.max_steps, 200)]

    for i, step in enumerate(steps, start=1):
        ev = {"timestamp": now_iso(), "step": i, "tool": step.tool, "args": step.args, "outcome": "unknown", "error": None}
        spec = reg.get(step.tool)
        if not spec:
            ev["outcome"] = "error"; ev["error"] = "unknown_tool"
            telemetry.append(ev); outcomes.append({"tool": step.tool, "ok": False, "error": "unknown_tool"})
            continue
        try:
            out = spec.run(step.args, ctx)
            ok = bool(out.get("ok", True))
            ev["outcome"] = "ok" if ok else "fail"
            outcomes.append({"tool": step.tool, **out})
        except Exception as e:
            ev["outcome"] = "error"; ev["error"] = str(e)
            outcomes.append({"tool": step.tool, "ok": False, "error": str(e)})
        telemetry.append(ev)

    summary = RunSummary(
        run_id=run_dir.name,
        created_at=now_iso(),
        objective=plan.objective,
        mode=cfg.mode,
        perms=cfg.perms,
        steps=len(steps),
        outcomes=outcomes,
    ).model_dump()

    write_json(run_dir / "summary.json", summary)
    write_jsonl(run_dir / "telemetry.jsonl", telemetry)
    return summary

def run(plan: Plan, cfg: Config, out_root: Path) -> Dict[str, Any]:
    out_root.mkdir(parents=True, exist_ok=True)
    run_dir = out_root / f"run_{uuid.uuid4().hex[:10]}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return _run_plan_sync(plan, cfg, run_dir)

def run_background(plan: Plan, cfg: Config, out_root: Path) -> str:
    out_root.mkdir(parents=True, exist_ok=True)
    run_id = f"bg_{uuid.uuid4().hex[:10]}"
    run_dir = out_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    def worker():
        _run_plan_sync(plan, cfg, run_dir)

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    (run_dir / "status.txt").write_text("running", encoding="utf-8")
    return str(run_dir)
