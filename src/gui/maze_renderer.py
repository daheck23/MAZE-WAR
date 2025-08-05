import numpy as np
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QBrush, QColor
from PyQt6.QtCore import Qt

class MazeRenderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.maze_data = None
        self.cell_size = 20

    def set_maze_data(self, maze_data):
        self.maze_data = maze_data
        self.setFixedSize(
            self.maze_data.shape[1] * self.cell_size,
            self.maze_data.shape[0] * self.cell_size
        )
        self.update()

    def paintEvent(self, event):
        if self.maze_data is None:
            return

        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

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
