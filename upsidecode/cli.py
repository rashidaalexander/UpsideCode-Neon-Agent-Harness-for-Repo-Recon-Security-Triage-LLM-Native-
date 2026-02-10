from __future__ import annotations
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import yaml

from . import __version__
from .themes.neon import splash, tag
from .core.io import read_yaml, read_json, write_json
from .core.schemas import Config, Plan
from .core.tools import load_tools
from .agents.planner import make_plan
from .core.runtime import run, run_background

app = typer.Typer(add_completion=False, help="UpsideCode — LLM-native coding harness with background agents, tool registry, session permissions, and neon-terminal vibes.")
console = Console()

@app.command()
def banner():
    splash(console)

@app.command()
def tools():
    splash(console)
    reg = load_tools()
    tbl = Table(title="Tool Registry", show_lines=True)
    tbl.add_column("Tool", style="bold")
    tbl.add_column("Risk")
    tbl.add_column("Description")
    for t in sorted(reg.values(), key=lambda x: x.name):
        tbl.add_row(t.name, t.risk, t.description)
    console.print(tbl)

@app.command()
def init(out: Path = typer.Option(Path("configs/upside.yml"), "--out", "-o")):
    cfg = Config().model_dump()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    splash(console)
    console.print(Panel.fit(f"[bold]Config created[/bold]\n{out}", border_style="red"))

@app.command()
def plan(
    objective: str = typer.Argument(...),
    config: Path = typer.Option(Path("configs/upside.yml"), "--config", "-c", exists=True, readable=True),
    out: Path = typer.Option(Path("examples/plan.generated.json"), "--out", "-o"),
):
    splash(console)
    cfg = Config.model_validate(read_yaml(config))
    reg = load_tools()
    allow = sorted(reg.keys())
    tag(console, "Generating plan (LLM required).")
    plan_obj = make_plan(objective, allow, cfg.max_steps)
    write_json(out, plan_obj.model_dump())
    console.print(Panel.fit(f"[bold]Plan written[/bold]\n{out}\n[dim]Run it: upside run --plan {out}[/dim]", border_style="red"))

@app.command("run")
def run_cmd(
    plan: Path = typer.Option(..., "--plan", "-p", exists=True, readable=True),
    config: Path = typer.Option(Path("configs/upside.yml"), "--config", "-c", exists=True, readable=True),
    out: Path = typer.Option(Path(".upside/runs"), "--out", "-o"),
    background: bool = typer.Option(False, "--background"),
):
    splash(console)
    cfg = Config.model_validate(read_yaml(config))
    plan_obj = Plan.model_validate(read_json(plan))
    if background:
        tag(console, "Launching background run…")
        run_dir = run_background(plan_obj, cfg, out)
        console.print(Panel.fit(f"[bold]Background started[/bold]\n{run_dir}", border_style="red"))
        return
    tag(console, f"Executing in {cfg.mode} mode…")
    summ = run(plan_obj, cfg, out)
    console.print(Panel.fit(f"[bold]Run complete[/bold]\n{out}/{summ['run_id']}", border_style="red"))

@app.command()
def version():
    console.print(__version__)

def main():
    app()

if __name__ == "__main__":
    main()
