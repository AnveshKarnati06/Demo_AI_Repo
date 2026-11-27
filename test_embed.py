from app.ollama_client import embed

vector = embed(
    "VPN troubleshooting guide"
)

print(type(vector))
print(len(vector))
print(vector[:5])