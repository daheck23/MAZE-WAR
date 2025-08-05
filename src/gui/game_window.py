import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from gui.maze_renderer import MazeRenderer

class GameWindow(QWidget):
    def __init__(self, maze_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MAZE-AI War v1.0 - Game")
        self.maze_data = maze_data
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.maze_renderer = MazeRenderer()
        self.maze_renderer.set_maze_data(self.maze_data)
        layout.addWidget(self.maze_renderer)

        # Button, um zum Startbildschirm zurückzukehren
        back_button = QPushButton("Zurück zum Start")
        back_button.clicked.connect(self._on_back_to_start_clicked)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def _on_back_to_start_clicked(self):
        self.close()
        if self.parent:
            self.parent.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Spiel beenden",
            "Möchtest du das Spiel beenden und zum Startbildschirm zurückkehren?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.parent:
                self.parent.show()
            event.accept()
        else:
            event.ignore()
