from app.knowledge import retrieve_guide

results = retrieve_guide(
    "What is the laptop replacement policy?"
)

for item in results:
    print("-" * 60)
    print("TITLE:", item["title"])
    print("SCORE:", item["score"])
    print(item["text"])
