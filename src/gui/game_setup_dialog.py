import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QPushButton, QComboBox,
    QLabel, QFormLayout, QMessageBox, QHBoxLayout, QWidget
)
from PyQt6.QtCore import Qt
from game_logic.maze_generator import MazeGenerator
from gui.game_window import GameWindow

class GameSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Spiel starten")
        self.setFixedSize(500, 400)
        self.team_combos = []
        self.ki_combos = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_layout = QFormLayout()

        # Map-Auswahl
        self.map_combo = QComboBox()
        self.load_maps()
        form_layout.addRow(QLabel("Karte auswählen:"), self.map_combo)
        
        main_layout.addLayout(form_layout)
        
        main_layout.addSpacing(20)

        # Team- und KI-Auswahl
        team_options = ["No", "Team Red", "Team Blue", "Team Green", "Team Pink", "Team Gold"]
        ki_options = ["KI 1 (PyTorch)", "KI 2 (TensorFlow)"]

        for i in range(5):
            team_layout = QHBoxLayout()
            
            team_label = QLabel(f"Team {i + 1}:")
            team_combo = QComboBox()
            team_combo.addItems(team_options)
            self.team_combos.append(team_combo)

            ki_combo = QComboBox()
            ki_combo.addItems(ki_options)
            self.ki_combos.append(ki_combo)
            
            team_layout.addWidget(team_label)
            team_layout.addWidget(team_combo)
            team_layout.addWidget(ki_combo)
            
            main_layout.addLayout(team_layout)

        # Buttons
        button_layout = QVBoxLayout()
        self.start_game_button = QPushButton("Starten")
        self.start_game_button.clicked.connect(self._on_start_game)
        button_layout.addWidget(self.start_game_button)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self._on_cancel)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def load_maps(self):
        maps_dir = "assets/maps"
        if not os.path.exists(maps_dir):
            os.makedirs(maps_dir)
            return

        map_files = [f for f in os.listdir(maps_dir) if f.endswith(".map")]
        self.map_combo.addItems(map_files)

    def _validate_teams(self):
        selected_teams = [combo.currentText() for combo in self.team_combos if combo.currentText() != "No"]
        
        if len(selected_teams) < 2:
            QMessageBox.warning(self, "Fehler", "Es müssen mindestens 2 Teams ausgewählt werden.")
            return False

        if len(selected_teams) != len(set(selected_teams)):
            QMessageBox.warning(self, "Fehler", "Jedes Team darf nur einmal ausgewählt werden.")
            return False

        return True

    def _on_start_game(self):
        if not self._validate_teams():
            return
        
        # Holen der ausgewählten Teams und KIs
        selected_teams = [combo.currentText() for combo in self.team_combos if combo.currentText() != "No"]
        selected_ki_types = [
            self.ki_combos[i].currentText() 
            for i, team in enumerate(self.team_combos) 
            if team.currentText() != "No"
        ]
        
        # Temporäre Labyrinth-Generierung für die Ansicht (sollte später von der ausgewählten Map geladen werden)
        maze_gen = MazeGenerator(width=30, height=20)
        maze_data = maze_gen.generate()
        
        self.accept()
        self.close()
        
        game_window = GameWindow(maze_data, team_count=len(selected_teams), parent=self.parent)
        game_window.show()

    def _on_cancel(self):
        self.reject()
        self.close()
        if self.parent:
            self.parent.show()
