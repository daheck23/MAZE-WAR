# ... (Vorheriger Code) ...
from gui.game_window import GameWindow
from gui.map_settings_dialog import MapSettingsDialog

class StartDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAZE-AI War v1.0")
        self.setGeometry(100, 100, 600, 800)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, True)
        self.map_settings_dialog = None
        self.game_window = None
        self.init_ui()

    # ... (Rest des Codes bleibt gleich, bis zu den Methoden) ...

    def _on_start_game_clicked(self):
        # Temporäre Labyrinth-Generierung für die Ansicht
        maze_gen = MazeGenerator(width=30, height=20)
        maze_data = maze_gen.generate()
        
        self.game_window = GameWindow(maze_data, parent=self)
        self.hide()

    def _on_generate_map_clicked(self):
        self.map_settings_dialog = MapSettingsDialog()
        self.map_settings_dialog.show()

    # ... (Rest der Methoden bleibt gleich) ...
