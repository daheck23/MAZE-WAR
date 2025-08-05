import sys
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from gui.maze_renderer import MazeRenderer
from game_logic.game_state import GameState

class GameWindow(QWidget):
    def __init__(self, maze_data, team_count, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MAZE-AI War v1.0 - Game")
        self.parent = parent
        self.maze_data = maze_data
        self.game_state = GameState(maze_data, team_count)
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
        self.scoreboard_label = QLabel()
        self.update_scoreboard()
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
        self.maze_renderer.set_team_bases(self._get_renderer_bases())
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
        for team_name in self.game_state.teams:
            member_frame = QFrame()
            member_frame.setFrameShape(QFrame.Shape.Box)
            member_frame.setStyleSheet("background-color: lightgray;")
            member_frame.setFixedSize(200, 50)
            member_info = QLabel(f"{team_name} | Health: 20 | Respawn: -")
            member_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            member_frame_layout = QVBoxLayout(member_frame)
            member_frame_layout.addWidget(member_info)
            sidebar_layout.addWidget(member_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(sidebar_layout, 3)
        self.setLayout(main_layout)

    def _get_renderer_bases(self):
        bases_for_renderer = {}
        for team_name, data in self.game_state.teams.items():
            r, g, b = data['color']
            bases_for_renderer[team_name] = {
                'color': QColor(r, g, b),
                'position': data['position']
            }
        return bases_for_renderer

    def update_scoreboard(self):
        scores = [f"{team}: {data['score']}" for team, data in self.game_state.teams.items()]
        self.scoreboard_label.setText("  |  ".join(scores))

    def _on_restart_clicked(self):
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
            QMessageBox.information(self, "Rundenende", "Die Zeit ist abgelaufen!")
