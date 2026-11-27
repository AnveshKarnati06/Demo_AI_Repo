"""
Application configuration module.
"""

import os
from dotenv import load_dotenv

# Load values from .env into the environment
load_dotenv()

# Ollama server address
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL","http://localhost:11434").rstrip("/")
# Chat model used by the assistant
CHAT_MODEL = os.getenv("CHAT_MODEL","qwen2.5:3b")
# Embedding model used for RAG retrieval
EMBED_MODEL = os.getenv("EMBED_MODEL","nomic-embed-text")
# Maximum number of agent loop iterations
MAX_AGENT_STEPS = int(os.getenv("MAX_AGENT_STEPS","4"))