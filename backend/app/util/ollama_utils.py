import ollama

from ..core.config import settings


def stream_receive_message(messages: list[dict], model: str | None = None):
    model = model or settings.DEFAULT_MODEL
    collected = []
    try:
        for chunk in ollama.chat(model=model, messages=messages, stream=True):
            if "message" in chunk and "content" in chunk["message"]:
                content = chunk["message"]["content"]
                yield content
                collected.append(content)
    except Exception as e:
        raise RuntimeError(f"Ollama streaming error: {e}")