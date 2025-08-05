import os
import numpy as np
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox,
    QPushButton, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from game_logic.maze_generator import MazeGenerator

class MapSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Map Generieren")
        self.setGeometry(200, 200, 400, 250)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Name der Karte
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("z.B. meine_erste_map")
        form_layout.addRow(QLabel("Name der Karte:"), self.name_input)

        # Breite der Karte
        self.width_input = QSpinBox()
        self.width_input.setMinimum(15)
        self.width_input.setMaximum(100)
        self.width_input.setValue(25)
        form_layout.addRow(QLabel("Breite (min. 15):"), self.width_input)

        # Höhe der Karte
        self.height_input = QSpinBox()
        self.height_input.setMinimum(15)
        self.height_input.setMaximum(100)
        self.height_input.setValue(25)
        form_layout.addRow(QLabel("Höhe (min. 15):"), self.height_input)

        main_layout.addLayout(form_layout)

        # Buttons
        button_layout = QVBoxLayout()
        self.generate_button = QPushButton("Karte generieren und speichern")
        self.generate_button.clicked.connect(self.generate_and_save_map)
        button_layout.addWidget(self.generate_button)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def generate_and_save_map(self):
        map_name = self.name_input.text()
        map_width = self.width_input.value()
        map_height = self.height_input.value()

        if not map_name:
            QMessageBox.warning(self, "Fehler", "Bitte gib einen Namen für die Karte ein.")
            return

        # Sicherstellen, dass der Ordner existiert
        maps_dir = "assets/maps"
        os.makedirs(maps_dir, exist_ok=True)
        
        file_path = os.path.join(maps_dir, f"{map_name}.map")

        if os.path.exists(file_path):
            reply = QMessageBox.question(
                self,
                "Karte existiert",
                "Eine Karte mit diesem Namen existiert bereits. Möchtest du sie überschreiben?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                return

        # Labyrinth generieren
        maze_gen = MazeGenerator(width=map_width, height=map_height)
        maze_data = maze_gen.generate()

        # Karte speichern
        try:
            np.savetxt(file_path, maze_data, fmt='%d', delimiter=',')
            QMessageBox.information(
                self, "Erfolg", f"Karte '{map_name}' wurde erfolgreich gespeichert."
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, "Fehler", f"Ein Fehler ist beim Speichern aufgetreten: {e}"
            )
