import json

class GameState:
    def __init__(self, map_data, player_data):
        self.map_data = map_data
        self.player_data = player_data
        self.item_properties = self._define_item_properties()
        self.items_on_map = self._get_items_on_map()

    def _define_item_properties(self):
        """
        Definiert die Eigenschaften (Werte) aller Objekte im Spiel,
        einschließlich der Bildnamen und Kampf-Attribute.
        """
        return {
            'redpill': {'health': 20, 'attack': 0, 'image': 'redpill.png'},
            'bluepill': {'health': 10, 'attack': 0, 'image': 'bluepill.png'},
            'gun': {'health': 0, 'attack': 5, 'range': 3, 'image': 'gun.png'},
            'grenade': {'health': 0, 'attack': 15, 'range': 4, 'image': 'grenade.png'},
            'nuke': {'health': 0, 'attack': 9999, 'range': 9999, 'image': 'nuke.png'},
            'flag': {'health': 0, 'attack': 0, 'win_condition': True, 'image': 'flag.png'},
            'knife': {'health': 0, 'attack': 2, 'range': 2, 'image': 'knife.png'}
        }
        
    def _get_items_on_map(self):
        """
        Scannt die Karte nach vorhandenen Objekten und speichert deren Position und Typ.
        """
        items = {}
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell not in ['#', '.']:
                    items[(x, y)] = cell
        return items

    def get_item_value(self, item_name):
        """
        Gibt die definierten Werte für ein bestimmtes Objekt zurück.
        """
        return self.item_properties.get(item_name, None)

    def get_player_health(self, player_id):
        """
        Gibt die aktuelle Gesundheit eines Spielers zurück.
        """
        return self.player_data[player_id]['health']

    def get_player_position(self, player_id):
        """
        Gibt die aktuelle Position eines Spielers zurück.
        """
        return self.player_data[player_id]['position']

    def get_state_for_ki(self, player_id):
        """
        Bereitet den Spielzustand so auf, dass er von der KI einfach verarbeitet werden kann.
        """
        # Beispiel: Flache Liste von Werten, die als Input für ein neuronales Netz dient
        state = []
        
        # Eigene Gesundheit und Position hinzufügen
        state.append(self.get_player_health(player_id))
        state.extend(self.get_player_position(player_id))
        
        # Position des Teammitglieds hinzufügen
        # (Annahme: wir können das Teammitglied identifizieren)
        # state.extend(self.player_data[team_mate_id]['position'])

        # Positionen und Werte aller Objekte auf der Karte hinzufügen
        for pos, item in self.items_on_map.items():
            state.extend(pos)
            item_values = self.get_item_value(item)
            if item_values:
                state.append(item_values.get('health', 0))
                state.append(item_values.get('attack', 0))

        # Weitere relevante Informationen (z.B. Gegnerpositionen) hinzufügen
        
        return state
