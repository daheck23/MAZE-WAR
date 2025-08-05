import sys
from PyQt6.QtWidgets import QApplication
from gui.start_dialog import StartDialog

def main():
    app = QApplication(sys.argv)
    start_dialog = StartDialog()
    start_dialog.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
