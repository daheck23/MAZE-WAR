import random
import time

class ItemManager:
    """
    Verwaltet das Platzieren, Einsammeln und Respawn von Objekten auf der Karte.
    """
    def __init__(self, map_data, base_positions, all_soldier_positions):
        self.map_data = map_data
        self.base_positions = base_positions
        self.soldier_positions = all_soldier_positions
        self.map_height = len(map_data)
        self.map_width = len(map_data[0]) if self.map_height > 0 else 0
        
        # Maximale Anzahl an Items basierend auf der Kartengröße
        self.max_item_count = (self.map_width * self.map_height) // 20
        
        self.respawn_delay = 30 # Sekunden für das schrittweise Auffüllen
        self.last_respawn_time = 0
        self.items_on_map = {}
        self.flag_placed = False

    def place_initial_items(self):
        """
        Platziert die Flagge, optional eine Nuke und die restlichen Objekte am Spielstart.
        Stellt sicher, dass maximal eine Nuke platziert wird.
        """
        if not self.flag_placed:
            self._place_specific_item('flag')
            self.flag_placed = True

        # Liste der zufälligen Items (ohne Flagge und Nuke)
        items_list = ['red pill', 'blue pill', 'knife', 'gun', 'grenade', 'pink duck', 'fake_flag', 'binoculars']
        
        # Platziere optional eine Nuke mit einer bestimmten Wahrscheinlichkeit
        if random.random() < 0.10:  # 10% Wahrscheinlichkeit für eine Nuke am Start
            if self._place_specific_item('nuke'):
                print("Eine Nuke wurde am Spielstart platziert.")

        initial_item_count = self.max_item_count // 2
        
        # Platziere die restlichen Items
        for _ in range(initial_item_count - len(self.items_on_map)):
            item_type = random.choice(items_list)
            self._place_specific_item(item_type)

    def _get_random_item(self, items_list):
        """
        Gibt ein zufälliges Item zurück, wobei die Wahrscheinlichkeit für seltene Items geringer ist.
        """
        rare_items = {'nuke': 0.05}
        
        # Wähle ein Item unter Berücksichtigung der seltenen Items
        if random.random() < rare_items.get('nuke', 0):
            return 'nuke'
        else:
            return random.choice([item for item in items_list if item != 'nuke'])

    def _place_specific_item(self, item_type):
        """
        Platziert ein spezifisches Item an einer zufälligen, leeren Position.
        """
        empty_positions = self._get_empty_positions()
        if empty_positions:
            x, y = random.choice(empty_positions)
            # Item wird in einem Dictionary gespeichert, um seine Position zu verfolgen
            self.items_on_map[(x, y)] = item_type
            print(f"Item '{item_type}' wurde bei ({x}, {y}) platziert.")
            return True
        else:
            print(f"Warnung: Nicht genug Platz für neue Objekte. '{item_type}' konnte nicht platziert werden.")
            return False

    def update_item_respawn(self):
        """
        Überprüft, ob neue Items platziert werden sollen, um das Maximum aufzufüllen.
        """
        if len(self.items_on_map) < self.max_item_count and \
           (time.time() - self.last_respawn_time) > self.respawn_delay:
            
            # Platziere ein einzelnes neues Item
            items_list = ['red pill', 'blue pill', 'nuke', 'knife', 'gun', 'grenade', 'pink duck', 'fake_flag', 'binoculars']
            
            # Nuke Respawn-Logik: Max. 1 Nuke zur gleichen Zeit
            if 'nuke' in self.items_on_map.values():
                items_list.remove('nuke')
                
            new_item = self._get_random_item(items_list)
            
            if self._place_specific_item(new_item):
                self.last_respawn_time = time.time()
                print(f"Neues Item '{new_item}' wurde platziert.")

    def _get_empty_positions(self):
        """
        Findet alle leeren Positionen auf der Karte, die keine Mauern, Basen, Items oder Soldaten sind.
        """
        map_height = len(self.map_data)
        map_width = len(self.map_data[0]) if map_height > 0 else 0
        
        # Füge die Positionen der Soldaten zur Liste der zu vermeidenden Positionen hinzu
        occupied_positions = set(self.items_on_map.keys()) | set(self.base_positions.values()) | set(self.soldier_positions)
        
        empty_positions = []
        for y in range(map_height):
            for x in range(map_width):
                if self.map_data[y][x] == ' ' and (x, y) not in occupied_positions:
                    empty_positions.append((x, y))
        return empty_positions