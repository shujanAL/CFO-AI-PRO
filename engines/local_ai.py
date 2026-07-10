import json
import urllib.error
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:3b"


def _compact_context(context):
    safe_context = {
        "metrics": context.get("metrics", {}),
        "health": context.get("health", {}),
        "financing": context.get("financing", {}),
        "best_decision": context.get("best_decision", {}),
        "recommendation": context.get("recommendation", ""),
        "forecast": context.get("forecast", []),
        "top_decisions": context.get("top_decisions", []),
        "decision_history": context.get("decision_history", []),
    }
    return json.dumps(safe_context, ensure_ascii=False, default=str)


def is_ollama_available(timeout=1.5):
    try:
        request = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def ask_local_ai(question, context, language="en", model=DEFAULT_MODEL, timeout=20):
    if not is_ollama_available():
        return None, "Unavailable", "Ollama is not running on this machine."

    lang_instruction = (
        "Answer in Arabic. Keep the answer concise, practical, and based only on the provided financial context."
        if language == "ar"
        else "Answer in English. Keep the answer concise, practical, and based only on the provided financial context."
    )
    prompt = f"""
You are CFO AI PRO, a privacy-first financial copilot.
Use only the JSON context below. Do not invent facts, external market data, or guarantees.
If the context is not enough, say what is missing and give a cautious next step.

{lang_instruction}

Financial context:
{_compact_context(context)}

User question:
{question}
"""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2},
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            OLLAMA_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
            answer = result.get("response", "").strip()
            if not answer:
                return None, "Unavailable", "Ollama returned an empty response."
            return answer, "Local AI", None
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None, "Unavailable", f"Ollama model '{model}' is not installed."
        return None, "Unavailable", f"Ollama HTTP error: {error.code}"
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
        return None, "Unavailable", f"Ollama is unavailable: {error}"
