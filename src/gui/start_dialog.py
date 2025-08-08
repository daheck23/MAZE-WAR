import sys
import traceback
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from game_logic.maze_generator import MazeGenerator
from gui.game_window import GameWindow
from gui.map_settings_dialog import MapSettingsDialog
from gui.game_setup_dialog import GameSetupDialog
import numpy as np

class StartDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAZE-AI War v1.0")
        self.setGeometry(100, 100, 600, 800)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, True)
        self.map_settings_dialog = None
        self.game_window = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Titel
        title_label = QLabel("MAZE-AI War")
        title_font = QFont("Arial", 36, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Platzhalter für das Bild
        image_label = QLabel()
        image_label.setFixedSize(400, 400)
        image_label.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setText("Platzhalter für Bild")
        layout.addWidget(image_label)

        # Buttons
        self.start_button = QPushButton("Spiel starten")
        self.start_button.setFixedSize(200, 50)
        self.start_button.setFont(QFont("Arial", 14))
        self.start_button.clicked.connect(self._on_start_game_clicked)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.generate_map_button = QPushButton("Map generieren")
        self.generate_map_button.setFixedSize(200, 50)
        self.generate_map_button.setFont(QFont("Arial", 14))
        self.generate_map_button.clicked.connect(self._on_generate_map_clicked)
        layout.addWidget(self.generate_map_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.settings_button = QPushButton("Einstellungen")
        self.settings_button.setFixedSize(200, 50)
        self.settings_button.setFont(QFont("Arial", 14))
        layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.quit_button = QPushButton("Beenden")
        self.quit_button.setFixedSize(200, 50)
        self.quit_button.setFont(QFont("Arial", 14))
        self.quit_button.clicked.connect(self.close_application)
        layout.addWidget(self.quit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def _on_generate_map_clicked(self):
        self.map_settings_dialog = MapSettingsDialog()
        self.map_settings_dialog.show()

    def _on_start_game_clicked(self):
        self.game_setup_dialog = GameSetupDialog(parent=self)
        self.hide()

        if self.game_setup_dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                # Holen der ausgewählten Daten
                selected_teams = self.game_setup_dialog.selected_teams
                map_name = self.game_setup_dialog.selected_map
                
                # Labyrinth generieren oder laden (temporär)
                # Hier muss später die Logik zum Laden der Map aus der Datei hin
                maze_gen = MazeGenerator(width=30, height=20)
                maze_data = maze_gen.generate()
                
                # GameWindow als unabhängiges Fenster erstellen
                self.game_window = GameWindow(maze_data, team_count=len(selected_teams), start_dialog_ref=self)
                self.game_window.show()
            except Exception as e:
                # Zeigt eine Fehlermeldung, wenn etwas schiefgeht
                error_message = f"Ein unerwarteter Fehler ist aufgetreten:\n\n{e}\n\nTraceback:\n{traceback.format_exc()}"
                QMessageBox.critical(self, "Fehler beim Starten des Spiels", error_message)
                self.show() # StartDialog wieder anzeigen
        else:
            # Wenn der Dialog abgebrochen wird, Startdialog wieder anzeigen
            self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Beenden",
            "Möchtest du das Programm wirklich schließen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def close_application(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = StartDialog()
    dialog.show()
    sys.exit(app.exec())