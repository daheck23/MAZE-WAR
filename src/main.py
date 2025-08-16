import sys
import os
from PyQt6.QtWidgets import QApplication
# Korrigierter Import-Pfad
from .gui.start_dialog import StartDialog

def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.join(base_dir, os.pardir))
    except FileNotFoundError:
        print("FEHLER: Konnte das Basisverzeichnis nicht finden. Überprüfe die Dateistruktur.")
        return

    app = QApplication(sys.argv)
    
    start_dialog = StartDialog()
    start_dialog.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()