from ollama import chat

from backend.app.core.config import Settings

def receive_message(messages: list[dict]):
    # TODO internal prompting to tell LLM what to do and context
    stream = chat(
        model='llama3.2:3b',
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
        # TODO: Process each chunk as needed
    
    return stream.final_response
