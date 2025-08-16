import sys
import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QAbstractItemView,
    QLabel, QLineEdit, QSpinBox, QFormLayout, QComboBox, QCheckBox, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.game_logic.game_engine import GameEngine

class GameSetupDialog(QDialog):
    def __init__(self, start_dialog):
        super().__init__()
        self.start_dialog = start_dialog
        self.game_engine = None
        self.teams_info = []

        # Fenster-Eigenschaften
        self.setWindowTitle("Spiel einrichten")
        self.setFixedSize(600, 500)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setStyleSheet("background-color: #333333; color: white;")
        
        # Haupt-Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(15)
        
        # Titel-Label
        title_font = QFont("Arial", 20, QFont.Weight.Bold)
        title_label = QLabel("Spiel einrichten")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)

        # ------------------
        # 1. Karten-Auswahl
        # ------------------
        self.map_group_box = QGroupBox("Wähle eine Karte aus")
        self.map_group_box.setStyleSheet("color: white; border: 1px solid #555555; border-radius: 5px;")
        self.map_group_layout = QVBoxLayout(self.map_group_box)
        self.map_list = QListWidget()
        self.map_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.map_list.setStyleSheet("background-color: #555555; border: 1px solid #777777; color: white;")
        self.map_group_layout.addWidget(self.map_list)
        self._load_maps()
        self.main_layout.addWidget(self.map_group_box)

        # ------------------
        # 2. Teams-Konfiguration
        # ------------------
        self.teams_group_box = QGroupBox("Team-Einstellungen")
        self.teams_group_box.setStyleSheet("color: white; border: 1px solid #555555; border-radius: 5px;")
        self.teams_layout = QFormLayout(self.teams_group_box)
        self.team_checkboxes = []
        self.team_models = []

        # Team-Namen aktualisiert
        team_names = ["Team Rot", "Team Blau", "Team Grün", "Team Pink", "Team Gold"]
        for i, team_name in enumerate(team_names):
            # H-Box für jedes Team
            team_h_layout = QHBoxLayout()
            
            # Checkbox für das Team
            team_checkbox = QCheckBox(team_name)
            team_checkbox.setChecked(True) # Standardmäßig alle Teams ausgewählt
            team_checkbox.setStyleSheet("color: white;")
            self.team_checkboxes.append(team_checkbox)
            team_h_layout.addWidget(team_checkbox)

            # Auswahl für das AI-Modell
            ai_model_selection = QComboBox()
            ai_model_selection.addItems(["Torch", "TensorFlow"])
            ai_model_selection.setStyleSheet("background-color: #555555; color: white;")
            self.team_models.append(ai_model_selection)
            team_h_layout.addWidget(ai_model_selection)
            
            # Füge das H-Layout zur Form hinzu
            self.teams_layout.addRow(team_h_layout)

        self.main_layout.addWidget(self.teams_group_box)

        # ------------------
        # 3. Aktions-Buttons
        # ------------------
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.start_button = QPushButton("Starten")
        self.start_button.setFont(QFont("Arial", 14))
        self.start_button.setFixedSize(120, 30)
        self.start_button.setStyleSheet("background-color: #555555; border-radius: 10px; color: white;")
        self.start_button.clicked.connect(self.start_game)
        
        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setFont(QFont("Arial", 14))
        self.cancel_button.setFixedSize(120, 30)
        self.cancel_button.setStyleSheet("background-color: #AA0000; border-radius: 10px; color: white;")
        self.cancel_button.clicked.connect(self.cancel_game)
        
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.cancel_button)
        
        self.main_layout.addLayout(self.button_layout)
        
    def _load_maps(self):
        """Lädt die .map-Dateien aus dem assets-Ordner und fügt sie der Liste hinzu."""
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            maps_path = os.path.abspath(os.path.join(base_path, os.pardir, 'assets', 'maps'))
            
            if not os.path.exists(maps_path):
                print(f"FEHLER: 'maps'-Ordner nicht gefunden unter {maps_path}")
                return

            for filename in os.listdir(maps_path):
                if filename.endswith('.map'):
                    self.map_list.addItem(filename)
            
            if self.map_list.count() > 0:
                self.map_list.setCurrentRow(0)

        except Exception as e:
            print(f"SCHWERER FEHLER: Ein unerwarteter Fehler ist beim Laden der Karten aufgetreten.")
            print(f"Fehlertyp: {type(e).__name__}")
            print(f"Fehlermeldung: {e}")
            
    def start_game(self):
        """Sammelt die ausgewählten Einstellungen und startet das Spiel."""
        selected_map_items = self.map_list.selectedItems()
        if not selected_map_items:
            print("Keine Karte ausgewählt. Spielstart abgebrochen.")
            return

        map_name = selected_map_items[0].text()
        
        # Erstelle eine Liste der ausgewählten Teams und ihrer AI-Modelle
        self.teams_info = []
        for i, checkbox in enumerate(self.team_checkboxes):
            if checkbox.isChecked():
                team_name = checkbox.text()
                ai_model = self.team_models[i].currentText()
                # Für die Demonstration setzen wir die Anzahl der Soldaten auf 1
                self.teams_info.append({'name': team_name, 'soldiers': 1, 'ai_model': ai_model})
        
        if not self.teams_info:
            print("Keine Teams ausgewählt. Spielstart abgebrochen.")
            return

        self.hide()
        
        self.game_engine = GameEngine(self.start_dialog)
        self.game_engine.start_game(map_name, self.teams_info)
        
    def cancel_game(self):
        """Bricht die Einrichtung ab und kehrt zum Startdialog zurück."""
        self.close()
        self.start_dialog.show()
