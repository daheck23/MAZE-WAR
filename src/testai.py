import os
import sys

# Füge das src-Verzeichnis zum Python-Pfad hinzu, damit Imports funktionieren
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.ki_tensorflow import KI_TensorFlow
from src.agents.ki_torch import KI_Torch
from src.agents.base_agent import BaseAgent
from src.game_logic.game_state import GameState # Nutze die echte GameState Klasse

# --- Mock-Klassen zur Simulation ---

# Wir verwenden hier die echte GameState Klasse, da sie bereits die Werte
# für die Objekte enthält. Wir müssen nur die Player-Daten simulieren.
def create_mock_game_state(health, position, team_mates=None, opponents=None):
    """Erstellt eine simulierte Instanz der GameState Klasse."""
    map_data = ["###", "#.#", "###"] # Eine einfache Karte für den Test
    player_data = {
        "TestAgent": {"health": health, "position": position},
        "TeamMate": {"health": 100, "position": (1, 2)}
    }
    if opponents:
        player_data.update(opponents)
    
    return GameState(map_data, player_data)


# --- Testfunktionen für die KI-Agenten ---

def test_tensorflow_agent():
    print("## Test für KI_TensorFlow gestartet ##")
    ki_agent = KI_TensorFlow(name="TensorFlowAgent")
    sim_state = create_mock_game_state(health=75, position=(5, 8))
    
    # Simuliere die choose_action Methode
    action = ki_agent.choose_action(sim_state)
    
    print(f"-> Agent '{ki_agent.name}' wählt die Aktion: '{action}'")
    print("--------------------------------------\n")


def test_pytorch_agent():
    print("## Test für KI_Torch gestartet ##")
    ki_agent = KI_Torch(name="PyTorchAgent")
    sim_state = create_mock_game_state(health=75, position=(5, 8))
    
    # Simuliere die choose_action Methode
    action = ki_agent.choose_action(sim_state)
    
    print(f"-> Agent '{ki_agent.name}' wählt die Aktion: '{action}'")
    print("--------------------------------------\n")


def test_fake_flag_logic():
    print("## Test für Fake-Flag-Logik gestartet ##")
    
    # Simuliere zwei Teammitglieder (Agenten)
    team_member_a = KI_TensorFlow(name="TeamMemberA")
    team_member_b = KI_TensorFlow(name="TeamMemberB")
    
    # Weist ihnen gegenseitig ihren Teammate zu
    team_member_a.set_team_mate(team_member_b)
    team_member_b.set_team_mate(team_member_a)
    
    # Simuliere eine Situation, in der Agent A die Flagge gefunden hat (oder eine falsche Flagge)
    # Hier müsste normalerweise eine Aktion des Spiels die Nachricht auslösen.
    # Wir rufen die Methode direkt auf, um den Effekt zu testen.
    fake_flag_coords = (10, 20)
    
    print(f"-> {team_member_a.name} findet die Flagge bei {fake_flag_coords} und sendet eine Nachricht.")
    
    # In der echten Logik würde eine Funktion im Spiel die Nachricht erzeugen.
    # Wir senden hier eine beispielhafte Nachricht, wie sie von CrewAI generiert werden könnte.
    message_content = f"Ich habe die Flagge bei den Koordinaten {fake_flag_coords} gefunden. Wir müssen uns dorthin bewegen."
    team_member_a.send_message(team_member_a.team_mate, message_content)
    
    # Jetzt verarbeitet Agent B seinen Posteingang
    print(f"-> {team_member_b.name} checkt den Posteingang und verarbeitet die Nachricht.")
    team_member_b.check_inbox()
    
    print("--------------------------------------\n")


if __name__ == '__main__':
    test_tensorflow_agent()
    test_pytorch_agent()
    test_fake_flag_logic()
