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
            "Team Green": QColor(0, 255, 0, 150),
            "Team Gold": QColor(255, 255, 0, 150),
            "Team Pink": QColor(128, 0, 128, 150)
        }
        
        for team, (x, y) in self.base_positions.items():
            if team in base_colors:
                brush = QBrush(base_colors[team])
                pen = QPen(Qt.PenStyle.SolidLine)
                pen.setWidth(2)
                pen.setColor(QColor(0, 0, 0))
                self.scene.addRect(x * tile_size, y * tile_size, tile_size, tile_size, pen, brush)

    def _load_map_data(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        maps_path = os.path.join(base_path, 'assets', 'maps')
        file_path = os.path.join(maps_path, self.map_name)
        
        print(f"DEBUG: Versuche, Karte von Pfad zu laden: '{file_path}'")
        map_data = []
        if os.path.exists(file_path):
            print("DEBUG: Kartendatei existiert.")
            with open(file_path, 'r') as f:
                for line in f:
                    map_data.append(line.strip())
        else:
            print("DEBUG: Fehler - Kartendatei existiert NICHT.")
        
        return map_data

    def _get_image_path(self, filename):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, 'assets', 'images', filename)

    def _draw_maze(self, scene):
        print(f"DEBUG: _draw_maze() aufgerufen mit {len(self.map_data)} Zeilen.")
        if not self.map_data:
            print("DEBUG: Kartendaten sind leer.")
            return
        
        view_width = self.view.width()
        view_height = self.view.height()
        
        if self.width == 0 or self.height == 0 or view_width == 0 or view_height == 0:
            print("DEBUG: Fenstergröße ist null. Zeichnen nicht möglich.")
            return

        tile_size_w = view_width // self.width if self.width > 0 else 0
        tile_size_h = view_height // self.height if self.height > 0 else 0
        tile_size = min(tile_size_w, tile_size_h) if tile_size_w > 0 and tile_size_h > 0 else 0
        
        print(f"DEBUG: Fenstergröße: {view_width}x{view_height}, berechnete Kachelgröße: {tile_size}")

        if tile_size <= 0:
            print("DEBUG: Kachelgröße ist 0 oder kleiner. Zeichnen nicht möglich.")
            return

        wall_pixmap = QPixmap(self._get_image_path("wall.png")).scaled(tile_size, tile_size)
        
        for y, row in enumerate(self.map_data):
            # Korrektur: Überprüfen, ob x innerhalb der Zeilenlänge liegt
            for x, tile in enumerate(row):
                if tile == '#':
                    item = QGraphicsPixmapItem(wall_pixmap)
                    item.setPos(x * tile_size, y * tile_size)
                    scene.addItem(item)
                else:
                    scene.addRect(x * tile_size, y * tile_size, tile_size, tile_size, QPen(Qt.PenStyle.NoPen), QBrush(QColor(255, 255, 255)))
    
    def init_ui(self):
        main_layout = QGridLayout(self.central_widget)
        
        left_panel = QVBoxLayout()
        info_font = QFont("Arial", 16, QFont.Weight.Bold)
        info_label = QLabel("Timer: 5:00  |  Runde 1/7")
        info_label.setFont(info_font)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel.addWidget(info_label)
        
        left_panel.addWidget(self.view)
        
        right_panel = QVBoxLayout()
        teams_group_box = QGroupBox("Teams & Punkte")
        teams_layout = QVBoxLayout()
        
        team_images = {
            "Team Red": "soldier-red.png",
            "Team Blue": "soldier-blue.png",
            "Team Green": "soldier-green.png",
            "Team Gold": "soldier-gold.png",
            "Team Pink": "soldier-pink.png"
        }
        
        for team_info in self.teams_info:
            team_name = team_info['name']
            soldier_img = team_images.get(team_name, "default-soldier.png")
            
            team_layout = QHBoxLayout()
            pixmap = QPixmap(self._get_image_path(soldier_img)).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
            img_label = QLabel()
            img_label.setPixmap(pixmap)
            team_layout.addWidget(img_label)
            
            info_label = QLabel(f"{team_name}: 5 Punkte")
            team_layout.addWidget(info_label)
            teams_layout.addLayout(team_layout)
            
        teams_group_box.setLayout(teams_layout)
        right_panel.addWidget(teams_group_box)
        right_panel.addStretch()
        
        button_font = QFont("Arial", 12)
        next_round_button = QPushButton("Nächste Runde")
        next_round_button.setFont(button_font)
        right_panel.addWidget(next_round_button)
        
        restart_button = QPushButton("Neustart")
        restart_button.setFont(button_font)
        right_panel.addWidget(restart_button)
        
        back_to_start_button = QPushButton("Zurück zum Startbildschirm")
        back_to_start_button.setFont(button_font)
        back_to_start_button.clicked.connect(self.close_and_return_to_start)
        right_panel.addWidget(back_to_start_button)
        
        main_layout.addLayout(left_panel, 0, 0, 1, 1)
        main_layout.addLayout(right_panel, 0, 1, 1, 1)

    def close_and_return_to_start(self):
        print("DEBUG: close_and_return_to_start() aufgerufen.")
        if isinstance(self.parent(), QWidget):
            print("DEBUG: Parent existiert, zeige Parent an.")
            self.parent().show()
        else:
            print("DEBUG: Kein Parent gefunden.")
        self.close()
