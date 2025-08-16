import sys
import os
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Wichtige Korrekturen: Die korrekten Dialoge importieren
try:
    from .game_setup_dialog import GameSetupDialog
    from .map_settings_dialog import MapSettingsDialog
    from .settings_dialog import SettingsDialog
    print("DEBUG: Alle Importe in start_dialog.py erfolgreich.")
except ImportError as e:
    print(f"SCHWERER FEHLER: Import-Fehler in start_dialog.py")
    print(f"Fehlermeldung: {e}")
    sys.exit(1)

class StartDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.game_setup_dialog = None
        self.setWindowTitle("MAZE-AI WAR")
        self.setFixedSize(400, 300)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setStyleSheet("background-color: #333333; color: white;")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.init_ui()

    def init_ui(self):
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label = QLabel("MAZE-AI WAR")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        self.main_layout.addSpacing(40)

        start_button = QPushButton("Spiel starten")
        start_button.setFont(QFont("Arial", 14))
        start_button.setFixedSize(200, 40)
        start_button.setStyleSheet("background-color: #555555; border-radius: 10px;")
        start_button.clicked.connect(self.open_game_setup)
        self.main_layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        generate_map_button = QPushButton("Karte generieren")
        generate_map_button.setFont(QFont("Arial", 14))
        generate_map_button.setFixedSize(200, 40)
        generate_map_button.setStyleSheet("background-color: #555555; border-radius: 10px;")
        generate_map_button.clicked.connect(self.open_map_settings)
        self.main_layout.addWidget(generate_map_button, alignment=Qt.AlignmentFlag.AlignCenter)

        settings_button = QPushButton("Einstellungen")
        settings_button.setFont(QFont("Arial", 14))
        settings_button.setFixedSize(200, 40)
        settings_button.setStyleSheet("background-color: #555555; border-radius: 10px;")
        settings_button.clicked.connect(self.open_settings)
        self.main_layout.addWidget(settings_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addSpacing(40)

        quit_button = QPushButton("Beenden")
        quit_button.setFont(QFont("Arial", 14))
        quit_button.setFixedSize(200, 40)
        quit_button.setStyleSheet("background-color: #AA0000; border-radius: 10px;")
        quit_button.clicked.connect(self.close)
        self.main_layout.addWidget(quit_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def open_game_setup(self):
        self.game_setup_dialog = GameSetupDialog(self)
        self.game_setup_dialog.show()
        self.hide()

    def open_map_settings(self):
        map_settings_dialog = MapSettingsDialog(self)
        map_settings_dialog.show()
        self.hide()

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.show()
        self.hide()
