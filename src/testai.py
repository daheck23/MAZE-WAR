import os
import sys

# Füge das src-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.ki_tensorflow import KI_TensorFlow
from src.agents.ki_torch import KI_Torch
from src.agents.base_agent import BaseAgent
from src.game_logic.game_state import GameState

# --- Mock-Klassen zur Simulation ---

# Wir verwenden hier die echte GameState Klasse und simulieren nur die Daten
def create_mock_game_state(map_data, player_health, player_pos, items, enemies):
    """Erstellt eine simulierte Instanz der GameState Klasse."""
    player_data = {
        "TestAgent": {"health": player_health, "position": player_pos},
        "TeamMate": {"health": 100, "position": (1, 2)}
    }
    enemy_data = {f"Enemy{i}": {"health": 100, "position": pos} for i, pos in enumerate(enemies)}
    player_data.update(enemy_data)
    
    # Simuliere Items auf der Karte, indem wir sie in die map_data einfügen
    mock_map = [list(row) for row in map_data]
    for pos, item_char in items.items():
        mock_map[pos[1]][pos[0]] = item_char
    
    final_map = ["".join(row) for row in mock_map]
    
    return GameState(final_map, player_data)


# --- Testfunktionen für die KI-Agenten ---

def test_ki_agent_logic(ki_class, agent_name):
    print(f"## Test für {agent_name} gestartet ##")
    ki_agent = ki_class(name=agent_name)
    
    # Szenario 1: Normales Spielverhalten (keine Bedrohung)
    print("Szenario 1: Keine Bedrohung. Erwarte normale Bewegung oder 'do_nothing'.")
    map_data = ["...", "...", "..." ]
    sim_state = create_mock_game_state(map_data, player_health=100, player_pos=(0, 0), items={}, enemies=[])
    action = ki_agent.choose_action(sim_state)
    print(f"-> Agent wählt Aktion: '{action}'")
    
    # Szenario 2: Gesundheit niedrig, suche Pille
    print("\nSzenario 2: Gesundheit niedrig. Erwarte, dass Agent nach Pille sucht.")
    map_data = ["p..", "...", "..." ] # 'p' für Pille
    sim_state = create_mock_game_state(map_data, player_health=40, player_pos=(2, 2), items={(0,0): 'p'}, enemies=[])
    action = ki_agent.choose_action(sim_state)
    print(f"-> Agent wählt Aktion: '{action}'")
    
    # Szenario 3: Fake Flag Item gefunden
    print("\nSzenario 3: Fake Flag Item gefunden. Erwarte, dass Agent die Nachricht sendet.")
    map_data = ["...", "F..", "..." ] # 'F' für fake_flag_item
    sim_state = create_mock_game_state(map_data, player_health=100, player_pos=(0, 0), items={(1,0): 'F'}, enemies=[])
    
    # Simuliere gegnerischen Agenten, damit die Nachricht irgendwo ankommt
    opponent = BaseAgent(name="Opponent")
    ki_agent.team_mate = opponent
    
    action = ki_agent.choose_action(sim_state)
    print(f"-> Agent wählt Aktion: '{action}'")
    print("--------------------------------------\n")


if __name__ == '__main__':
    test_ki_agent_logic(KI_TensorFlow, "TensorFlowAgent")
    test_ki_agent_logic(KI_Torch, "PyTorchAgent")
