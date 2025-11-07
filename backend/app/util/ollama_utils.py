from ollama import chat

from backend.app.core.config import Settings

def receive_message(messages: list[dict]):
    # TODO internal prompting to tell LLM what to do and context
    stream = chat(
        model=Settings.JWT_SECRET,
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        # TODO: Process each chunk as needed
        pass
    
    return stream.final_response
