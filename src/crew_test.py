#
# Datei: crew_complex_workflow.py
#
# Dieses Skript demonstriert einen komplexen, nicht-sequenziellen CrewAI-Workflow,
# indem es vier separate Agenten und Aufgaben erstellt, die den
# gewünschten Kommunikationsfluss abbilden:
# 1. PyTorch -> PyTorch
# 2. PyTorch -> TensorFlow
# 3. TensorFlow -> PyTorch
# 4. TensorFlow -> TensorFlow
#
# Jeder Schritt verarbeitet die Ausgabe des vorherigen Schritts.
#

import torch
import tensorflow as tf
import time
from crewai import Agent, Task, Crew, Process
from typing import Dict, Any

# -----------------------------------------------------------------------------
# Agenten definieren
# Jeder Agent hat eine klare Rolle und einen klaren Zweck.
# -----------------------------------------------------------------------------

# Agent für den ersten PyTorch-Schritt
torch_agent_1 = Agent(
    role="PyTorch Initial Processor",
    goal="Führe eine erste Vektoraddition mit PyTorch durch.",
    backstory=(
        "Ein grundlegender Datenverarbeiter, der die ersten numerischen Operationen "
        "mit PyTorch durchführt und die Daten für den nächsten Agenten vorbereitet."
    ),
    verbose=True,
    allow_delegation=False
)

# Agent für den zweiten PyTorch-Schritt (empfängt von Torch)
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

# Agent für den ersten TensorFlow-Schritt (empfängt von Torch)
tensorflow_agent_1 = Agent(
    role="TensorFlow Bridge Analyst",
    goal="Nimm die Ausgabe eines PyTorch-Agenten und berechne die Summe mit TensorFlow.",
    backstory=(
        "Ein Analyst, der als Brücke zwischen PyTorch- und TensorFlow-Operationen fungiert. "
        "Er konvertiert die Vektor-Ausgabe in eine Skalar-Summe und übergibt sie."
    ),
    verbose=True,
    allow_delegation=False
)

# Agent für den dritten PyTorch-Schritt (empfängt von TensorFlow)
torch_agent_3 = Agent(
    role="PyTorch Reverse Processor",
    goal="Verarbeite das Ergebnis eines TensorFlow-Agenten mit PyTorch.",
    backstory=(
        "Ein vielseitiger PyTorch-Ingenieur, der in der Lage ist, Skalarwerte von TensorFlow "
        "zu nehmen und eine neue Vektoroperation durchzuführen."
    ),
    verbose=True,
    allow_delegation=False
)

