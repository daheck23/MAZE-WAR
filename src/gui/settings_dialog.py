import sys
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QSlider, QLabel, QGroupBox, QGridLayout, QHBoxLayout, QPushButton, QRadioButton, QMessageBox
from PyQt6.QtCore import Qt
from ..utils.config import ConfigManager

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Einstellungen")
        self.setFixedSize(400, 300)
        
        self.config_manager = ConfigManager()
        self.settings = self.config_manager.load_settings()
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Rundenzeit-Einstellungen
        time_group = QGroupBox("Rundenzeit (Minuten)")
        time_layout = QVBoxLayout()
        self.time_slider_label = QLabel(f"Rundenzeit: {self.settings['round_time']} Minuten")
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setMinimum(5)
        self.time_slider.setMaximum(15)
        self.time_slider.setValue(self.settings['round_time'])
        self.time_slider.valueChanged.connect(self.update_time_label)
        time_layout.addWidget(self.time_slider_label)
        time_layout.addWidget(self.time_slider)
        time_group.setLayout(time_layout)
        
        # Best of-Einstellungen
        best_of_group = QGroupBox("Best of")
        best_of_layout = QHBoxLayout()
        self.best_of_buttons = {}
        options = [3, 5, 7]
        for value in options:
            button = QRadioButton(str(value))
            if value == self.settings['best_of']:
                button.setChecked(True)
            self.best_of_buttons[value] = button
            best_of_layout.addWidget(button)
        best_of_group.setLayout(best_of_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Speichern")
        cancel_button = QPushButton("Abbrechen")
        
        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        main_layout.addWidget(time_group)
        main_layout.addWidget(best_of_group)
        main_layout.addLayout(button_layout)
        
    def update_time_label(self, value):
        self.time_slider_label.setText(f"Rundenzeit: {value} Minuten")

    def save_settings(self):
        new_time = self.time_slider.value()
        new_best_of = self.settings['best_of']
        for value, button in self.best_of_buttons.items():
            if button.isChecked():
                new_best_of = value
                break
        
        self.settings['round_time'] = new_time
        self.settings['best_of'] = new_best_of
        self.config_manager.save_settings(self.settings)
        QMessageBox.information(self, "Einstellungen gespeichert", "Die Einstellungen wurden erfolgreich aktualisiert.")
        
        if self.parent():
            self.parent().show()
        self.accept()
    
    def reject(self):
        if self.parent():
            self.parent().show()
        super().reject()
        
    def closeEvent(self, event):
        if self.parent():
            self.parent().show()
        super().closeEvent(event)