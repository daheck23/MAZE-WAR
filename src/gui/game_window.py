import sys
import os
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QFrame,
    QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPixmap
from gui.maze_renderer import MazeRenderer
from game_logic.game_state import GameState

class GameWindow(QWidget):
    def __init__(self, maze_data, team_count, start_dialog_ref=None):
        super().__init__()
        self.setWindowTitle("MAZE-AI War v1.0 - Game")
        self.start_dialog_ref = start_dialog_ref
        self.maze_data = maze_data
        self.game_state = GameState(maze_data, team_count)
        
        self.timer = QTimer(self)
        self.timer_seconds = 300
        
        self.object_spawn_timer = QTimer(self)
        self.bonus_spawn_timer = QTimer(self)
        
        self.init_ui()
        self.showFullScreen()
        
        self.start_all_timers()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        game_area_layout = QVBoxLayout()
        
        self.scoreboard_label = QLabel()
        self.update_scoreboard()
        self.scoreboard_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.scoreboard_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        game_area_layout.addWidget(self.scoreboard_label)

        self.timer_label = QLabel("05:00")
        self.timer_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        game_area_layout.addWidget(self.timer_label)

        self.maze_renderer = MazeRenderer()
        self.maze_renderer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.maze_renderer.set_maze_data(self.maze_data)
        self.maze_renderer.set_team_bases(self._get_renderer_bases())
        
        # Übergibt die Objekte und die Flagge an den Renderer
        self.maze_renderer.set_objects(self.game_state.objects)
        self.maze_renderer.set_flag(self.game_state.flag)
        
        game_area_layout.addWidget(self.maze_renderer, 1)
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.restart_button = QPushButton("Neustart")
        self.restart_button.clicked.connect(self._on_restart_clicked)
        sidebar_layout.addWidget(self.restart_button)

        self.back_button = QPushButton("Zurück zum Startbildschirm")
        self.back_button.clicked.connect(self._on_back_to_start_clicked)
        sidebar_layout.addWidget(self.back_button)

        sidebar_layout.addSpacing(50)
        team_members_label = QLabel("Teammitglieder-Status:")
        team_members_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        sidebar_layout.addWidget(team_members_label)
        
        for team_name in self.game_state.teams:
            color_name = team_name.split()[1].lower()
            image_path = os.path.join("assets", "images", f"soldier-{color_name}.png")
            
            member_frame = QFrame()
            member_frame.setFrameShape(QFrame.Shape.Box)
            member_frame.setStyleSheet("background-color: lightgray;")
            
            member_layout = QHBoxLayout(member_frame)
            
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaledToHeight(40, Qt.TransformationMode.SmoothTransformation))
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                member_layout.addWidget(image_label)
            
            member_info = QLabel(f"{team_name} | Health: 20 | Respawn: -")
            member_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            member_layout.addWidget(member_info)
            
            sidebar_layout.addWidget(member_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(game_area_layout, 7)
        main_layout.addLayout(sidebar_layout, 3)

    def _get_renderer_bases(self):
        bases_for_renderer = {}
        for team_name, data in self.game_state.teams.items():
            r, g, b = data['color']
            bases_for_renderer[team_name] = {
                'color': QColor(r, g, b),
                'position': data['base_position']
            }
        return bases_for_renderer

    def update_scoreboard(self):
        scores = [f"{team}: {data['score']}" for team, data in self.game_state.teams.items()]
        self.scoreboard_label.setText("  |  ".join(scores))

    def _on_restart_clicked(self):
        QMessageBox.information(self, "Neustart", "Das Spiel wird neu gestartet.")

    def _on_back_to_start_clicked(self):
        self.close()
        if self.start_dialog_ref:
            self.start_dialog_ref.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Spiel beenden",
            "Möchtest du das Spiel beenden und zum Startbildschirm zurückkehren?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.start_dialog_ref:
                self.start_dialog_ref.show()
            event.accept()
        else:
            event.ignore()

    def start_all_timers(self):
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        
        self.object_spawn_timer.timeout.connect(self._spawn_object)
        self.object_spawn_timer.start(5000)
        
        self.bonus_spawn_timer.timeout.connect(self._spawn_bonus_object)
        self.bonus_spawn_timer.start(30000)

    def _spawn_object(self):
        self.game_state.place_object()
        self.maze_renderer.set_objects(self.game_state.objects)
        
    def _spawn_bonus_object(self):
        self.game_state.place_object(is_bonus_spawn=True)
        self.maze_renderer.set_objects(self.game_state.objects)
        
    def update_timer(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.timer_label.setText(f"{minutes:02}:{seconds:02}")
        else:
            self.timer.stop()
            self.object_spawn_timer.stop()
            self.bonus_spawn_timer.stop()
            QMessageBox.information(self, "Rundenende", "Die Zeit ist abgelaufen!")