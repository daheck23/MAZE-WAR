import os
import json

class BaseAgent:
    """
    Basisklasse für alle KI-Agenten, die die Kernfunktionen wie
    Modellverwaltung und Kommunikation bereitstellt.
    """
    def __init__(self, name, model_name=None):
        self.name = name
        self.model = None
        self.model_name = model_name
        self.team_mate = None # Verweis auf den anderen Agenten im Team
        self.inbox = [] # Liste für empfangene Nachrichten

    def set_team_mate(self, team_mate_agent):
        """Weist dem Agenten ein Teammitglied zu."""
        self.team_mate = team_mate_agent
    
    def choose_action(self, game_state):
        """
        Wählt eine Aktion basierend auf dem aktuellen Spielzustand.
        Muss von erbenden Klassen überschrieben werden.
        """
        raise NotImplementedError("Die Methode 'choose_action' muss in einer erbenden Klasse implementiert werden.")

    def save_model(self):
        """Speichert den Lernfortschritt des Modells."""
        if self.model_name:
            model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, self.model_name)
            
            print(f"INFO: Speichere Modell '{self.model_name}' unter {model_path}")
            # Die eigentliche Speicherung muss in der erbenden Klasse implementiert werden
            # (z.B. model.save() für TensorFlow oder torch.save() für PyTorch).
            
    def load_model(self):
        """Lädt einen gespeicherten Lernfortschritt des Modells."""
        if self.model_name:
            model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
            model_path = os.path.join(model_dir, self.model_name)
            
            if os.path.exists(model_path):
                print(f"INFO: Lade Modell '{self.model_name}' von {model_path}")
                # Die eigentliche Ladung muss in der erbenden Klasse implementiert werden.
                return True
            else:
                print(f"INFO: Kein Modell '{self.model_name}' gefunden. Beginne neu.")
                return False
        return False

    # Kommunikationsmethoden
    def send_message(self, recipient, message):
        """Sendet eine Nachricht an ein anderes Teammitglied."""
        if recipient:
            recipient.inbox.append(message)
            print(f"INFO: '{self.name}' sendet Nachricht an '{recipient.name}': {message}")

    def check_inbox(self):
        """Verarbeitet alle neuen Nachrichten im Posteingang."""
        messages_to_process = self.inbox.copy()
        self.inbox.clear()
        
        for message in messages_to_process:
            self._process_message(message)

    def _process_message(self, message):
        """Interne Methode zur Verarbeitung einer einzelnen Nachricht."""
        # Hier wird die Logik implementiert, um auf eine Nachricht zu reagieren.
        # Beispiel: Wenn die Nachricht Flaggen-Koordinaten enthält, aktualisiere den Zustand.
        print(f"INFO: '{self.name}' verarbeitet Nachricht: {message}")
