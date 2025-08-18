#
# Datei: crew_workflow.py
#
# Dieses Skript demonstriert einen CrewAI-Workflow, bei dem ein PyTorch-Agent,
# ein LLM-Agent (simuliert über Gemini-API) und ein TensorFlow-Agent
# sequenziell zusammenarbeiten und ihre Ergebnisse übergeben.
#

import torch
import tensorflow as tf
import time
import json
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from typing import Dict, Any

# -----------------------------------------------------------------------------
# WICHTIG:
# Dieses Skript simuliert einen API-Aufruf an das Gemini-Modell.
# In einer echten Umgebung benötigen Sie eine API-Verbindung, die CrewAI
# nativ über die .env-Datei oder Umgebungsvariablen verwaltet.
# Hier zeigen wir den logischen Fluss.
# -----------------------------------------------------------------------------

# Ein Tool, das die Kommunikation mit einem LLM simuliert.
# Es nimmt Daten entgegen und gibt eine formatierte JSON-Antwort zurück.
@tool
def process_with_llm(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simuliert die Verarbeitung von Daten durch ein LLM (Gemini API).
    Erzeugt eine zusammenfassende Nachricht und berechnet die Summe.
    """
    print("\n--- LLM-Agent: Daten für die Analyse erhalten. ---")
    
    # Simuliere die Antwort eines echten API-Aufrufs.
    numbers = input_data.get("numbers", [])
    if not numbers:
        print("❌ Fehler: Keine Zahlen für die LLM-Analyse erhalten.")
        return {"summary": "Fehler: Keine Zahlen zur Analyse.", "sum": 0}

    total_sum = sum(numbers)
    
    # Mock der JSON-Antwort, die wir von einem echten LLM erwarten würden
    mock_llm_response = {
        "summary": f"Der PyTorch-Agent hat eine Reihe von Zahlen berechnet. "
                   f"Die Summe dieser Zahlen ist {total_sum}.",
        "sum": total_sum
    }
    
    print(f"✅ LLM-Analyse abgeschlossen. Summary: {mock_llm_response['summary']}")
    return mock_llm_response

# -----------------------------------------------------------------------------
# Agenten definieren
# -----------------------------------------------------------------------------

pytorch_agent = Agent(
    role="PyTorch Data Processor",
    goal="Führe komplexe mathematische Operationen aus und verarbeite numerische Daten.",
    backstory=(
        "Ein erfahrener Spezialist in der Datenverarbeitung und numerischen Berechnung "
        "mit PyTorch. Er ist bekannt für seine Präzision und Effizienz bei der "
        "Transformation von Daten."
    ),
    verbose=True,
    allow_delegation=False
)

llm_agent = Agent(
    role="LLM Analyst",
    goal="Verwende ein großes Sprachmodell, um numerische Daten zu analysieren und zu interpretieren.",
    backstory=(
        "Ein KI-Experte, der fortschrittliche Sprachmodelle wie Gemini API nutzt, um "
        "menschlich lesbare Zusammenfassungen aus maschinell generierten Daten zu erstellen."
    ),
    tools=[process_with_llm],
    verbose=True,
    allow_delegation=False
)

tensorflow_agent = Agent(
    role="TensorFlow Finalizer",
    goal="Nimm die Ausgabe des LLM-Agenten und führe abschließende Berechnungen durch.",
    backstory=(
        "Ein Analyst, der die Leistungsfähigkeit von TensorFlow für abschließende "
        "statistische Auswertungen und die Visualisierung von Ergebnissen nutzt."
    ),
    verbose=True,
    allow_delegation=False
)

# -----------------------------------------------------------------------------
# Aufgaben definieren
# -----------------------------------------------------------------------------

pytorch_task = Task(
    description=(
        "Führe eine Vektoraddition mit PyTorch durch. Beginne mit einem Startvektor [1, 2, 3] "
        "und addiere einen zweiten Vektor [4, 5, 6]. Gib das Ergebnis als Python-Liste zurück."
    ),
    agent=pytorch_agent,
    expected_output="Eine Python-Liste, die die Ergebnisse der PyTorch-Berechnung enthält."
)

llm_task = Task(
    description=(
        "Analysiere die numerischen Ergebnisse der vorherigen PyTorch-Aufgabe. Verwende das "
        "bereitgestellte Tool, um eine verständliche Zusammenfassung zu erstellen und die "
        "Summe der Zahlen zu ermitteln."
    ),
    agent=llm_agent,
    context=[pytorch_task],
    expected_output="Ein Dictionary mit einem String für die Zusammenfassung und einem numerischen Wert für die Summe."
)

tensorflow_task = Task(
    description=(
        "Nimm die Summe aus der LLM-Analyse. Erstelle einen TensorFlow-Tensor aus dieser Summe "
        "und multipliziere ihn mit 2.5, um ein endgültiges Ergebnis zu erhalten."
    ),
    agent=tensorflow_agent,
    context=[llm_task],
    expected_output="Ein String, der das Endergebnis der TensorFlow-Berechnung darstellt."
)

# -----------------------------------------------------------------------------
# Crew zusammenstellen und starten
# -----------------------------------------------------------------------------

# Definiere die Funktionen, die von den Agenten ausgeführt werden
def run_pytorch_calculation():
    """Simuliert die PyTorch-Aktion und gibt das Ergebnis zurück."""
    tensor_a = torch.tensor([1, 2, 3], dtype=torch.float32)
    tensor_b = torch.tensor([4, 5, 6], dtype=torch.float32)
    result_tensor = tensor_a + tensor_b
    result_list = result_tensor.tolist()
    print(f"\n--- PyTorch-Agent: Berechnung abgeschlossen. Ergebnis: {result_list} ---")
    return {"numbers": result_list}

def run_tensorflow_calculation(llm_result):
    """Simuliert die TensorFlow-Aktion mit dem Ergebnis des LLM-Agenten."""
    llm_sum = llm_result.get("sum")
    if llm_sum is None:
        print("❌ Fehler: Keine Summe vom LLM-Agenten erhalten.")
        return "Berechnung fehlgeschlagen."
        
    tf_tensor = tf.constant(llm_sum, dtype=tf.float32)
    final_result = tf_tensor * 2.5
    print(f"\n--- TensorFlow-Agent: Endgültige Berechnung abgeschlossen. Ergebnis: {final_result.numpy()} ---")
    return f"Endgültiges Ergebnis: {final_result.numpy()}"

# Überschreibe die `_execute` Methoden der Tasks, um die Funktionen aufzurufen
pytorch_task._execute = run_pytorch_calculation
llm_task._execute = lambda: llm_agent.tools[0].run(pytorch_task.output) # Übergibt die Ausgabe des ersten Tasks
tensorflow_task._execute = lambda: run_tensorflow_calculation(llm_task.output) # Übergibt die Ausgabe des zweiten Tasks


# Erstelle die Crew
crew = Crew(
    agents=[pytorch_agent, llm_agent, tensorflow_agent],
    tasks=[pytorch_task, llm_task, tensorflow_task],
    process=Process.sequential,
    verbose=2
)

# Starte den Workflow
print("\n=== CrewAI Workflow gestartet ===")
final_result = crew.kickoff()
print("\n=== Workflow abgeschlossen ===")
print(f"Endgültiges Resultat der Crew: {final_result}")

