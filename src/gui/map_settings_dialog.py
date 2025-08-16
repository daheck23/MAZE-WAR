import sys
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QSlider, QPushButton, QGroupBox, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
import os
from ..game_logic.maze_generator import MazeGenerator

class MapSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Map generieren")
        self.setFixedSize(350, 300)
        
        self.map_name = "MeineMap.map"
        self.map_width = 15
        self.map_height = 15
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Map-Name
        name_group = QGroupBox("Map-Name")
        name_layout = QVBoxLayout()
        self.name_input = QLineEdit(self.map_name)
        name_layout.addWidget(self.name_input)
        name_group.setLayout(name_layout)
        main_layout.addWidget(name_group)

        # Breite und Höhe
        size_group = QGroupBox("Dimensionen")
        size_layout = QVBoxLayout()
        
        self.width_slider_label = QLabel(f"Breite: {self.map_width}")
        self.width_slider = QSlider(Qt.Orientation.Horizontal)
        self.width_slider.setMinimum(15)
        self.width_slider.setMaximum(31)
        self.width_slider.setSingleStep(2)
        self.width_slider.setPageStep(2)
        self.width_slider.setValue(self.map_width)
        self.width_slider.valueChanged.connect(self._adjust_width_slider)
        
        self.height_slider_label = QLabel(f"Höhe: {self.map_height}")
        self.height_slider = QSlider(Qt.Orientation.Horizontal)
        self.height_slider.setMinimum(15)
        self.height_slider.setMaximum(31)
        self.height_slider.setSingleStep(2)
        self.height_slider.setPageStep(2)
        self.height_slider.setValue(self.map_height)
        self.height_slider.valueChanged.connect(self._adjust_height_slider)
        
        size_layout.addWidget(self.width_slider_label)
        size_layout.addWidget(self.width_slider)
        size_layout.addWidget(self.height_slider_label)
        size_layout.addWidget(self.height_slider)
        size_group.setLayout(size_layout)
        main_layout.addWidget(size_group)

        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Abbrechen")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)
        
    def _adjust_width_slider(self, value):
        if value % 2 == 0:
            value = value + 1
            if value > 31:
                value = 31
            self.width_slider.setValue(value)
        self.width_slider_label.setText(f"Breite: {value}")

    def _adjust_height_slider(self, value):
        if value % 2 == 0:
            value = value + 1
            if value > 31:
                value = 31
            self.height_slider.setValue(value)
        self.height_slider_label.setText(f"Höhe: {value}")
    
    def accept(self):
        self.map_name = self.name_input.text()
        self.map_width = self.width_slider.value()
        self.map_height = self.height_slider.value()
            
        if not self.map_name.endswith('.map'):
            self.map_name += '.map'

        if not self.map_name:
            QMessageBox.warning(self, "Fehler", "Bitte gib einen Map-Namen ein.")
            return
            
        try:
            # Korrigierter Aufruf, um die statische Methode zu verwenden
            maze_data = MazeGenerator.generate_maze(self.map_width, self.map_height)
            
            maps_path = os.path.join("src", "assets", "maps")
            os.makedirs(maps_path, exist_ok=True)
            
            file_path = os.path.join(maps_path, self.map_name)
            
            # Korrigierter Aufruf, um die statische Methode zu verwenden
            MazeGenerator.save_map(maze_data, file_path)

            QMessageBox.information(self, "Erfolg", f"Map '{self.map_name}' wurde erfolgreich mit den Maßen {self.map_width}x{self.map_height} gespeichert.")
            
            if self.parent():
                self.parent().show()
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Ein Fehler ist aufgetreten: {e}")
            if self.parent():
                self.parent().show()
            super().reject()

    def reject(self):
        if self.parent():
            self.parent().show()
        super().reject()

    def closeEvent(self, event):
        if self.parent():
            self.parent().show()
        super().closeEvent(event)
