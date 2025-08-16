import sys
import os
import random
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QGroupBox, QListWidget, QProgressBar
)
from PyQt6.QtGui import QPixmap, QFont, QPainter, QColor
from PyQt6.QtCore import Qt, QTimer, QRectF

class MapWidget(QWidget):
    """
    Ein benutzerdefiniertes Widget zum Zeichnen der Labyrinth-Karte.
    """
    def __init__(self, map_name, teams_info, parent=None):
        super().__init__(parent)
        self.map_name = map_name
        self.teams_info = teams_info
        self.map_data = []
        self.cell_size = 0
        self.map_width = 0
        self.map_height = 0
        self.bases = []
        self.flag_pos = None  # Position der Flagge

        # Zuordnung der Teamnamen zu den Farben
        self.team_colors = {
            "Team Rot": QColor(255, 0, 0),
            "Team Blau": QColor(0, 0, 255),
            "Team Grün": QColor(0, 255, 0),
            "Team Pink": QColor(255, 105, 180), # Dunkleres Pink für bessere Sichtbarkeit
            "Team Gold": QColor(255, 215, 0)
        }

        # Pfad zur Bilddatei für die Wand und die Flagge
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        wall_path = os.path.join(base_path, 'assets', 'images', 'wall.png')
        flag_path = os.path.join(base_path, 'assets', 'images', 'flag.png')
        
        self.wall_pixmap = QPixmap(wall_path)
        self.flag_pixmap = QPixmap(flag_path)

        if self.wall_pixmap.isNull():
            print(f"FEHLER: Wall-Bilddatei nicht gefunden oder fehlerhaft: {wall_path}")
        if self.flag_pixmap.isNull():
            print(f"FEHLER: Flaggen-Bilddatei nicht gefunden oder fehlerhaft: {flag_path}")
            
        self.load_map()
        self.place_bases()
        self.place_flag()

    def load_map(self):
        """Lädt die Labyrinth-Daten aus der .map-Datei."""
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            map_path = os.path.join(base_path, 'assets', 'maps', self.map_name)

            print(f"DEBUG: Versuche, Karte zu laden von: {map_path}")
            
            with open(map_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                self.map_data = [list(line) for line in lines]
            
            self.map_height = len(self.map_data)
            self.map_width = len(self.map_data[0])
            print(f"DEBUG: Karte erfolgreich geladen. Abmessungen: {self.map_width}x{self.map_height}")
            
        except FileNotFoundError:
            print(f"FEHLER: Kartendatei nicht gefunden: {self.map_name}")
            self.map_data = []
        except IndexError:
            print(f"FEHLER: Leere oder fehlerhafte Kartendatei: {self.map_name}")
            self.map_data = []
        except Exception as e:
            print(f"SCHWERER FEHLER: Ein unerwarteter Fehler beim Laden der Karte ist aufgetreten: {e}")
            self.map_data = []

    def place_bases(self):
        """Platziert die Basen der Teams zufällig auf der Karte."""
        if not self.map_data:
            return

        empty_cells = []
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.map_data[y][x] == '.':
                    empty_cells.append((x, y))

        if not empty_cells:
            print(f"FEHLER: Die Karte '{self.map_name}' enthält keine leeren Felder ('.'). Basen können nicht platziert werden.")
            return

        random.shuffle(empty_cells)
        
        for team in self.teams_info:
            team_name = team['name']
            team_color = self.team_colors.get(team_name, QColor(255, 255, 255)) # Standardfarbe
            
            found_spot = False
            # Durchlaufe eine Kopie der Liste, um Modifikationen zu vermeiden
            for x, y in list(empty_cells):
                is_far_enough = True
                for base in self.bases:
                    # Manhattandistanz-Überprüfung
                    distance = abs(x - base['x']) + abs(y - base['y'])
                    # Die Entfernung muss größer oder gleich 4 sein
                    if distance < 4:
                        is_far_enough = False
                        break
                
                if is_far_enough:
                    self.bases.append({
                        'x': x,
                        'y': y,
                        'color': team_color,
                        'health': team['health'],
                        'sight_range': team['sight_range'],
                        'team_name': team_name # Füge den Teamnamen zur Basis hinzu
                    })
                    print(f"DEBUG: Basis für {team_name} bei ({x}, {y}) platziert.")
                    found_spot = True
                    # Die verwendete Zelle aus der Liste der leeren Zellen entfernen
                    empty_cells.remove((x, y))
                    break
            
            if not found_spot:
                print(f"WARNUNG: Konnte keine geeignete Position für die Basis von {team_name} finden. Möglicherweise sind zu viele Teams für die Kartengröße ausgewählt.")

    def place_flag(self):
        """Platziert die Flagge zufällig auf einem freien Feld auf der Karte."""
        if not self.map_data or self.flag_pos:
            return # Platziere nur eine Flagge pro Runde

        empty_cells = []
        for y in range(self.map_height):
            for x in range(self.map_width):
                # Finde leere Felder, die keine Basis sind
                is_base = any(base['x'] == x and base['y'] == y for base in self.bases)
                if self.map_data[y][x] == '.' and not is_base:
                    empty_cells.append((x, y))

        if empty_cells:
            random.shuffle(empty_cells)
            self.flag_pos = empty_cells[0]
            print(f"DEBUG: Flagge bei ({self.flag_pos[0]}, {self.flag_pos[1]}) platziert.")
        else:
            print("WARNUNG: Keine leeren Felder für die Flagge gefunden.")


    def paintEvent(self, event):
        """Zeichnet die Labyrinth-Zellen, Basen und Spielfiguren."""
        painter = QPainter(self)
        if not self.map_data:
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "FEHLER: Karte nicht geladen")
            return

        # Berechne die Zellgröße basierend auf der Größe des Widgets
        cell_width = self.width() / self.map_width
        cell_height = self.height() / self.map_height
        self.cell_size = min(cell_width, cell_height)

        # Zeichne das Labyrinth-Gitter
        for row_idx, row in enumerate(self.map_data):
            for col_idx, cell in enumerate(row):
                rect = QRectF(col_idx * self.cell_size, row_idx * self.cell_size, self.cell_size, self.cell_size)
                
                if cell == '#':
                    # Zeichne die Wand mit dem Bild
                    if not self.wall_pixmap.isNull():
                        scaled_pixmap = self.wall_pixmap.scaled(int(self.cell_size), int(self.cell_size), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        painter.drawPixmap(rect.toRect(), scaled_pixmap)
                    else:
                        painter.setBrush(QColor(0, 0, 0)) # Fallback, falls das Bild nicht geladen werden kann
                        painter.drawRect(rect)
                else:
                    # Zeichne den Weg mit der gewünschten Farbe
                    painter.setBrush(QColor(200, 200, 200)) # Graue Wege
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawRect(rect)
        
        # Zeichne die Basen
        if self.bases:
            for base in self.bases:
                painter.setBrush(base['color'])
                painter.setPen(Qt.PenStyle.NoPen)
                base_rect = QRectF(
                    base['x'] * self.cell_size + self.cell_size * 0.25,
                    base['y'] * self.cell_size + self.cell_size * 0.25,
                    self.cell_size * 0.5,
                    self.cell_size * 0.5
                )
                painter.drawEllipse(base_rect)

        # Zeichne die Flagge, falls vorhanden
        if self.flag_pos and not self.flag_pixmap.isNull():
            flag_rect = QRectF(
                self.flag_pos[0] * self.cell_size + self.cell_size * 0.2,
                self.flag_pos[1] * self.cell_size + self.cell_size * 0.2,
                self.cell_size * 0.6,
                self.cell_size * 0.6
            )
            scaled_pixmap = self.flag_pixmap.scaled(int(flag_rect.width()), int(flag_rect.height()), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(flag_rect.toRect(), scaled_pixmap)

class GameWindow(QMainWindow):
    """
    Das Hauptfenster des Spiels.
    """
    def __init__(self, start_dialog, map_name, teams_info):
        super().__init__()
        self.start_dialog = start_dialog
        self.map_name = map_name
        
        # Spiel-Variablen
        self.current_round = 1
        self.round_time_limit = 300 # 5 Minuten in Sekunden
        self.time_left = self.round_time_limit
        
        # Zuordnung der Teamnamen zu den Farben
        team_colors = {
            "Team Rot": QColor(255, 0, 0),
            "Team Blau": QColor(0, 0, 255),
            "Team Grün": QColor(0, 255, 0),
            "Team Pink": QColor(255, 105, 180),
            "Team Gold": QColor(255, 215, 0)
        }
        
        # Erstelle eine neue Teams-Info-Liste mit den erforderlichen Werten
        self.teams_info = []
        for team in teams_info:
            team_name = team['name']
            new_team = {
                'name': team_name,
                'color': team_colors.get(team_name, QColor(255, 255, 255)),
                'health': 200,
                'sight_range': 3,
                'score': 0,
                'is_active': True
            }
            self.teams_info.append(new_team)

        # Debugging-Ausgaben
        print(f"DEBUG: GameWindow-Initialisierung beginnt.")
        print(f"DEBUG: Geladene Karte: {self.map_name}")
        print(f"DEBUG: Geladene Teams: {self.teams_info}")

        # Fenster-Eigenschaften
        self.setWindowTitle("MAZE-AI WAR")
        self.setWindowState(Qt.WindowState.WindowFullScreen) # Vollbildmodus
        self.setStyleSheet("background-color: #333333; color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Haupt-Layout mit horizontaler Teilung (Spielfeld links, Teams rechts)
        self.main_h_layout = QHBoxLayout(self.central_widget)
        
        # Linke Seite: Spielfeld und Buttons
        self.left_v_layout = QVBoxLayout()
        self.left_v_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_v_layout.setSpacing(20)

        # Titel-Label
        self.title_label = QLabel(f"Runde {self.current_round}")
        self.title_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_v_layout.addWidget(self.title_label)
        
        # Rundenzeit-Label
        self.round_time_label = QLabel(f"Zeit: {self.time_left // 60:02}:{self.time_left % 60:02}")
        self.round_time_label.setFont(QFont("Arial", 14))
        self.round_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_v_layout.addWidget(self.round_time_label)

        # Spielfeld-Widget (ersetzt den alten QLabel-Platzhalter)
        self.game_area = MapWidget(self.map_name, self.teams_info)
        self.game_area.setFixedSize(800, 600)
        self.game_area.setStyleSheet("border: 2px solid #555555;")
        self.left_v_layout.addWidget(self.game_area)

        # Buttons
        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setFont(QFont("Arial", 14))
        self.pause_button.setFixedSize(120, 40)
        self.pause_button.setStyleSheet("background-color: #555555; border-radius: 10px; color: white;")
        
        self.restart_button = QPushButton("Neustart")
        self.restart_button.setFont(QFont("Arial", 14))
        self.restart_button.setFixedSize(120, 40)
        self.restart_button.setStyleSheet("background-color: #555555; border-radius: 10px; color: white;")

        self.quit_button = QPushButton("Beenden")
        self.quit_button.setFont(QFont("Arial", 14))
        self.quit_button.setFixedSize(120, 40)
        self.quit_button.setStyleSheet("background-color: #AA0000; border-radius: 10px; color: white;")
        self.quit_button.clicked.connect(self.close)

        self.button_h_layout.addWidget(self.pause_button)
        self.button_h_layout.addWidget(self.restart_button)
        self.button_h_layout.addWidget(self.quit_button)
        
        self.left_v_layout.addLayout(self.button_h_layout)

        # Rechte Seite: Team-Übersicht
        self.right_v_layout = QVBoxLayout()
        self.right_v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        teams_title_label = QLabel("Team-Übersicht")
        teams_title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        teams_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_v_layout.addWidget(teams_title_label)
        
        for team in self.teams_info:
            team_group = QGroupBox()
            team_group.setStyleSheet("color: white; border: 1px solid #555555; border-radius: 5px;")
            team_layout = QVBoxLayout(team_group)
            
            # Punktzahl und gewonnene Runden
            team_header_layout = QHBoxLayout()
            score_label = QLabel(f"{team['name']}: {team['score']} Punkte | 0 Runden")
            score_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            team_header_layout.addWidget(score_label)
            team_layout.addLayout(team_header_layout)

            # Basis-Gesundheit
            base_health_label = QLabel(f"Basis Gesundheit ({team['health']}):")
            team_layout.addWidget(base_health_label)
            base_health_bar = QProgressBar()
            base_health_bar.setRange(0, team['health'])
            base_health_bar.setValue(team['health'])
            base_health_bar.setStyleSheet("QProgressBar { background-color: #555555; border: 1px solid grey; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #4CAF50; }")
            team_layout.addWidget(base_health_bar)
            
            # Soldier-Details
            # Platzhalter für die Soldaten (noch ohne echte Spiellogik)
            
            # Simuliert einen toten Soldaten mit 10 Sekunden Respawn-Zeit
            is_soldier_1_dead = True
            respawn_time_1 = 10
            
            soldier_1_label = QLabel(f"Soldat 1: Waffe, Health 100")
            if is_soldier_1_dead:
                 soldier_1_label.setText(f"Soldat 1: respawning in {respawn_time_1}s")
            
            # Simuliert einen lebenden Soldaten
            is_soldier_2_dead = False
            respawn_time_2 = 0
            
            soldier_2_label = QLabel(f"Soldat 2: Waffe, Health 100")
            if is_soldier_2_dead:
                 soldier_2_label.setText(f"Soldat 2: respawning in {respawn_time_2}s")

            # Füge die Labels zum Layout hinzu
            team_layout.addWidget(soldier_1_label)
            team_layout.addWidget(soldier_2_label)
            
            self.right_v_layout.addWidget(team_group)

        # Füge die Layouts zum Haupt-Layout hinzu
        self.main_h_layout.addLayout(self.left_v_layout, 7) # größeres Stretch-Verhältnis
        self.main_h_layout.addLayout(self.right_v_layout, 3) # kleineres Stretch-Verhältnis
        
        # Timer für die Rundenzeit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_round_time)
        self.timer.start(1000)

    def update_round_time(self):
        """Aktualisiert das Rundenzeit-Label jede Sekunde."""
        if self.time_left > 0:
            self.time_left -= 1
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.round_time_label.setText(f"Zeit: {minutes:02}:{seconds:02}")
        else:
            self.timer.stop()
            self.round_time_label.setText("Zeit abgelaufen!")
            # Hier könnte Logik für das Ende der Runde eingefügt werden

    def closeEvent(self, event):
        """
        Behandelt das Schließen des Fensters und kehrt zum Start-Dialog zurück.
        """
        print("DEBUG: GameWindow wird geschlossen, kehre zum StartDialog zurück.")
        if self.timer.isActive():
            self.timer.stop()
        self.start_dialog.show()
        event.accept()
