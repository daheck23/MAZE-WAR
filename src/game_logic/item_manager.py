import random
import time

class ItemManager:
    """
    Verwaltet das Platzieren, Einsammeln und Respawn von Objekten auf der Karte.
    """
    def __init__(self, map_data):
        self.map_data = map_data
        self.map_height = len(map_data)
        self.map_width = len(map_data[0]) if self.map_height > 0 else 0
        self.max_item_count = (self.map_width * self.map_height) // 20  # Beispiel: 1 Item pro 20 Kacheln
        self.respawn_delay = 30 # Sekunden für das schrittweise Auffüllen
        self.last_respawn_time = 0
        self.items_on_map = {}
        self.flag_placed = False

    def place_initial_items(self):
        """
        Platziert die Flagge und die Hälfte der restlichen Objekte am Spielstart.
        """
        if not self.flag_placed:
            self._place_specific_item('flag')
            self.flag_placed = True

        initial_item_count = self.max_item_count // 2
        
        # Liste der zufälligen Items (ohne Flagge)
        items_list = ['red pill', 'blue pill', 'nuke', 'knife', 'gun', 'grenade', 'pink duck', 'fake_flag']
        
        # Stelle sicher, dass Nuke sehr selten auftaucht
        random_items = [self._get_random_item(items_list) for _ in range(initial_item_count)]
        
        self._place_items(random_items)
        self.last_respawn_time = time.time() # Startet den Auffüll-Timer

    def _get_random_item(self, items_list):
        """Wählt ein zufälliges Item aus, wobei die Nuke sehr selten ist."""
        weights = [1] * len(items_list)
        if 'nuke' in items_list:
            nuke_index = items_list.index('nuke')
            weights[nuke_index] = 0.05 # 5% Wahrscheinlichkeit für Nuke
        
        return random.choices(items_list, weights, k=1)[0]
    
    def _place_specific_item(self, item_type):
        """Platziert ein einzelnes, spezifisches Item auf einer gültigen Position."""
        empty_positions = self._get_empty_positions()
        if empty_positions:
            random_pos = random.choice(empty_positions)
            x, y = random_pos
            self.map_data[y][x] = item_type
            self.items_on_map[item_type] = (x, y)
            print(f"Objekt '{item_type}' wurde bei ({x}, {y}) platziert.")
            return True
        return False
    
    def _place_items(self, item_list):
        """Platziert eine Liste von Items auf der Karte."""
        empty_positions = self._get_empty_positions()
        random.shuffle(empty_positions)
        
        for item_type in item_list:
            if empty_positions:
                x, y = empty_positions.pop(0)
                self.map_data[y][x] = item_type
                self.items_on_map[item_type] = (x, y)
            else:
                print(f"Warnung: Nicht genug Platz für alle Objekte. '{item_type}' konnte nicht platziert werden.")

    def update_item_respawn(self):
        """
        Überprüft, ob neue Items platziert werden sollen, um das Maximum aufzufüllen.
        """
        if len(self.items_on_map) < self.max_item_count and \
           (time.time() - self.last_respawn_time) > self.respawn_delay:
            
            # Platziere ein einzelnes neues Item
            new_item = self._get_random_item(['red pill', 'blue pill', 'nuke', 'knife', 'gun', 'grenade', 'pink duck', 'fake_flag'])
            if self._place_specific_item(new_item):
                self.last_respawn_time = time.time()
                print(f"Neues Item '{new_item}' wurde platziert.")

    def _get_empty_positions(self):
        """
        Findet alle leeren Positionen auf der Karte, die keine Mauern oder Basen sind.
        """
        map_height = len(self.map_data)
        map_width = len(self.map_data[0]) if map_height > 0 else 0
        
        empty_positions = []
        for y in range(map_height):
            for x in range(map_width):
                # Prüft, ob die Kachel weder eine Mauer ('#') noch eine Basis ('B') oder Startposition ('S') ist
                if self.map_data[y][x] not in ['#', 'B', 'S']:
                    empty_positions.append((x, y))
        return empty_positions
