"""
Knowledge Retrieval Module. Implements a simple RAG pipeline:
1. Load Markdown guide
2. Split into sections
3. Generate embeddings
4. Calculate cosine similarity
5. Return best matching sections
"""

from pathlib import Path
import re

from .ollama_client import embed

# Path to knowledge document
GUIDE_FILE = (Path(__file__).resolve().parent.parent/ "data"/ "it_operations_guide.md")

def load_guide_sections():
    # Load the guide and split it into sections.
    text = GUIDE_FILE.read_text(encoding="utf-8")
    sections = re.split(r"(?=^## )",text,flags=re.MULTILINE)
    chunks = []
    for section in sections:
        section = section.strip()
        if section.startswith("## "):
            title = (section.splitlines()[0].replace("## ", "").strip())
            chunks.append({"title": title,"text": section})
    return chunks

def cosine_similarity(a, b):
    # Calculate cosine similarity between vectors.
    dot_product = sum(
        x * y
        for x, y in zip(a, b)
    )
    magnitude_a = (
        sum(x * x for x in a)
    ) ** 0.5
    magnitude_b = (
        sum(y * y for y in b)
    ) ** 0.5
    if not magnitude_a or not magnitude_b:
        return 0.0
    return (dot_product /(magnitude_a * magnitude_b))

def retrieve_guide(question,top_k=3):
    # Retrieve best matching guide sections.
    sections = load_guide_sections()
    question_vector = embed(question)
    scored_results = []
    for section in sections:
        section_vector = embed(section["text"])
        score = cosine_similarity(question_vector,section_vector)
        scored_results.append((score,section))
    scored_results.sort(key=lambda item: item[0],reverse=True)
    selected = [
        {
            "title": section["title"],
            "text": section["text"],
            "score": round(score, 4)
        }
        for score, section
        in scored_results[:top_k]
        if score > 0.70
    ]
    return selected