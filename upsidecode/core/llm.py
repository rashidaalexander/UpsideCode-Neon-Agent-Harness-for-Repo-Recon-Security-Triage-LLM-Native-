from __future__ import annotations
import os, requests

def complete(system: str, user: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    if provider == "openai":
        return _openai(system, user)
    return _ollama(system, user)

def _ollama(system: str, user: str) -> str:
    url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    prompt = f"{system}\n\nUser:\n{user}\n"
    r = requests.post(f"{url}/api/generate", json={"model": model, "prompt": prompt, "stream": False}, timeout=120)
    r.raise_for_status()
    return (r.json().get("response") or "").strip()

def _openai(system: str, user: str) -> str:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    r = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
              "input":[{"role":"system","content":system},{"role":"user","content":user}]},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    out = ""
    for item in data.get("output", []):
        for c in item.get("content", []):
            if c.get("type") == "output_text":
                out += c.get("text","")
    return out.strip()
