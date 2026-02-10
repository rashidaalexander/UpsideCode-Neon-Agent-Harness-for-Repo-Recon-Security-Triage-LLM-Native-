# UpsideCode 🟥 (Neon Edition)

A **thorough, tool-like** LLM harness inspired by modern agent orchestrators — with a supernatural 80s neon terminal vibe (original ASCII only).

Why it feels “big”:
- **Tool registry** (repo tools + security + LLM)
- **Background runs** (`--background`)
- **Session permissions** + safe defaults
- **Telemetry artifacts** per run (`summary.json`, `telemetry.jsonl`)
- **LLM plan generation** constrained to allowlisted tools

Inspired by the *style* and thoroughness of popular agent harness repos like `oh-my-opencode`. 
---

## Install

```bash
pip install .
```

## Quickstart

```bash
upside init
upside tools
upside run --plan examples/plan.json
```

Runs land in `.upside/runs/`.

---

## LLM setup

Default: **Ollama** (local)
```bash
ollama serve
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3.1:8b
```

Optional: **OpenAI**
```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=...
export OPENAI_MODEL=gpt-4.1-mini
```

---

## Generate a plan with the LLM

```bash
upside plan "Summarize this repo and list 5 actionable improvements" --out examples/plan.generated.json
upside run --plan examples/plan.generated.json
```

---

## Safety model

- Default `mode: shadow` + `perms.network: false` → **no network execution**
- Repo tools are bounded (size/line limits)
- Security tools are **defensive** only (secrets detection)

---

## License
MIT
