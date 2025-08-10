import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGroupBox, QGridLayout, QLabel,
                             QComboBox, QPushButton, QCheckBox, QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from .game_window import GameWindow

class GameSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Spiel-Setup")
        self.setFixedSize(500, 500)
        
        self.main_layout = QVBoxLayout(self)
        self.map_list = self._load_map_list()
        self.teams_settings = {}

        self.init_ui()

    def _load_map_list(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        maps_path = os.path.join(base_path, 'assets', 'maps')
        
        if not os.path.exists(maps_path):
            return []
            
        all_files = os.listdir(maps_path)
        map_files = [f for f in all_files if f.endswith('.map')]
        
        return map_files

    def init_ui(self):
        map_groupbox = QGroupBox("Karte auswählen")
        map_layout = QHBoxLayout()
        self.map_combobox = QComboBox()
        self.map_combobox.addItems(self.map_list)
        map_layout.addWidget(self.map_combobox)
        map_groupbox.setLayout(map_layout)
        self.main_layout.addWidget(map_groupbox)

        team_groupbox = QGroupBox("Teams & KI-Typ auswählen")
        team_layout = QGridLayout()
        
        header_font = QFont("Arial", 10, QFont.Weight.Bold)
        team_layout.addWidget(QLabel("Team"), 0, 0, Qt.AlignmentFlag.AlignLeft)
        team_layout.addWidget(QLabel("Aktiv"), 0, 1, Qt.AlignmentFlag.AlignCenter)
        team_layout.addWidget(QLabel("KI-Typ"), 0, 2, Qt.AlignmentFlag.AlignLeft)
        
        teams = ["Team Red", "Team Blue", "Team Green", "Team Gold", "Team Pink"]
        
        for i, team_name in enumerate(teams):
            row = i + 1
            
            label = QLabel(team_name)
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            
            ai_type_combobox = QComboBox()
            ai_type_combobox.addItems(["KI (PyTorch)", "KI (TensorFlow)"])
            
            team_layout.addWidget(label, row, 0)
            team_layout.addWidget(checkbox, row, 1, Qt.AlignmentFlag.AlignCenter)
            team_layout.addWidget(ai_type_combobox, row, 2)

            self.teams_settings[team_name] = {
                'checkbox': checkbox,
                'ai_type_combobox': ai_type_combobox
            }

        team_groupbox.setLayout(team_layout)
        self.main_layout.addWidget(team_groupbox)

        button_layout = QHBoxLayout()
        start_button = QPushButton("Spiel starten")
        start_button.clicked.connect(self.start_game)
        
        cancel_button = QPushButton("Abbrechen")
        cancel_button.clicked.connect(self.close_and_return_to_start)
        
        button_layout.addWidget(start_button)
        button_layout.addWidget(cancel_button)
        self.main_layout.addLayout(button_layout)

    def _get_game_settings(self):
        game_settings = {
            'selected_map': self.map_combobox.currentText(),
            'teams': []
        }
        
        print(f"DEBUG: Ausgewählte Karte: '{game_settings['selected_map']}'")
        
        for team_name, widgets in self.teams_settings.items():
            if widgets['checkbox'].isChecked():
                team_info = {
                    'name': team_name,
                    'ai_type': widgets['ai_type_combobox'].currentText()
                }
                game_settings['teams'].append(team_info)
        
        return game_settings

    def start_game(self):
        game_settings = self._get_game_settings()
        
        if not game_settings['teams']:
            QMessageBox.warning(self, "Fehler", "Bitte wähle mindestens ein Team aus.")
            return

        self.game_window = GameWindow(
            map_name=game_settings['selected_map'],
            teams=game_settings['teams'],
            parent=self
        )
        self.game_window.show()
        self.hide()

    def close_and_return_to_start(self):
        self.parent().show()
        self.close()