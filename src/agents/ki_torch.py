import torch
import torch.nn as nn
import os
import random
from .base_agent import BaseAgent
from src.game_logic.game_state import GameState # Importiere die GameState Klasse

class SimpleNet(nn.Module):
    """
    Ein einfaches neuronales Netzwerk für PyTorch, das die Aktionen des Agenten vorhersagt.
    """
    def __init__(self, input_size, output_size):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x

class KI_Torch(BaseAgent):
    """
    KI-Agent, der ein PyTorch-Modell verwendet und die Logik für
    Entscheidungsfindung und Kommunikation implementiert.
    """
    def __init__(self, name, model_name="ki_torch_model_1.pt"):
        super().__init__(name, model_name)
        # Die Größe der Ein- und Ausgänge muss an das Spiel angepasst werden
        self.input_size = 50  # Beispielwert, muss an die Größe des GameState-Vektors angepasst werden
        self.output_size = 5  # Beispielwert: 5 mögliche Aktionen (z.B. Oben, Unten, Links, Rechts, Pass)
        
        self.model = SimpleNet(self.input_size, self.output_size)
        self.load_model()
    
    def choose_action(self, game_state: GameState):
        """
        Wählt basierend auf dem Spielzustand eine Aktion mit dem PyTorch-Modell aus.
        """
        # 1. Posteingang checken und verarbeiten
        self.check_inbox()

        # 2. Prioritätenbasierte Entscheidungslogik
        
        # Priorität 1: Gesundheit niedrig? Suche Pille oder rufe um Hilfe
        if game_state.get_player_health(self.name) < 50:
            nearest_pill_pos = self._find_nearest_item(game_state, ['redpill', 'bluepill'])
            if nearest_pill_pos:
                # Hier könnte die KI die Aktion wählen, sich zur Pille zu bewegen
                print(f"WARN: Gesundheit niedrig! Bewege mich zu Pille bei {nearest_pill_pos}.")
                return self._get_move_action(game_state.get_player_position(self.name), nearest_pill_pos)
            
            # Wenn keine Pille in der Nähe, sende Hilferuf
            message = f"Hilfe! Meine Gesundheit ist niedrig bei {game_state.get_player_position(self.name)}."
            self.send_message(self.team_mate, message)

        # Priorität 2: Feind in der Nähe? Angreifen oder fliehen
        nearest_enemy_pos = self._find_nearest_enemy(game_state)
        if nearest_enemy_pos and self._is_enemy_in_range(game_state, nearest_enemy_pos):
            if game_state.get_player_health(self.name) > 75:
                print("INFO: Feind in Reichweite. Ich greife an!")
                return 'attack'
            else:
                print("WARN: Feind in Reichweite, Gesundheit zu niedrig. Ich fliehe!")
                return 'flee'

        # Priorität 3: Normales Spielverhalten (keine Bedrohung)
        fake_flag_pos = self._find_nearest_item(game_state, ['fake_flag_item'])
        if fake_flag_pos:
            print("INFO: Fake-Flag-Item gefunden. Bewege mich dorthin.")
            self._send_fake_flag_message(self.team_mate) # Diese Nachricht würde an den Gegner gehen
            return self._get_move_action(game_state.get_player_position(self.name), fake_flag_pos)

        # Wenn nichts Spezielles passiert, nutze das trainierte Modell für die nächste Aktion
        processed_state = self._preprocess_state(game_state)
        
        if self.model:
            state_tensor = torch.tensor(processed_state, dtype=torch.float32)
            
            with torch.no_grad():
                output = self.model(state_tensor)
            
            action_index = torch.argmax(output).item()
            action = self._map_action_index_to_action(action_index)
            return action
        else:
            return 'do_nothing'
    
    # --- Hilfsmethoden (Platzhalter) ---

    def _find_nearest_item(self, game_state: GameState, item_types):
        """Sucht das nächste Item eines bestimmten Typs."""
        return None

    def _find_nearest_enemy(self, game_state: GameState):
        """Sucht den nächsten Gegner."""
        return None

    def _is_enemy_in_range(self, game_state: GameState, enemy_pos):
        """Prüft, ob der Gegner in Angriffsreichweite ist."""
        return False
        
    def _get_move_action(self, current_pos, target_pos):
        """Leitet eine Bewegungsaktion von der aktuellen zur Zielposition ab."""
        return random.choice(['move_up', 'move_down', 'move_left', 'move_right'])

    def _preprocess_state(self, game_state):
        """
        Bereitet den GameState für die KI auf.
        """
        state_vector = [
            game_state.get_player_health(self.name),
            *game_state.get_player_position(self.name)
        ]
        return state_vector + [0] * (self.input_size - len(state_vector))

    def _map_action_index_to_action(self, index):
        """
        Übersetzt den Index aus dem Modell in eine spielbare Aktion.
        """
        actions = ['move_up', 'move_down', 'move_left', 'move_right', 'do_nothing']
        return actions[index]

    def save_model(self):
        # ... (Methoden bleiben unverändert)
        pass

    def load_model(self):
        # ... (Methoden bleiben unverändert)
        pass

    def _get_model_directory(self):
        # ... (Methoden bleiben unverändert)
        pass