# Agent für den zweiten TensorFlow-Schritt (empfängt von TensorFlow)
tensorflow_agent_2 = Agent(
    role="TensorFlow Finalizer",
    goal="Nimm die Ausgabe des PyTorch-Agenten und berechne das endgültige Ergebnis mit TensorFlow.",
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

torch_to_torch_task = Task(
    description=(
        "Führe eine PyTorch-Vektoraddition durch. Verwende einen Startvektor [10, 20, 30] "
        "und addiere [1, 1, 1] hinzu. Die Ausgabe ist eine Python-Liste."
    ),
    agent=torch_agent_1,
    expected_output="Eine Python-Liste, die das Ergebnis der Vektoraddition enthält."
)

torch_to_tensorflow_task = Task(
    description=(
        "Nimm das Ergebnis der 'PyTorch Initial Processor'-Aufgabe. Führe eine elementweise "
        "Multiplikation mit dem Vektor [2, 2, 2] durch und gib das neue Ergebnis als Liste aus."
    ),
    agent=torch_agent_2,
    context=[torch_to_torch_task],
    expected_output="Eine Python-Liste, die das Ergebnis der zweiten PyTorch-Berechnung enthält."
)

tensorflow_to_torch_task = Task(
    description=(
        "Nimm die Ausgabe der 'PyTorch Secondary Processor'-Aufgabe. Konvertiere die Liste in "
        "einen TensorFlow-Tensor und berechne die Summe aller Elemente. Gib die Summe als Python-Skalar zurück."
    ),
    agent=tensorflow_agent_1,
    context=[torch_to_tensorflow_task],
    expected_output="Ein einzelner numerischer Wert, der die Summe des Vektors darstellt."
)

tensorflow_to_tensorflow_task = Task(
    description=(
        "Nimm die skalare Summe aus der 'TensorFlow Bridge Analyst'-Aufgabe. Erstelle einen "
        "PyTorch-Tensor, multipliziere ihn mit 10 und gib das Ergebnis als neue Liste aus."
    ),
    agent=torch_agent_3,
    context=[tensorflow_to_torch_task],
    expected_output="Eine Python-Liste, die das Ergebnis der PyTorch-Multiplikation enthält."
)

final_tensorflow_task = Task(
    description=(
        "Nimm die Ausgabe der 'PyTorch Reverse Processor'-Aufgabe. Konvertiere die Liste in einen "
        "TensorFlow-Tensor und führe die finale Summe aller Elemente durch. Gib das Ergebnis als String aus."
    ),
    agent=tensorflow_agent_2,
    context=[tensorflow_to_tensorflow_task],
    expected_output="Ein String, der das Endergebnis der finalen TensorFlow-Berechnung enthält."
)

# -----------------------------------------------------------------------------
# Helferfunktionen zur Simulation der Berechnungen
# -----------------------------------------------------------------------------

def run_torch_1_calc():
    """PyTorch -> PyTorch"""
    tensor_a = torch.tensor([10, 20, 30], dtype=torch.float32)
    tensor_b = torch.tensor([1, 1, 1], dtype=torch.float32)
    result = (tensor_a + tensor_b).tolist()
    print(f"\n--- PyTorch Agent 1: Vektoraddition abgeschlossen. Ergebnis: {result} ---")
    return {"data": result}

def run_torch_2_calc(context):
    """PyTorch -> TensorFlow"""
    input_data = context.get("data")
    if not input_data:
        print("❌ Fehler: Keine Daten von PyTorch 1 erhalten.")
        return {"data": []}
    
    tensor_in = torch.tensor(input_data, dtype=torch.float32)
    tensor_mult = torch.tensor([2, 2, 2], dtype=torch.float32)
    result = (tensor_in * tensor_mult).tolist()
    print(f"\n--- PyTorch Agent 2: Vektormultiplikation abgeschlossen. Ergebnis: {result} ---")
    return {"data": result}

def run_tensorflow_1_calc(context):
    """TensorFlow -> PyTorch"""
    input_data = context.get("data")
    if not input_data:
        print("❌ Fehler: Keine Daten von PyTorch 2 erhalten.")
        return {"data": 0}
        
    tf_tensor = tf.constant(input_data, dtype=tf.float32)
    total_sum = tf.reduce_sum(tf_tensor).numpy()
    print(f"\n--- TensorFlow Agent 1: Summe berechnet. Ergebnis: {total_sum} ---")
    return {"data": total_sum}

def run_torch_3_calc(context):
    """TensorFlow -> TensorFlow"""
    input_data = context.get("data")
    if not isinstance(input_data, (int, float)):
        print("❌ Fehler: Keine skalare Summe von TensorFlow 1 erhalten.")
        return {"data": []}

    torch_tensor = torch.tensor(input_data, dtype=torch.float32)
    result = (torch_tensor * 10).tolist()
    print(f"\n--- PyTorch Agent 3: Skalar-Multiplikation abgeschlossen. Ergebnis: {result} ---")
    return {"data": result}

def run_tensorflow_2_calc(context):
    """Final TensorFlow"""
    input_data = context.get("data")
    if not input_data:
        print("❌ Fehler: Keine Daten von PyTorch 3 erhalten.")
        return "Berechnung fehlgeschlagen."

    tf_tensor = tf.constant(input_data, dtype=tf.float32)
    final_result = tf.reduce_sum(tf_tensor).numpy()
    print(f"\n--- TensorFlow Agent 2: Finale Summe berechnet. Ergebnis: {final_result} ---")
    return f"Endgültiges Resultat: {final_result}"

# Überschreibe die `_execute` Methoden der Tasks, um die Funktionen aufzurufen
torch_to_torch_task._execute = run_torch_1_calc
torch_to_tensorflow_task._execute = lambda: run_torch_2_calc(torch_to_torch_task.output)
tensorflow_to_torch_task._execute = lambda: run_tensorflow_1_calc(torch_to_tensorflow_task.output)
tensorflow_to_tensorflow_task._execute = lambda: run_torch_3_calc(tensorflow_to_torch_task.output)
final_tensorflow_task._execute = lambda: run_tensorflow_2_calc(tensorflow_to_tensorflow_task.output)


# Erstelle die Crew
crew = Crew(
    agents=[torch_agent_1, torch_agent_2, tensorflow_agent_1, torch_agent_3, tensorflow_agent_2],
    tasks=[torch_to_torch_task, torch_to_tensorflow_task, tensorflow_to_torch_task, tensorflow_to_tensorflow_task, final_tensorflow_task],
    process=Process.sequential,
    verbose=2
)

# Starte den Workflow
print("\n=== CrewAI Workflow gestartet ===")
final_result = crew.kickoff()
print("\n=== Workflow abgeschlossen ===")
print(f"Endgültiges Resultat der Crew: {final_result}")
