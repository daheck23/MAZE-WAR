#
# Datei: complex_llm_crew_workflow.py
#
# Dieses Skript demonstriert den gewünschten komplexen Kommunikationsfluss:
# 1. PyTorch -> PyTorch
# 2. PyTorch -> TensorFlow
# 3. TensorFlow -> LLM (llama-cpp)
# 4. LLM -> TensorFlow
#
# Die Integration von llama-cpp ist hier zentral, da es als Brücke
# zwischen den rein numerischen Berechnungen dient.
#
import torch
import tensorflow as tf
import re
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from typing import Dict, Any

# -----------------------------------------------------------------------------
# LLM-Import und Konfiguration für Llama-CPP
# -----------------------------------------------------------------------------
try:
    from llama_cpp import Llama
    print("✅ llama-cpp Modul erfolgreich geladen.")
except ImportError:
    print("❌ Fehler: 'llama-cpp-python' ist nicht installiert. Bitte installieren Sie es mit 'pip install llama-cpp-python'.")
    exit()

# Geben Sie den absoluten Pfad zu Ihrer GGUF-Modell-Datei an.
# Passen Sie diesen Pfad an Ihre lokale Umgebung an.
model_path = "C:\\lab\\llama-cpp\\llama-2-7b-chat.Q4_K_M.gguf"

# Globale Llama-Instanz, um sicherzustellen, dass das Modell nur einmal geladen wird.
try:
    llama_model = Llama(model_path=model_path, n_ctx=2048)
    print(f"✅ Llama-Modell erfolgreich von '{model_path}' geladen.")
except FileNotFoundError:
    print(f"❌ Fehler: Das Llama-Modell wurde unter dem Pfad '{model_path}' nicht gefunden.")
    print("Bitte überprüfen Sie den Pfad und stellen Sie sicher, dass die Datei existiert.")
    exit()
except Exception as e:
    print(f"❌ Ein unerwarteter Fehler ist beim Laden des Llama-Modells aufgetreten: {e}")
    exit()

@tool
def process_with_llama(input_data: Dict[str, Any]) -> str:
    """
    Verarbeitet einen numerischen Wert durch das lokale Llama-Modell.
    Generiert eine zusammenfassende Beschreibung, die eine neue Zahl enthält.
    """
    print("\n--- LLM-Agent (Llama-CPP): Daten zur Analyse erhalten. ---")
    
    number = input_data.get("value")
    if number is None:
        return "❌ Fehler: Keine Zahl für die LLM-Analyse erhalten."
    
    # Erstellt einen Prompt für das Llama-Modell.
    # Wir fragen das Modell, eine neue Zahl in den Text einzubauen.
    prompt = f"The input value is {number}. Summarize this and generate a new number that is double the input value. Format the output like this: 'Summary: [Your summary]. The new value is [New value].'"

    # Führt die Inferenz mit dem geladenen Modell durch.
    try:
        output = llama_model(prompt, max_tokens=100, stop=["Q:", "\n"], echo=False)
        llm_text = output["choices"][0]["text"].strip()
        print(f"✅ Llama-Analyse abgeschlossen. Output: {llm_text}")
        return llm_text
    except Exception as e:
        print(f"❌ Fehler bei der Inferenz mit Llama-Modell: {e}")
        return "Fehler bei der LLM-Analyse."

# -----------------------------------------------------------------------------
# Agenten definieren
# -----------------------------------------------------------------------------

# Agent für den ersten PyTorch-Schritt
torch_agent_1 = Agent(
    role="PyTorch Initial Processor",
    goal="Führe eine erste Vektoraddition mit PyTorch durch.",
    backstory=(
        "Ein grundlegender Datenverarbeiter, der die ersten numerischen Operationen "
        "mit PyTorch durchführt."
    ),
    verbose=True,
    allow_delegation=False
)

