import numpy as np
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtCore import Qt

class MazeRenderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.maze_data = None
        self.team_bases = {}
        self.cell_size = 20

    def set_maze_data(self, maze_data):
        self.maze_data = maze_data
        if maze_data is not None:
            self.setFixedSize(
                self.maze_data.shape[1] * self.cell_size,
                self.maze_data.shape[0] * self.cell_size
            )
        self.update()

    def set_team_bases(self, team_bases):
        self.team_bases = team_bases
        self.update()

    def paintEvent(self, event):
        if self.maze_data is None:
            return

        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

        # Draw the maze first
        for y in range(self.maze_data.shape[0]):
            for x in range(self.maze_data.shape[1]):
                cell_value = self.maze_data[y, x]
                if cell_value == 1:  # Wall
                    painter.setBrush(QBrush(QColor(100, 100, 100)))  # Dark gray
                else:  # Path
                    painter.setBrush(QBrush(QColor(200, 200, 200)))  # Light gray
                
                painter.drawRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

        # Draw team bases
        self.draw_team_bases(painter)

    def draw_team_bases(self, painter):
        for team_name, base_info in self.team_bases.items():
            color = base_info['color']
            position = base_info['position']
            x, y = position

            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            
            # Position und Größe des Kreises
            circle_x = x * self.cell_size + self.cell_size // 2
            circle_y = y * self.cell_size + self.cell_size // 2
            radius = self.cell_size // 2 - 2
            
            painter.drawEllipse(circle_x - radius, circle_y - radius, radius * 2, radius * 2)
