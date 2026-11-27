"""
Ollama client module.
Provides helper functions for:
1. Chat completions
2. Embedding generation
"""

import requests
from functools import lru_cache

from .config import (OLLAMA_BASE_URL,CHAT_MODEL,EMBED_MODEL)

class OllamaError(RuntimeError):
    # Raised when Ollama cannot be contacted or returns an unexpected response.
    pass


def chat(messages, tools=None):
    """
    Send chat messages to Ollama.
    Parameters:
        messages (list): Chat history and prompts.
        tools (list): Optional tool definitions.
    Returns:
        dict: Assistant message returned by Ollama.
    """

    payload = {"model": CHAT_MODEL,"messages": messages,"stream": False}

    if tools:
        payload["tools"] = tools

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=120
        )

        response.raise_for_status()
        data = response.json()
        if "message" not in data:
            raise OllamaError(
                "Ollama response does not contain a message."
            )
        return data["message"]

    except requests.RequestException as exc:
        raise OllamaError(
            "Unable to connect to Ollama. "
            "Ensure Ollama is running and the model is available."
        ) from exc

@lru_cache(maxsize=128)
def embed(text):
    """
    Convert text into an embedding vector.
    Parameters:
        text (str): Input text.
    Returns:
        listEmbedding vector.
    """

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/embed",
            json={
                "model": EMBED_MODEL,
                "input": text
            },
            timeout=90
        )

        response.raise_for_status()

        data = response.json()

        embeddings = data.get("embeddings", [])

        if not embeddings:
            raise OllamaError(
                "Embedding model returned no vector."
            )

        return embeddings[0]

    except requests.RequestException as exc:
        raise OllamaError(
            "Unable to generate embeddings. "
            "Verify the embedding model exists."
        ) from exc