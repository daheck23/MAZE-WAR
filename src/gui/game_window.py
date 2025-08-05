import sys
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from gui.maze_renderer import MazeRenderer

class GameWindow(QWidget):
    def __init__(self, maze_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MAZE-AI War v1.0 - Game")
        self.parent = parent
        self.maze_data = maze_data
        self.timer = QTimer(self)
        self.timer_seconds = 300  # 5 Minuten
        self.init_ui()
        self.showFullScreen()
        self.start_timer()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Linke Seite: Spielfeld
        game_area_layout = QVBoxLayout()
        
        # Scoreboard-Bereich
        self.scoreboard_label = QLabel("Team 1: 0  |  Team 2: 0  |  Team 3: 0") # Platzhalter
        self.scoreboard_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.scoreboard_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        game_area_layout.addWidget(self.scoreboard_label)

        # Timer-Bereich
        self.timer_label = QLabel("05:00")
        self.timer_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        game_area_layout.addWidget(self.timer_label)

        # Maze-Renderer
        self.maze_renderer = MazeRenderer()
        self.maze_renderer.set_maze_data(self.maze_data)
        game_area_layout.addWidget(self.maze_renderer, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(game_area_layout, 7)

        # Rechte Seite: Buttons & Team-Infos
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Buttons
        self.restart_button = QPushButton("Neustart")
        self.restart_button.clicked.connect(self._on_restart_clicked)
        sidebar_layout.addWidget(self.restart_button)

        self.back_button = QPushButton("Zurück zum Startbildschirm")
        self.back_button.clicked.connect(self._on_back_to_start_clicked)
        sidebar_layout.addWidget(self.back_button)

        # Platzhalter für Teammitglieder
        sidebar_layout.addSpacing(50)
        team_members_label = QLabel("Teammitglieder-Status:")
        team_members_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        sidebar_layout.addWidget(team_members_label)
        
        # Beispiel für ein Platzhalter-Widget
        for i in range(4): # 2 Teams mit je 2 Spielern
            member_frame = QFrame()
            member_frame.setFrameShape(QFrame.Shape.Box)
            member_frame.setStyleSheet("background-color: lightgray;")
            member_frame.setFixedSize(200, 50)
            member_info = QLabel(f"Spieler {i+1} | Health: 20 | Respawn: -")
            member_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            member_frame_layout = QVBoxLayout(member_frame)
            member_frame_layout.addWidget(member_info)
            sidebar_layout.addWidget(member_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(sidebar_layout, 3)

        self.setLayout(main_layout)

    def _on_restart_clicked(self):
        # Hier kommt später die Logik zum Neustart des Spiels hin
        QMessageBox.information(self, "Neustart", "Das Spiel wird neu gestartet.")

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

    def start_timer(self):
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.timer_label.setText(f"{minutes:02}:{seconds:02}")
        else:
            self.timer.stop()
            # Hier kommt später die Logik für das Rundenende hin
            QMessageBox.information(self, "Rundenende", "Die Zeit ist abgelaufen!")
