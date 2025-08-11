import tensorflow as tf
from .base_agent import BaseAgent

class KI_TensorFlow(BaseAgent):
    """
    KI-Agent, der ein TensorFlow-Modell verwendet.
    """
    def __init__(self, name, model_name="ki_tensorflow_model_1.h5"):
        super().__init__(name, model_name)
        self.load_model()
        if self.model is None:
            self._build_model()
            
    def _build_model(self):
        """
        Baut das neuronale Netz für TensorFlow auf.
        Hier definieren wir die Architektur des Modells.
        """
        # Beispielarchitektur (muss später an die Spielanforderungen angepasst werden)
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(...)), # Input-Dimension anpassen
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(..., activation='softmax') # Output-Dimension anpassen
        ])
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')
        print(f"INFO: Neues TensorFlow-Modell für '{self.name}' erstellt.")
        
    def choose_action(self, game_state):
        """
        Wählt basierend auf dem Spielzustand eine Aktion mit dem TensorFlow-Modell aus.
        """
        # Hier wird der game_state in eine für das Modell verständliche Form umgewandelt.
        # Beispiel: state = self._preprocess_state(game_state)
        # action_probabilities = self.model.predict(state)
        # action = self._choose_from_probabilities(action_probabilities)
        # return action
        pass

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
        except (IOError, ValueError) as e:
            print(f"WARN: Konnte TensorFlow-Modell nicht laden: {e}")
            self.model = None
            return False

    def _get_model_directory(self):
        """Hilfsfunktion, um den Pfad zum models-Ordner zu erhalten."""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))
