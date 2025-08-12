import tensorflow as tf
import os
from .base_agent import BaseAgent

class KI_TensorFlow(BaseAgent):
    """
    KI-Agent, der ein TensorFlow-Modell verwendet und die Logik für
    Entscheidungsfindung und Kommunikation implementiert.
    """
    def __init__(self, name, model_name="ki_tensorflow_model_1.h5"):
        super().__init__(name, model_name)
        # Die Größe der Ein- und Ausgänge muss an das Spiel angepasst werden
        self.input_size = 50  # Beispielwert, muss an die Größe des GameState-Vektors angepasst werden
        self.output_size = 5  # Beispielwert: 5 mögliche Aktionen (z.B. Oben, Unten, Links, Rechts, Pass)
        
        self.load_model()
        if self.model is None:
            self._build_model()
            
    def _build_model(self):
        """
        Baut das neuronale Netz für TensorFlow auf.
        """
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(self.input_size,)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.output_size, activation='softmax')
        ])
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')
        print(f"INFO: Neues TensorFlow-Modell für '{self.name}' erstellt.")
        
    def choose_action(self, game_state):
        """
        Wählt basierend auf dem Spielzustand eine Aktion mit dem TensorFlow-Modell aus.
        """
        # 1. Posteingang checken und verarbeiten
        self.check_inbox()
        
        # 2. Spielzustand für die KI aufbereiten
        processed_state = self._preprocess_state(game_state)
        
        # 3. Das Modell nutzen, um eine Aktion vorherzusagen
        if self.model:
            # Die predict-Methode erwartet ein 2D-Array, daher reshape
            state_input = tf.constant(processed_state, dtype=tf.float32)[tf.newaxis, ...]
            action_probabilities = self.model.predict(state_input, verbose=0)[0]
            
            # Die Aktion mit der höchsten Wahrscheinlichkeit wählen
            action_index = tf.argmax(action_probabilities).numpy()
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
        """Speichert das TensorFlow-Modell im HDF5-Format."""
        if self.model:
            model_dir = self._get_model_directory()
            model_path = os.path.join(model_dir, self.model_name)
            self.model.save(model_path)
            print(f"INFO: TensorFlow-Modell für '{self.name}' gespeichert.")

    def load_model(self):
        """Lädt das TensorFlow-Modell."""
        model_dir = self._get_model_directory()
        model_path = os.path.join(model_dir, self.model_name)
        try:
            self.model = tf.keras.models.load_model(model_path)
            print(f"INFO: TensorFlow-Modell für '{self.name}' geladen.")
            return True
        except (IOError, ValueError, TypeError) as e:
            print(f"WARN: Konnte TensorFlow-Modell nicht laden: {e}")
            self.model = None
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
        # Zum Beispiel: Steht ein Gegner in der Nähe?
        return False

    def _map_action_index_to_action(self, index):
        """
        Übersetzt den Index aus dem Modell in eine spielbare Aktion.
        """
        # Beispiel: 0 -> Oben, 1 -> Unten, etc.
        actions = ['move_up', 'move_down', 'move_left', 'move_right', 'do_nothing']
        return actions[index]
