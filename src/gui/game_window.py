import sys
import os
import random
from PyQt6.QtWidgets import (QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, 
                             QWidget, QLabel, QGroupBox, QGridLayout, QPushButton,
                             QMessageBox, QApplication, QGraphicsPixmapItem, QHBoxLayout,
                             QSizePolicy)
from PyQt6.QtGui import QFont, QBrush, QColor, QPixmap, QPen
from PyQt6.QtCore import Qt, QTimer

class GameWindow(QMainWindow):
    def __init__(self, map_name, teams, parent=None):
        super().__init__(parent)
        self.map_name = map_name
        self.teams_info = teams
        self.teams = [t['name'] for t in teams]
        
        self.width = 0 
        self.height = 0
        self.map_data = []
        self.base_positions = {}
        
        self.setWindowTitle(f"MAZE-AI WAR - {self.map_name}")
        self.showFullScreen()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        
        self.init_ui()
        QTimer.singleShot(100, self._delayed_draw_maze)

    def _delayed_draw_maze(self):
        print("DEBUG: _delayed_draw_maze() aufgerufen.")
        self.scene.clear()
        self.map_data = self._load_map_data()
        
        if not self.map_data:
            print("DEBUG: Kartendaten sind leer, kann nicht zeichnen.")
            return

        self.height = len(self.map_data)
        self.width = max(len(row) for row in self.map_data) if self.map_data else 0

        self._draw_maze(self.scene)
        self._place_bases()
        self._draw_bases()

    def _place_bases(self):
        placed_positions = []
        
        for team in self.teams:
            found_position = False
            while not found_position:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                
                if x >= len(self.map_data[y]) or self.map_data[y][x] == '#':
                    continue
                
                is_far_enough = True
                for placed_x, placed_y in placed_positions:
                    distance_x = abs(x - placed_x)
                    distance_y = abs(y - placed_y)
                    if distance_x <= 4 and distance_y <= 4:
                        is_far_enough = False
                        break
                
                if is_far_enough:
                    self.base_positions[team] = (x, y)
                    placed_positions.append((x, y))
                    found_position = True

    def _draw_bases(self):
        if not self.base_positions:
            return
            
        view_width = self.view.width()
        view_height = self.view.height()
        tile_size_w = view_width // self.width if self.width > 0 else 0
        tile_size_h = view_height // self.height if self.height > 0 else 0
        
        tile_size = min(tile_size_w, tile_size_h) if tile_size_w > 0 and tile_size_h > 0 else 0

        base_colors = {
            "Team Red": QColor(255, 0, 0, 150),
            "Team Blue": QColor(0, 0, 255, 150),
            "Team Green
