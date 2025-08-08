import numpy as np
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen, QPolygon
from PyQt6.QtCore import QPoint, Qt

class MazeRenderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.maze_data = None
        self.team_bases = {}
        self.objects = []
        self.flag = None

    def set_maze_data(self, maze_data):
        self.maze_data = maze_data
        self.update()

    def set_team_bases(self, team_bases):
        self.team_bases = team_bases
        self.update()

    def set_objects(self, objects):
        self.objects = objects
        self.update()

    def set_flag(self, flag):
        self.flag = flag
        self.update()

    def paintEvent(self, event):
        if self.maze_data is None:
            return

        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

        if self.maze_data.shape[0] > 0 and self.maze_data.shape[1] > 0:
            cell_width = self.width() / self.maze_data.shape[1]
            cell_height = self.height() / self.maze_data.shape[0]
            self.cell_size = min(cell_width, cell_height)
        else:
            self.cell_size = 20

        for y in range(self.maze_data.shape[0]):
            for x in range(self.maze_data.shape[1]):
                cell_value = self.maze_data[y, x]
                if cell_value == 1:
                    painter.setBrush(QBrush(QColor(100, 100, 100)))
                else:
                    painter.setBrush(QBrush(QColor(200, 200, 200)))
                
                painter.drawRect(
                    int(x * self.cell_size),
                    int(y * self.cell_size),
                    int(self.cell_size),
                    int(self.cell_size)
                )

        self.draw_team_bases(painter)
        self.draw_objects(painter)
        self.draw_flag(painter)

    def draw_team_bases(self, painter):
        for team_name, base_info in self.team_bases.items():
            color = base_info['color']
            position = base_info['position']
            y, x = position  # Korrigierte Zuweisung

            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            
            circle_x = int(x * self.cell_size + self.cell_size / 2)
            circle_y = int(y * self.cell_size + self.cell_size / 2)
            radius = int(self.cell_size / 2 - 2)
            
            painter.drawEllipse(circle_x - radius, circle_y - radius, radius * 2, radius * 2)

    def draw_objects(self, painter):
        for obj in self.objects:
            position = obj['position']
            y, x = position  # Korrigierte Zuweisung
            obj_type = obj['type']
            
            if obj_type == 'knife':
                color = QColor(255, 255, 255)
            elif obj_type == 'gun':
                color = QColor(100, 100, 100)
            elif obj_type == 'grenade':
                color = QColor(255, 128, 0)
            elif obj_type == 'nuke':
                color = QColor(0, 0, 0)
            elif obj_type == 'bonus':
                color = QColor(0, 255, 255)
            else:
                color = QColor(0, 0, 0)
                
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            
            rect_x = int(x * self.cell_size + self.cell_size * 0.25)
            rect_y = int(y * self.cell_size + self.cell_size * 0.25)
            rect_size = int(self.cell_size * 0.5)
            
            painter.drawRect(rect_x, rect_y, rect_size, rect_size)
            
    def draw_flag(self, painter):
        if self.flag is not None:
            position = self.flag['position']
            y, x = position  # Korrigierte Zuweisung
            color = QColor(255, 215, 0)
            
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 2))

            points = QPolygon([
                QPoint(int(x * self.cell_size + self.cell_size * 0.5), int(y * self.cell_size + self.cell_size * 0.2)),
                QPoint(int(x * self.cell_size + self.cell_size * 0.8), int(y * self.cell_size + self.cell_size * 0.5)),
                QPoint(int(x * self.cell_size + self.cell_size * 0.5), int(y * self.cell_size + self.cell_size * 0.8))
            ])
            painter.drawPolygon(points)