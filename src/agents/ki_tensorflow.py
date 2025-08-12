import tensorflow as tf
import os
import random
from .base_agent import BaseAgent
from src.game_logic.game_state import GameState # Importiere die GameState Klasse

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
        
    def choose_action(self, game_state: GameState):
        """
        Wählt basierend auf dem Spielzustand eine Aktion mit dem TensorFlow-Modell aus.
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
                # Beispiel: Aktion zur Bewegung zur Pille ableiten
                return self._get_move_action(game_state.get_player_position(self.name), nearest_pill_pos)
            
            # Wenn keine Pille in der Nähe, sende Hilferuf
            message = f"Hilfe! Meine Gesundheit ist niedrig bei {game_state.get_player_position(self.name)}."
            self.send_message(self.team_mate, message)

        # Priorität 2: Feind in der Nähe? Angreifen oder fliehen
        nearest_enemy_pos = self._find_nearest_enemy(game_state)
        if nearest_enemy_pos and self._is_enemy_in_range(game_state, nearest_enemy_pos):
            # Angreifen, wenn die eigene Gesundheit hoch genug ist
            if game_state.get_player_health(self.name) > 75:
                print("INFO: Feind in Reichweite. Ich greife an!")
                # Hier würde die Aktion 'angreifen' gewählt werden
                return 'attack'
            else:
                # Fliehen, wenn die Gesundheit niedrig ist
                print("WARN: Feind in Reichweite, Gesundheit zu niedrig. Ich fliehe!")
                return 'flee'

        # Priorität 3: Normales Spielverhalten (keine Bedrohung)
        
        # Suche nach einem "fake_flag_item"
        fake_flag_pos = self._find_nearest_item(game_state, ['fake_flag_item'])
        if fake_flag_pos:
            print("INFO: Fake-Flag-Item gefunden. Bewege mich dorthin.")
            # Die KI bewegt sich zum Item und sendet dann eine falsche Nachricht
            self._send_fake_flag_message(self.team_mate) # Diese Nachricht würde an den Gegner gehen
            return self._get_move_action(game_state.get_player_position(self.name), fake_flag_pos)

        # Wenn nichts Spezielles passiert, nutze das trainierte Modell für die nächste Aktion
        processed_state = self._preprocess_state(game_state)
        
        if self.model:
            state_input = tf.constant(processed_state, dtype=tf.float32)[tf.newaxis, ...]
            action_probabilities = self.model.predict(state_input, verbose=0)[0]
            action_index = tf.argmax(action_probabilities).numpy()
            action = self._map_action_index_to_action(action_index)
            return action
        else:
            return 'do_nothing'

    # --- Hilfsmethoden (Platzhalter) ---

    def _find_nearest_item(self, game_state: GameState, item_types):
        """Sucht das nächste Item eines bestimmten Typs."""
        # TODO: Implementiere die Logik, um die Koordin
