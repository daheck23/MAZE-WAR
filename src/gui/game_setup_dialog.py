import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QPushButton, QSpinBox, QComboBox,
    QLabel, QFormLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from game_logic.maze_generator import MazeGenerator
from gui.game_window import GameWindow

class GameSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Spiel starten")
        self.setFixedSize(400, 300)
        self.team_spinbox = QSpinBox()
        self.team_spinbox.setMinimum(2)
        self.team_spinbox.setMaximum(5)
        self.team_spinbox.valueChanged.connect(self.update_team_selection)
        self.ki_selectors = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_layout = QFormLayout()
        
        # Team-Anzahl
        form_layout.addRow(QLabel("Anzahl der Teams (2-5):"), self.team_spinbox)
        main_layout.addLayout(form_layout)

        # Dynamische KI-Auswahl
        self.ki_selection_layout = QVBoxLayout()
        main_layout.addLayout(self.ki_selection_layout)
        self.update_team_selection(self.team_spinbox.value())

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

    def update_team_selection(self, num_teams):
        # Entferne alte Widgets
        for i in reversed(range(self.ki_selection_layout.count())): 
            widget = self.ki_selection_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        self.ki_selectors = []
        for i in range(num_teams):
            ki_selector = QComboBox()
            ki_selector.addItem("KI 1 (PyTorch)")
            ki_selector.addItem("KI 2 (TensorFlow)")
            self.ki_selectors.append(ki_selector)
            
            label = QLabel(f"Team {i + 1} KI-Typ:")
            team_layout = QHBoxLayout()
            team_layout.addWidget(label)
            team_layout.addWidget(ki_selector)
            self.ki_selection_layout.addLayout(team_layout)

    def _on_start_game(self):
        # Temporäre Logik zum Starten des Spiels
        maze_gen = MazeGenerator(width=30, height=20)
        maze_data = maze_gen.generate()
        
        # Holen der ausgewählten KI-Typen (Platzhalter)
        ki_types = [selector.currentText() for selector in self.ki_selectors]
        
        self.accept()
        self.close()
        
        game_window = GameWindow(maze_data, parent=self.parent)
        game_window.show()

    def _on_cancel(self):
        self.close()
        if self.parent:
            self.parent.show()
