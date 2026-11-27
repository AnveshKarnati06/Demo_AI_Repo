from app.ollama_client import chat

messages = [
    {
        "role": "user",
        "content": "Hello! Tell me about yourself."
    }
]

response = chat(messages)

print(response)