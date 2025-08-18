#
# Datei: test_torch.py
#
# Dieses Skript testet die Installation von PyTorch.
#

import torch

def test_torch():
    """
    Führt einen einfachen Test für PyTorch durch.
    """
    try:
        # Gib die installierte PyTorch-Version aus.
        print("--- Teste PyTorch-Installation ---")
        print(f"PyTorch Version: {torch.__version__}")

        # Erstelle einen einfachen Tensor (das ist wie ein NumPy-Array, aber für PyTorch optimiert).
        x = torch.tensor([1, 2, 3])
        y = torch.tensor([4, 5, 6])
        
        # Führe eine einfache Operation aus: Addition.
        z = x + y

        # Gib die Ergebnisse aus.
        print(f"Erster Tensor (x): {x}")
        print(f"Zweiter Tensor (y): {y}")
        print(f"Ergebnis der Addition (z): {z}")

        print("PyTorch-Test erfolgreich.")

    except ImportError:
        print("FEHLER: PyTorch ist nicht installiert. Bitte installieren Sie es mit 'pip install torch'.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == '__main__':
    test_torch()

print("\n" + "="*50 + "\n") # Trennlinie zwischen den beiden Skripten

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
