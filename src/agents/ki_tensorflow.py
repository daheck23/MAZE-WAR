import os
import json
import numpy as np
import tensorflow as tf
from src.agents.base_agent import BaseAgent # <-- Hier wurde der Import-Pfad korrigiert
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

class KI_TensorFlow(BaseAgent):
    """
    Ein KI-Agent, der auf einem TensorFlow/Keras-Modell basiert.
    """
    def __init__(self, name, model_name=None, team_mate=None, map_data=None):
        super().__init__(name, model_name=model_name, team_mate=team_mate, map_data=map_data)
        self.state_size = 100 # Beispielgröße, muss an den Spielzustand angepasst werden
        self.action_size = 5  # Beispielgröße: Oben, Unten, Links, Rechts, Nichts
        self.model = self._build_model()
        
        # Lade ein gespeichertes Modell, falls vorhanden
        if model_name and os.path.exists(f'models/{model_name}'):
            self.model.load_weights(f'models/{model_name}')

    def _build_model(self):
        """Erstellt das neuronale Netzwerk."""
        model = Sequential([
            Dense(64, input_shape=(self.state_size,), activation='relu'),
            Dense(64, activation='relu'),
            Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
        return model

    def choose_action(self, game_state):
        """
        Wählt basierend auf dem Spielzustand eine Aktion aus.
        """
        # Annahme: game_state ist ein NumPy-Array oder kann in eines umgewandelt werden
        if game_state.shape != (1, self.state_size):
            game_state = np.reshape(game_state, [1, self.state_size])

        # Nutze das Modell, um eine Aktion vorherzusagen
        q_values = self.model.predict(game_state)
        action_index = np.argmax(q_values[0])
        
        # Konvertiere den Index zurück in eine Spielaktion
        # Diese Logik muss je nach den Aktionen in deinem Spiel angepasst werden
        actions = ['up', 'down', 'left', 'right', 'stay']
        return actions[action_index]

    def save_model(self, file_path):
        """Speichert das Modell."""
        self.model.save_weights(file_path)
        print(f"TensorFlow-Modell von {self.name} unter '{file_path}' gespeichert.")

    def load_model(self, file_path):
        """Lädt ein gespeichertes Modell."""
        if os.path.exists(file_path):
            self.model.load_weights(file_path)
            print(f"TensorFlow-Modell von {self.name} unter '{file_path}' geladen.")
        else:
            print(f"Warnung: Modell-Datei '{file_path}' nicht gefunden.")