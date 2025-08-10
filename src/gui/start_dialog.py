import sys
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from .game_setup_dialog import GameSetupDialog

class StartDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MAZE-AI WAR")
        self.setFixedSize(500, 300)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label = QLabel("MAZE-AI WAR")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        play_button = QPushButton("Spiel starten")
        play_button.clicked.connect(self.open_setup_dialog)
        main_layout.addWidget(play_button)

        exit_button = QPushButton("Beenden")
        exit_button.clicked.connect(self.close)
        main_layout.addWidget(exit_button)

    def open_setup_dialog(self):
        print("DEBUG: StartDialog öffnet GameSetupDialog.")
        setup_dialog = GameSetupDialog(parent=self)
        self.hide()
        setup_dialog.show()