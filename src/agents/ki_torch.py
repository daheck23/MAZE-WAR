import torch
import torch.nn as nn
import torch.optim as optim
import os
from .base_agent import BaseAgent

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
    
    def choose_action(self, game_state):
        """
        Wählt basierend auf dem Spielzustand eine Aktion mit dem PyTorch-Modell aus.
        """
        # 1. Posteingang checken und verarbeiten
        self.check_inbox()

        # 2. Spielzustand für die KI aufbereiten
        processed_state = self._preprocess_state(game_state)

        # 3. Das Modell nutzen, um eine Aktion vorherzusagen
        if self.model:
            # Zustand in einen PyTorch-Tensor umwandeln
            state_tensor = torch.tensor(processed_state, dtype=torch.float32)
            
            with torch.no_grad():
                output = self.model(state_tensor)
            
            # Die Aktion mit der höchsten Wahrscheinlichkeit wählen
            action_index = torch.argmax(output).item()
            action = self._map_action_index_to_action(action_index)

            # Beispielhafte Kommunikationslogik: Wenn angegriffen, sende eine Nachricht
            if self._is_under_attack(game_state):
                message = f"Hilfe! Ich werde bei {game_state.get_player_position(self.name)} angegriffen!"
                self.send_message(self.team_mate, message)
                
            return action
        else:
            # Fallback, falls das Modell nicht geladen wurde
            return 'do_nothing'

    def save_model(self):
        """Speichert das PyTorch-Modell."""
        if self.model:
            model_dir = self._get_model_directory()
            model_path = os.path.join(model_dir, self.model_name)
            torch.save(self.model.state_dict(), model_path)
            print(f"INFO: PyTorch-Modell für '{self.name}' gespeichert.")

    def load_model(self):
        """Lädt ein gespeichertes PyTorch-Modell."""
        model_dir = self._get_model_directory()
        model_path = os.path.join(model_dir, self.model_name)
        try:
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval()  # Setzt das Modell in den Evaluierungsmodus
            print(f"INFO: PyTorch-Modell für '{self.name}' geladen.")
            return True
        except (IOError, ValueError, RuntimeError) as e:
            print(f"WARN: Konnte PyTorch-Modell nicht laden: {e}")
            self.model = SimpleNet(self.input_size, self.output_size)
            return False

    def _get_model_directory(self):
        """Hilfsfunktion, um den Pfad zum models-Ordner zu erhalten."""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))

    def _preprocess_state(self, game_state):
        """
        Bereitet den GameState für die KI auf.
        Muss noch an die genaue Struktur angepasst werden.
        """
        # Beispiel: Eine flache Liste von Werten
        state_vector = [
            game_state.get_player_health(self.name),
            *game_state.get_player_position(self.name)
            # ... weitere relevante Daten
        ]
        return state_vector

    def _is_under_attack(self, game_state):
        """
        Prüft, ob der Agent angegriffen wird (Platzhalter).
        """
        # Hier würde man Logik einfügen, um den Spielzustand zu überprüfen.
        return False

    def _map_action_index_to_action(self, index):
        """
        Übersetzt den Index aus dem Modell in eine spielbare Aktion.
        """
        # Beispiel: 0 -> Oben, 1 -> Unten, etc.
        actions = ['move_up', 'move_down', 'move_left', 'move_right', 'do_nothing']
        return actions[index]
