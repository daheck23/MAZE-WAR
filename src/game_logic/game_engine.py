import sys
import os
from src.gui.game_window import GameWindow

class GameEngine:
    """
    Diese Klasse verwaltet die Kernlogik des Spiels.
    Sie ist für das Starten des Spiels und die Verwaltung der Spielzustände verantwortlich.
    """
    def __init__(self, start_dialog):
        # Das Hauptfenster, um zum Start-Dialog zurückzukehren
        self.start_dialog = start_dialog
        self.game_window = None

    def start_game(self, map_name, teams_info):
        """
        Startet das Spiel mit der ausgewählten Karte und den Team-Einstellungen.
        
        Args:
            map_name (str): Der Name der ausgewählten Karte.
            teams_info (list): Eine Liste von Dictionaries mit Team-Informationen.
        """
        print(f"DEBUG: start_game() wird aufgerufen.")
        print(f"DEBUG: Startet Spiel mit Karte: {map_name} und Teams: {teams_info}")
        
        # Erstelle eine Instanz des Spiel-Fensters
        self.game_window = GameWindow(self.start_dialog, map_name, teams_info)
        
        # Verberge den GameSetupDialog
        self.start_dialog.hide()
        
        # Zeige das Spiel-Fenster an
        self.game_window.show()
