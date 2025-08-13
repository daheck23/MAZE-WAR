import random

class ItemManager:
    """
    Verwaltet das Platzieren, Einsammeln und Respawn von Objekten auf der Karte.
    """
    def __init__(self, map_data):
        self.map_data = map_data
        self.respawn_times = {
            'pill': 15,    # 15 Sekunden
            'weapon': 30,  # 30 Sekunden
            'flag': 60,    # 60 Sekunden
        }
        self.items_on_map = {} # Speichert die Position der platzierten Items

    def place_initial_items(self, items_to_place):
        """
        Platziert die Startobjekte zufällig auf der Karte.
        """
        empty_positions = self._get_empty_positions()
        random.shuffle(empty_positions)

        for item_type in items_to_place:
            if empty_positions:
                x, y = empty_positions.pop(0)
                self.map_data[y][x] = item_type
                self.items_on_map[item_type] = (x, y)
                print(f"Objekt '{item_type}' wurde bei Position ({x}, {y}) platziert.")
            else:
                print(f"Warnung: Nicht genug Platz für alle Objekte. '{item_type}' konnte nicht platziert werden.")

    def _get_empty_positions(self):
        """
        Findet alle leeren Positionen auf der Karte.
        """
        map_height = len(self.map_data)
        map_width = len(self.map_data[0]) if map_height > 0 else 0
        
        empty_positions = []
        for y in range(map_height):
            for x in range(map_width):
                if self.map_data[y][x] == ' ':
                    empty_positions.append((x, y))
        return empty_positions

    def handle_item_collected(self, item_type):
        """
        Startet den Respawn-Timer für ein eingesammeltes Objekt.
        """
        print(f"Objekt '{item_type}' wurde eingesammelt. Respawn-Timer von {self.respawn_times.get(item_type, 'unbekannt')}s gestartet.")
        # Hier würdest du die Logik für den Timer implementieren.
        # Ein einfaches Beispiel wäre:
        # self.start_respawn_timer(item_type, self.respawn_times.get(item_type))
        # Diese Logik hängt stark von deinem Game-Loop ab.
        pass

# Beispiel zur Verwendung der Klasse in deiner main.py
# angenommen, du hast eine maze_map Variable
# from src.game_logic.item_manager import ItemManager
#
# my_map = [
#     ['#', '#', '#', '#'],
#     ['#', ' ', ' ', '#'],
#     ['#', ' ', ' ', '#'],
#     ['#', '#', '#', '#']
# ]
#
# item_manager = ItemManager(my_map)
# item_manager.place_initial_items(['flag', 'pill', 'weapon'])
