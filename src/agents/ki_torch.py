import torch
import torch.nn as nn
from .base_agent import BaseAgent

class SimpleNet(nn.Module):
    """
    Ein einfaches neuronales Netzwerk für PyTorch.
    """
    def __init__(self, input_size, output_size):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

class KI_Torch(BaseAgent):
    """
    KI-Agent, der ein PyTorch-Modell verwendet.
    """
    def __init__(self, name, model_name="ki_torch_model_1.pt"):
        super().__init__(name, model_name)
        # Die Größe der Ein- und Ausgänge muss an das Spiel angepasst werden
        self.input_size = 10 
        self.output_size = 4 
        self.model = SimpleNet(self.input_size, self.output_size)
        
        self.load_model()

    def choose_action(self, game_state):
        """
        Wählt basierend auf dem Spielzustand eine Aktion mit dem PyTorch-Modell aus.
        """
        # Hier wird der game_state in einen PyTorch-Tensor umgewandelt.
        # Beispiel: state_tensor = self._preprocess_state(game_state)
        # with torch.no_grad():
        #     output = self.model(state_tensor)
        # action = torch.argmax(output).item()
        # return action
        pass

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
            # Die Modellarchitektur muss beim Laden bekannt sein
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval() # Setzt das Modell in den Evaluierungsmodus
            print(f"INFO: PyTorch-Modell für '{self.name}' geladen.")
            return True
        except (IOError, ValueError) as e:
            print(f"WARN: Konnte PyTorch-Modell nicht laden: {e}")
            self.model = SimpleNet(self.input_size, self.output_size)
            return False
            
    def _get_model_directory(self):
        """Hilfsfunktion, um den Pfad zum models-Ordner zu erhalten."""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))
