#
# Datei: test_tensorflow.py
#
# Dieses Skript testet die Installation von TensorFlow.
#

import tensorflow as tf

def test_tensorflow():
    """
    Führt einen einfachen Test für TensorFlow durch.
    """
    try:
        # Gib die installierte TensorFlow-Version aus.
        print("--- Teste TensorFlow-Installation ---")
        print(f"TensorFlow Version: {tf.__version__}")

        # Erstelle einen einfachen Tensor (das ist der grundlegende Datencontainer in TensorFlow).
        a = tf.constant([[1, 2], [3, 4]])
        b = tf.constant([[5, 6], [7, 8]])
        
        # Führe eine einfache Operation aus: Matrix-Multiplikation.
        c = tf.matmul(a, b)
        
        # Gib die Ergebnisse aus.
        print(f"Erster Tensor (a):\n{a}")
        print(f"Zweiter Tensor (b):\n{b}")
        print(f"Ergebnis der Multiplikation (c):\n{c}")

        print("TensorFlow-Test erfolgreich.")

    except ImportError:
        print("FEHLER: TensorFlow ist nicht installiert. Bitte installieren Sie es mit 'pip install tensorflow'.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == '__main__':
    test_tensorflow()
