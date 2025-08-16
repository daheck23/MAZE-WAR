from llama_cpp import Llama

# Den Pfad zum GGUF-Modell angeben
# Option 1: Backslashes verdoppeln
model_path = "C:\\lab\\llama-cpp\\llama-2-7b-chat.Q4_K_M.gguf"

# Option 2: Raw-String verwenden (empfohlen)
# model_path = r"C:\lab\llama-cpp\llama-2-7b-chat.Q4_K_M.gguf"

# Llama-Modell laden
llm = Llama(model_path=model_path)

# Eine einfache Abfrage an das Modell senden
prompt = "Wie alt ist die Erde?"

# Eine Antwort generieren
output = llm(
    prompt,
    max_tokens=256,
    stop=["Q:", "\n"],
    echo=True,
)

# Die Antwort ausgeben
print(output["choices"][0]["text"])