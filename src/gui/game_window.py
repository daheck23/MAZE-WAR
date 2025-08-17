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
        self.objects_to_draw = [] # Liste der Objekte, die gezeichnet werden sollen
        self.soldiers_to_draw = [] # Liste der Soldaten, die gezeichnet werden sollen

        # Zuordnung der Teamnamen zu den Farben
        self.team_colors = {
            "Team Rot": QColor(255, 0, 0),
            "Team Blau": QColor(0, 0, 255),
            "Team Grün": QColor(0, 255, 0),
            "Team Pink": QColor(255, 105, 180),
            "Team Gold": QColor(255, 215, 0)
        }

        # Pfade zu den Bilddateien
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_paths = {
            'wall': os.path.join(base_path, 'assets', 'images', 'wall.png'),
            'flag': os.path.join(base_path, 'assets', 'images', 'flag.png'),
            'knife': os.path.join(base_path, 'assets', 'images', 'knife.png'),
            'gun': os.path.join(base_path, 'assets', 'images', 'gun.png'),
            'grenade': os.path.join(base_path, 'assets', 'images', 'grenade.png'),
            'nuke': os.path.join(base_path, 'assets', 'images', 'nuke.png'),
            'pink_duck': os.path.join(base_path, 'assets', 'images', 'pink_duck.png'),
            'red pill': os.path.join(base_path, 'assets', 'images', 'redpill.png'),
            'blue pill': os.path.join(base_path, 'assets', 'images', 'bluepill.png'),
            'fake flag': os.path.join(base_path, 'assets', 'images', 'fake_flag.png'),
            'fernglas': os.path.join(base_path, 'assets', 'images', 'binoculars.png'),
            # Korrigierte Dateinamen für Soldatenbilder
            'soldier-red': os.path.join(base_path, 'assets', 'images', 'soldier-red.png'),
            'soldier-blue': os.path.join(base_path, 'assets', 'images', 'soldier-blue.png'),
            'soldier-green': os.path.join(base_path, 'assets', 'images', 'soldier-green.png'),
            'soldier-pink': os.path.join(base_path, 'assets', 'images', 'soldier-pink.png'),
            'soldier-gold': os.path.join(base_path, 'assets', 'images', 'soldier-gold.png'),
            'dead-soldier': os.path.join(base_path, 'assets', 'images', 'dead-soldier.png'),
        }

        # Lade alle Pixmaps und prüfe auf Fehler
        self.pixmaps = {}
        for name, path in self.image_paths.items():
            self.pixmaps[name] = QPixmap(path)
            if self.pixmaps[name].isNull():
                print(f"FEHLER: Bilddatei für '{name}' nicht gefunden oder fehlerhaft: {path}")

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

    def update_objects_to_draw(self, objects_list):
        """Aktualisiert die Liste der zu zeichnenden Objekte."""
        self.objects_to_draw = objects_list
        self.update() # Löst ein Neuzeichnen des Widgets aus

    def update_soldiers_to_draw(self, soldiers_list):
        """Aktualisiert die Liste der zu zeichnenden Soldaten."""
        self.soldiers_to_draw = soldiers_list
        self.update() # Löst ein Neuzeichnen des Widgets aus


    def paintEvent(self, event):
        """Zeichnet die Labyrinth-Zellen, Basen, Spielfiguren und Soldaten."""
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
                    if 'wall' in self.pixmaps and not self.pixmaps['wall'].isNull():
                        scaled_pixmap = self.pixmaps['wall'].scaled(int(self.cell_size), int(self.cell_size), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
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
        if self.flag_pos and 'flag' in self.pixmaps and not self.pixmaps['flag'].isNull():
            flag_rect = QRectF(
                self.flag_pos[0] * self.cell_size + self.cell_size * 0.2,
                self.flag_pos[1] * self.cell_size + self.cell_size * 0.2,
                self.cell_size * 0.6,
                self.cell_size * 0.6
            )
            scaled_pixmap = self.pixmaps['flag'].scaled(int(flag_rect.width()), int(flag_rect.height()), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(flag_rect.toRect(), scaled_pixmap)
            
        # Zeichne die Objekte
        for obj in self.objects_to_draw:
            obj_type = obj['type']
            if obj_type in self.pixmaps and not self.pixmaps[obj_type].isNull():
                obj_rect = QRectF(
                    obj['pos'][0] * self.cell_size + self.cell_size * 0.2,
                    obj['pos'][1] * self.cell_size + self.cell_size * 0.2,
                    self.cell_size * 0.6,
                    self.cell_size * 0.6
                )
                scaled_pixmap = self.pixmaps[obj_type].scaled(int(obj_rect.width()), int(obj_rect.height()), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                painter.drawPixmap(obj_rect.toRect(), scaled_pixmap)

        # Zeichne die Soldaten
        for soldier in self.soldiers_to_draw:
            # Zeige tote Soldaten mit dem dead-soldier Bild an
            if soldier['health'] <= 0:
                soldier_type = 'dead-soldier'
            else:
                soldier_type = soldier['image']

            if soldier_type in self.pixmaps and not self.pixmaps[soldier_type].isNull():
                soldier_rect = QRectF(
                    soldier['pos'][0] * self.cell_size + self.cell_size * 0.2,
                    soldier['pos'][1] * self.cell_size + self.cell_size * 0.2,
                    self.cell_size * 0.6,
                    self.cell_size * 0.6
                )
                scaled_pixmap = self.pixmaps[soldier_type].scaled(int(soldier_rect.width()), int(soldier_rect.height()), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                painter.drawPixmap(soldier_rect.toRect(), scaled_pixmap)

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

        # Zuordnung der deutschen Teamnamen zu den englischen Bildnamen
        self.team_name_to_image_name = {
            'Team Rot': 'soldier-red',
            'Team Blau': 'soldier-blue',
            'Team Grün': 'soldier-green',
            'Team Pink': 'soldier-pink',
            'Team Gold': 'soldier-gold',
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

        # --- Objekt-Logik Hinzufügung ---
        self.objects = []
        self.max_objects = (self.game_area.map_width * self.game_area.map_height) // 50
        print(f"DEBUG: Maximale Objektanzahl für diese Karte: {self.max_objects}")
        
        self.object_types = {
            'knife': {'image': 'knife', 'attack': 2, 'radius': 2},
            'gun': {'image': 'gun', 'attack': 3, 'radius': 3},
            'grenade': {'image': 'grenade', 'attack': 5, 'radius': 4},
            'nuke': {'image': 'nuke', 'attack': 'all', 'radius': 'all'},
            'pink_duck': {'image': 'pink_duck', 'points': 3},
            'red pill': {'image': 'red pill', 'health': 25},
            'blue pill': {'image': 'blue pill', 'health': 10},
            'fake flag': {'image': 'fake flag', 'effect': 'deception'},
            'fernglas': {'image': 'fernglas', 'sight_range': 4},
        }

        # --- Soldaten-Logik Hinzufügung (Reihenfolge korrigiert) ---
        self.soldiers = []
        self.soldier_stats = {
            'health': 25,
            'sight_range': 3,
            'attack': 1,
            'attack_range': 1
        }
        self.place_initial_soldiers()
        # --- Ende Soldaten-Logik Hinzufügung ---
        
        # --- Objekt-Logik Hinzufügung (jetzt nach Soldaten-Initialisierung) ---
        self.place_initial_objects()
        self.object_spawn_timer = QTimer(self)
        self.object_spawn_timer.timeout.connect(self.spawn_new_object)
        self.object_spawn_timer.start(20000) # 20 Sekunden
        # --- Ende Objekt-Logik Hinzufügung ---


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

        self.team_ui_elements = {}
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
            soldier_details_layout = QVBoxLayout()
            self.team_ui_elements[team['name']] = {
                'score_label': score_label,
                'base_health_bar': base_health_bar,
                'soldier_labels': [QLabel("Soldat 1: Wird geladen..."), QLabel("Soldat 2: Wird geladen...")]
            }
            soldier_details_layout.addWidget(self.team_ui_elements[team['name']]['soldier_labels'][0])
            soldier_details_layout.addWidget(self.team_ui_elements[team['name']]['soldier_labels'][1])
            team_layout.addLayout(soldier_details_layout)
            
            self.right_v_layout.addWidget(team_group)

        # Füge die Layouts zum Haupt-Layout hinzu
        self.main_h_layout.addLayout(self.left_v_layout, 7) # größeres Stretch-Verhältnis
        self.main_h_layout.addLayout(self.right_v_layout, 3) # kleineres Stretch-Verhältnis
        
        # Haupt-Timer für die Spiel-Logik und UI-Updates
        self.game_loop_timer = QTimer(self)
        self.game_loop_timer.timeout.connect(self.check_game_state)
        self.game_loop_timer.start(100) # Läuft alle 100ms
        
        # Timer für die Rundenzeit
        self.round_time_timer = QTimer(self)
        self.round_time_timer.timeout.connect(self.update_round_time)
        self.round_time_timer.start(1000)

    def update_round_time(self):
        """Aktualisiert das Rundenzeit-Label jede Sekunde."""
        if self.time_left > 0:
            self.time_left -= 1
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.round_time_label.setText(f"Zeit: {minutes:02}:{seconds:02}")
        else:
            self.round_time_timer.stop()
            self.game_loop_timer.stop()
            self.object_spawn_timer.stop()
            self.round_time_label.setText("Zeit abgelaufen!")
            # Hier könnte Logik für das Ende der Runde eingefügt werden

    def closeEvent(self, event):
        """
        Behandelt das Schließen des Fensters und kehrt zum Start-Dialog zurück.
        """
        print("DEBUG: GameWindow wird geschlossen, kehre zum StartDialog zurück.")
        if self.round_time_timer.isActive():
            self.round_time_timer.stop()
        if self.game_loop_timer.isActive():
            self.game_loop_timer.stop()
        if self.object_spawn_timer.isActive():
            self.object_spawn_timer.stop()
        self.start_dialog.show()
        event.accept()

    def check_game_state(self):
        """Überprüft den Spielzustand, Kollisionen und respawned Soldaten."""
        self.check_collisions()
        self.check_and_respawn_soldiers()
        self.update_ui_details()
        
    def check_collisions(self):
        """Prüft auf Kollisionen zwischen Soldaten und Objekten."""
        soldiers_to_check = self.soldiers.copy()
        
        for soldier in soldiers_to_check:
            # Nur lebende Soldaten können Objekte aufsammeln
            if soldier['health'] <= 0:
                continue

            for obj in self.objects.copy():
                if soldier['pos'] == obj['pos']:
                    print(f"DEBUG: {soldier['id']} hat Objekt {obj['type']} bei {obj['pos']} aufgesammelt.")
                    
                    # Hier könnte die Logik zum Anwenden des Objekt-Effekts stehen
                    # z.B. soldier['health'] += self.object_types[obj['type']]['health']
                    # Die Logik zum Töten eines Soldaten wurde entfernt.
                    
                    self.objects.remove(obj)
                    self.game_area.update_objects_to_draw(self.objects)
                    # Da ein Objekt aufgesammelt wurde, verlassen wir die innere Schleife
                    # und gehen zum nächsten Soldaten
                    break


    def check_and_respawn_soldiers(self):
        """Überprüft tote Soldaten und respawned sie, wenn der Timer abgelaufen ist."""
        for soldier in self.soldiers:
            if soldier['health'] <= 0:
                # Zeige toten Soldaten auf der Karte an
                soldier['image'] = 'dead-soldier'
                if soldier['respawn_timer'] > 0:
                    soldier['respawn_timer'] -= 1
                    # print(f"DEBUG: {soldier['id']} respawnt in {soldier['respawn_timer']/10:.1f}s.")
                else:
                    base_info = next((base for base in self.game_area.bases if base['team_name'] == soldier['team_name']), None)
                    if base_info:
                        soldier['pos'] = (base_info['x'], base_info['y'])
                        soldier['health'] = self.soldier_stats['health']
                        soldier['respawn_timer'] = -1 # Timer zurücksetzen
                        # Setze das Bild des Soldaten auf das ursprüngliche Team-Bild zurück
                        soldier['image'] = self.team_name_to_image_name.get(soldier['team_name'])
                        print(f"DEBUG: {soldier['id']} respawned an Basis bei {soldier['pos']}.")
                    else:
                        print(f"FEHLER: Basis für Team {soldier['team_name']} nicht gefunden!")

        # Aktualisiere die Soldaten auf der Karte
        self.game_area.update_soldiers_to_draw(self.soldiers)

    def update_ui_details(self):
        """Aktualisiert die UI-Elemente basierend auf dem aktuellen Spielzustand."""
        soldiers_by_team = {}
        for soldier in self.soldiers:
            team_name = soldier['team_name']
            if team_name not in soldiers_by_team:
                soldiers_by_team[team_name] = []
            soldiers_by_team[team_name].append(soldier)
        
        for team_name, team_soldiers in soldiers_by_team.items():
            if team_name in self.team_ui_elements:
                labels = self.team_ui_elements[team_name]['soldier_labels']
                for i, soldier in enumerate(team_soldiers):
                    if soldier['health'] > 0:
                        labels[i].setText(f"Soldat {i+1}: Health {soldier['health']} | Attack {soldier['attack']} | Range {soldier['attack_range']}")
                    else:
                        respawn_time_seconds = soldier['respawn_timer'] / 10
                        labels[i].setText(f"Soldat {i+1}: respawning in {respawn_time_seconds:.1f}s")
    
    def place_initial_objects(self):
        """Platziert die Hälfte der maximalen Objekte beim Spielstart."""
        initial_count = self.max_objects // 2
        print(f"DEBUG: Platziere {initial_count} Objekte beim Spielstart.")
        for _ in range(initial_count):
            self.spawn_new_object(initial=True)

    def spawn_new_object(self, initial=False):
        """Platziert ein neues Objekt auf der Karte."""
        if len(self.objects) >= self.max_objects:
            # Maximale Objektzahl erreicht, Timer stoppen
            if not initial:
                print("DEBUG: Maximale Objektanzahl erreicht. Timer wird gestoppt.")
                self.object_spawn_timer.stop()
            return

        # Liste der Objekte zur Auswahl, mit Gewichten
        object_choices = ['knife', 'gun', 'grenade', 'pink_duck', 'red pill', 'blue pill', 'fake flag', 'fernglas']
        weights = [10, 8, 5, 5, 6, 7, 3, 4]

        # Die 'nuke' darf nicht am Anfang platziert werden und ist sehr selten
        if not initial:
            object_choices.append('nuke')
            weights.append(1)

        # Wähle ein Objekt basierend auf den Gewichten
        chosen_type = random.choices(object_choices, weights=weights, k=1)[0]
        
        # Finde eine leere Zelle, die weder eine Basis noch ein Objekt oder Soldat ist
        empty_cells = []
        for y in range(self.game_area.map_height):
            for x in range(self.game_area.map_width):
                is_occupied = any((x, y) == obj['pos'] for obj in self.objects) or \
                             any((x, y) == (base['x'], base['y']) for base in self.game_area.bases) or \
                             any((x, y) == soldier['pos'] and soldier['health'] > 0 for soldier in self.soldiers)
                if self.game_area.map_data[y][x] == '.' and not is_occupied:
                    empty_cells.append((x, y))
        
        if empty_cells:
            pos = random.choice(empty_cells)
            
            # Erstelle die Objektinstanz
            new_obj = {
                'type': chosen_type,
                'pos': pos
            }
            self.objects.append(new_obj)
            print(f"DEBUG: Neues Objekt '{chosen_type}' bei ({pos[0]}, {pos[1]}) platziert.")

            # Aktualisiere die Objekte, die gezeichnet werden sollen
            self.game_area.update_objects_to_draw(self.objects)
        else:
            print("WARNUNG: Konnte kein freies Feld für neues Objekt finden.")

    def place_initial_soldiers(self):
        """Platziert 2 Soldaten für jedes Team an ihrer jeweiligen Basis."""
        for team in self.teams_info:
            base_info = next((base for base in self.game_area.bases if base['team_name'] == team['name']), None)
            
            if base_info:
                team_name = team['name']
                team_image_name = self.team_name_to_image_name.get(team_name)

                if not team_image_name:
                    print(f"WARNUNG: Kein Bildname für Team '{team_name}' gefunden. Überspringe Soldatenerstellung.")
                    continue
                
                # Platzierung für 2 Soldaten pro Team
                for i in range(2):
                    new_soldier = {
                        'id': f"{team_name}-soldier-{i+1}",
                        'pos': (base_info['x'], base_info['y']),
                        'team_name': team_name,
                        'health': self.soldier_stats['health'],
                        'sight_range': self.soldier_stats['sight_range'],
                        'attack': self.soldier_stats['attack'],
                        'attack_range': self.soldier_stats['attack_range'],
                        'image': team_image_name,
                        'respawn_timer': -1 # -1 bedeutet nicht im Respawn
                    }
                    self.soldiers.append(new_soldier)
                    print(f"DEBUG: {new_soldier['id']} für {team_name} bei ({new_soldier['pos'][0]}, {new_soldier['pos'][1]}) platziert.")

        # Aktualisiere die Soldaten, die gezeichnet werden sollen
        self.game_area.update_soldiers_to_draw(self.soldiers)