# Agent für den zweiten PyTorch-Schritt
torch_agent_2 = Agent(
    role="PyTorch Secondary Processor",
    goal="Erhalte Daten von einem anderen PyTorch-Agenten und transformiere sie weiter.",
    backstory=(
        "Ein fortgeschrittener PyTorch-Spezialist, der die Ausgabe von Vektoroperationen "
        "versteht und eine weitere mathematische Transformation anwendet."
    ),
    verbose=True,
    allow_delegation=False
)

# Agent für den ersten TensorFlow-Schritt
tensorflow_agent_1 = Agent(
    role="TensorFlow Intermediate Analyst",
    goal="Nimm die Ausgabe eines PyTorch-Agenten und berechne die Summe mit TensorFlow.",
    backstory=(
        "Ein Analyst, der als Brücke zwischen PyTorch und dem LLM fungiert."
    ),
    verbose=True,
    allow_delegation=False
)

# Agent, der das Llama-Modell verwendet
llm_agent = Agent(
    role="Local LLM Interpreter",
    goal="Verwende ein lokales Sprachmodell, um numerische Daten zu interpretieren und einen neuen Wert zu generieren.",
    backstory=(
        "Ein KI-Experte, der fortschrittliche Sprachmodelle wie Llama-CPP nutzt, um "
        "die Ergebnisse von Berechnungen zu verarbeiten."
    ),
    tools=[process_with_llama], # Verwendet das Llama-Tool
    verbose=True,
    allow_delegation=False
)

# Agent für den letzten TensorFlow-Schritt
tensorflow_agent_2 = Agent(
    role="TensorFlow Finalizer",
    goal="Nimm die Textausgabe des LLM-Agenten, extrahiere den Wert und führe die finale Berechnung durch.",
    backstory=(
        "Der finale TensorFlow-Experte, der die endgültige Berechnung im Workflow durchführt "
        "und das Endergebnis liefert."
    ),
    verbose=True,
    allow_delegation=False
)

# -----------------------------------------------------------------------------
# Aufgaben definieren
# Jede Aufgabe repräsentiert eine Kommunikationsstufe.
# -----------------------------------------------------------------------------

# Schritt 1: PyTorch -> PyTorch
torch_to_torch_task = Task(
    description=(
        "Führe eine PyTorch-Vektoraddition durch. Verwende den Startvektor [10, 20, 30] "
        "und addiere [1, 1, 1] hinzu. Die Ausgabe ist eine Python-Liste."
    ),
    agent=torch_agent_1,
    expected_output="Eine Python-Liste, die das Ergebnis der Vektoraddition enthält."
)

# Schritt 2: PyTorch -> TensorFlow
torch_to_tensorflow_task = Task(
    description=(
        "Nimm das Ergebnis der 'PyTorch Initial Processor'-Aufgabe. Führe eine elementweise "
        "Multiplikation mit dem Vektor [2, 2, 2] durch und berechne dann die Summe aller Elemente. "
        "Gib die Summe als Python-Skalar zurück."
    ),
    agent=torch_agent_2,
    context=[torch_to_torch_task],
    expected_output="Ein einzelner numerischer Wert."
)

# Schritt 3: TensorFlow -> LLM
tensorflow_to_llm_task = Task(
    description=(
        "Nimm die skalare Summe aus der vorherigen Aufgabe und verarbeite sie mit dem lokalen "
        "Llama-Modell. Verwende das bereitgestellte Tool, um eine Textzusammenfassung zu generieren, "
        "die einen neuen, abgeleiteten Wert enthält."
    ),
    agent=llm_agent,
    context=[torch_to_tensorflow_task],
    expected_output="Ein String, der eine Textzusammenfassung und einen neuen Wert enthält."
)

