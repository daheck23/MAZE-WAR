import sys
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QSlider, QPushButton, QGroupBox, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

class MapSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Map generieren")
        self.setFixedSize(350, 300)
        
        self.map_name = ""
        self.map_width = 20
        self.map_height = 20
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Map-Name
        name_group = QGroupBox("Map-Name")
        name_layout = QVBoxLayout()
        self.name_input = QLineEdit("MeineMap")
        name_layout.addWidget(self.name_input)
        name_group.setLayout(name_layout)
        main_layout.addWidget(name_group)

        # Breite und Höhe
        size_group = QGroupBox("Dimensionen")
        size_layout = QVBoxLayout()
        
        self.width_slider_label = QLabel(f"Breite: {self.map_width}")
        self.width_slider = QSlider(Qt.Orientation.Horizontal)
        self.width_slider.setMinimum(15)
        self.width_slider.setMaximum(35)
        self.width_slider.setValue(self.map_width)
        self.width_slider.valueChanged.connect(lambda value: self.width_slider_label.setText(f"Breite: {value}"))
        
        self.height_slider_label = QLabel(f"Höhe: {self.map_height}")
        self.height_slider = QSlider(Qt.Orientation.Horizontal)
        self.height_slider.setMinimum(15)
        self.height_slider.setMaximum(35)
        self.height_slider.setValue(self.map_height)
        self.height_slider.valueChanged.connect(lambda value: self.height_slider_label.setText(f"Höhe: {value}"))
        
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
    
    def get_settings(self):
        self.map_name = self.name_input.text()
        self.map_width = self.width_slider.value()
        self.map_height = self.height_slider.value()
        return self.map_name, self.map_width, self.map_height