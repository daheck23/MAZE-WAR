import time
from src.game_logic.base_manager import BaseManager
from src.game_logic.player_manager import PlayerManager
from src.game_logic.item_manager import ItemManager

def setup_game(maze_map, team_config):
    """
    Initialisiert alle Spielkomponenten und startet das Spiel.
    Diese Funktion wird aufgerufen, wenn der Benutzer auf 'Spiel starten' klickt.
    """
    # Hier werden die Positionen der Basen aus der Karte oder einer Konfiguration geladen
    blue_base_pos = (5, 5) 
    red_base_pos = (20, 20)
    
    # 1. Instanziierung der Manager-Objekte
    blue_base_manager = BaseManager('blue', blue_base_pos, team_config['blue'], maze_map)
    red_base_manager = BaseManager('red', red_base_pos, team_config['red'], maze_map)
    base_managers = {'blue': blue_base_manager, 'red': red_base_manager}
    
    item_manager = ItemManager(maze_map)
    player_manager = PlayerManager(maze_map, team_config, base_managers)

    # 2. Spielstart-Logik
    item_manager.place_initial_items()
    player_manager.initial_spawn()

    print("Spiel wird gestartet...")
    run_game_loop(player_manager, item_manager, base_managers)

def run_game_loop(player_manager, item_manager, base_managers):
    """
    Der Haupt-Game-Loop, der das Spielgeschehen steuert.
    """
    game_over = False
    
    while not game_over:
        # Hier findet der eigentliche Spiel-Loop statt, z.B.
        # - Bewegungen der Spieler-Agenten
        # - Kämpfe und Schadensberechnung
        # - Einsammeln von Items
        
        # 1. Manager-Objekte aktualisieren
        player_manager.update_respawns()
        item_manager.update_item_respawn()
        
        # 2. Basen nach Gegnern suchen lassen
        all_player_positions = player_manager.get_all_player_positions()
        base_managers['blue'].check_for_enemies(all_player_positions)
        base_managers['red'].check_for_enemies(all_player_positions)

        # 3. Siegbedingungen prüfen
        # Beispiel: Wenn eine Basis zerstört ist, hat das andere Team gewonnen
        if not base_managers['blue'].is_active or not base_managers['red'].is_active:
            game_over = True
            
        time.sleep(0.1) # Kurze Pause, um die CPU nicht zu überlasten
        
    print("Spiel beendet.")
