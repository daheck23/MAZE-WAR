import json

class GameState:
    def __init__(self, map_data):
        self.map_data = map_data
        self.player_data = {}
        self.item_properties = self._define_item_properties()
        self.items_on_map = {}
        
    def _define_item_properties(self):
        """
        Definiert die Eigenschaften (Werte) aller Objekte im Spiel,
        einschließlich der Bildnamen und Kampf-Attribute.
        """
        return {
            'red pill': {'health': 20, 'attack': 0, 'range': 0, 'vision_boost': 0},
            'blue pill': {'health': 10, 'attack': 0, 'range': 0, 'vision_boost': 0},
            'knife': {'health': 0, 'attack': 2, 'range': 1, 'vision_boost': 0},
            'gun': {'health': 0, 'attack': 5, 'range': 3, 'vision_boost': 0},
            'grenade': {'health': 0, 'attack': 15, 'range': 4, 'vision_boost': 0},
            'nuke': {'health': 0, 'attack': 9999, 'range': 9999, 'vision_boost': 0},
            'flag': {'health': 0, 'attack': 0, 'range': 0, 'vision_boost': 0},
            'fake_flag': {'health': 0, 'attack': 0, 'range': 0, 'vision_boost': 0},
            'pink duck': {'health': 0, 'attack': 0, 'range': 0, 'vision_boost': 0},
            'binoculars': {'health': 0, 'attack': 0, 'range': 0, 'vision_boost': 4},
        }

    def update(self, soldiers, items_on_map):
        """
        Aktualisiert den Spielzustand mit den neuesten Daten.
        """
        self.player_data = {}
        for team_soldiers in soldiers.values():
            for soldier in team_soldiers:
                self.player_data[soldier.soldier_id] = {
                    'team': soldier.team,
                    'position': soldier.position,
                    'health': soldier.health,
                    'is_alive': soldier.is_alive
                }
        self.items_on_map = items_on_map

    def get_item_properties(self, item_type):
        """
        Gibt die Eigenschaften eines Items zurück.
        """
        return self.item_properties.get(item_type, {})

    def get_player_health(self, player_id):
        """
        Gibt die aktuelle Gesundheit eines Spielers zurück.
        """
        return self.player_data.get(player_id, {}).get('health')

    def get_player_position(self, player_id):
        """
        Gibt die aktuelle Position eines Spielers zurück.
        """
        return self.player_data.get(player_id, {}).get('position')

    def get_state_for_ki(self, player_id):
        """
        Bereitet den Spielzustand so auf, dass er von der KI einfach verarbeitet werden kann.
        """
        state = []
        
        # Eigene Gesundheit und Position hinzufügen
        player_info = self.player_data.get(player_id, {})
        state.append(player_info.get('health', 0))
        state.extend(player_info.get('position', (0,0)))
        
        # Positionen und Werte aller Objekte auf der Karte hinzufügen
        for pos, item in self.items_on_map.items():
            state.extend(pos)
            item_values = self.get_item_properties(item)
            if item_values:
                state.append(item_values.get('health', 0))
                state.append(item_values.get('attack', 0))
                state.append(item_values.get('range', 0))
                state.append(item_values.get('vision_boost', 0))
        
        return state