# Schritt 4: LLM -> TensorFlow
llm_to_tensorflow_task = Task(
    description=(
        "Nimm die Textausgabe des LLM-Agenten. Extrahiere den neuen Wert, der im Text erwähnt wird, "
        "und berechne das Quadrat dieses Wertes mit TensorFlow. Gib das Endergebnis als String aus."
    ),
    agent=tensorflow_agent_2,
    context=[tensorflow_to_llm_task],
    expected_output="Ein String, der das Endergebnis der finalen TensorFlow-Berechnung enthält."
)

# -----------------------------------------------------------------------------
# Hilfsfunktionen zur Simulation der Berechnungen
# -----------------------------------------------------------------------------

def run_torch_1_calc():
    """Simuliert Schritt 1: PyTorch -> PyTorch"""
    tensor_a = torch.tensor([10, 20, 30], dtype=torch.float32)
    tensor_b = torch.tensor([1, 1, 1], dtype=torch.float32)
    result = (tensor_a + tensor_b).tolist()
    print(f"\n--- PyTorch Agent 1: Vektoraddition abgeschlossen. Ergebnis: {result} ---")
    return {"data": result}

def run_torch_2_calc(context):
    """Simuliert Schritt 2: PyTorch -> TensorFlow"""
    input_data = context.get("data", [])
    if not input_data:
        print("❌ Fehler: Keine Daten von PyTorch 1 erhalten.")
        return {"value": 0}
    
    tensor_in = torch.tensor(input_data, dtype=torch.float32)
    tensor_mult = torch.tensor([2, 2, 2], dtype=torch.float32)
    result = (tensor_in * tensor_mult).sum().item()
    print(f"\n--- PyTorch Agent 2: Vektormultiplikation und Summe abgeschlossen. Ergebnis: {result} ---")
    return {"value": result}

def run_tensorflow_2_calc(context):
    """Simuliert Schritt 4: LLM -> TensorFlow"""
    llm_result_text = context
    print(f"\n--- TensorFlow Agent 2: Text von LLM erhalten: '{llm_result_text}' ---")
    
    # Extrahiere den neuen Wert aus dem Text.
    # Hier verwenden wir einen regulären Ausdruck, um den Wert zu finden.
    match = re.search(r'The new value is (\d+\.?\d*)', llm_result_text)
    if not match:
        print("❌ Fehler: Konnte den neuen Wert nicht aus dem LLM-Text extrahieren.")
        return "Berechnung fehlgeschlagen."
        
    try:
        new_value = float(match.group(1))
    except (ValueError, IndexError):
        print("❌ Fehler: Konnte den extrahierten Wert nicht in eine Zahl umwandeln.")
        return "Berechnung fehlgeschlagen."
        
    tf_tensor = tf.constant(new_value, dtype=tf.float32)
    final_result = tf.square(tf_tensor).numpy()
    print(f"\n--- TensorFlow Agent 2: Endgültige Berechnung (Quadrat) abgeschlossen. Ergebnis: {final_result} ---")
    return f"Endgültiges Resultat: {final_result}"

# Weisen Sie die Ausführungsfunktionen den Aufgaben zu
torch_to_torch_task._execute = run_torch_1_calc
torch_to_tensorflow_task._execute = lambda: run_torch_2_calc(torch_to_torch_task.output)
tensorflow_to_llm_task._execute = lambda: process_with_llama.run(tensorflow_to_llm_task.context[0].output)
llm_to_tensorflow_task._execute = lambda: run_tensorflow_2_calc(llm_to_tensorflow_task.context[0].output)

# Erstelle die Crew
crew = Crew(
    agents=[torch_agent_1, torch_agent_2, tensorflow_agent_1, llm_agent, tensorflow_agent_2],
    tasks=[torch_to_torch_task, torch_to_tensorflow_task, tensorflow_to_llm_task, llm_to_tensorflow_task],
    process=Process.sequential,
    verbose=2
)

# Starte den Workflow
print("\n=== CrewAI Workflow gestartet ===")
final_result = crew.kickoff()
print("\n=== Workflow abgeschlossen ===")
print(f"Endgültiges Resultat der Crew: {final_result}")
