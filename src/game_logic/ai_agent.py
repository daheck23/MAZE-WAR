import collections
import random

class AIAgent:
    def __init__(self, game_state):
        self.game_state = game_state

    def get_move(self, soldier):
        """
        Berechnet den nächsten Schritt für den Soldaten mithilfe der Breitensuche (BFS),
        um das nächstgelegene Item zu erreichen.
        """
        if not soldier.is_alive:
            return soldier.position

        start_pos = soldier.position
        
        closest_item_pos = self._find_closest_item(start_pos)

        if closest_item_pos:
            path = self._find_path(start_pos, closest_item_pos)
            
            if path and len(path) > 1:
                return path[1]

        return self._get_random_valid_move(start_pos)

    def _find_closest_item(self, start_pos):
        """Findet die Position des nächstgelegenen Items auf der Karte."""
        min_distance = float('inf')
        closest_item = None
        
        items_on_map = self.game_state.items_on_map

        for item_pos in items_on_map.keys():
            dist = abs(item_pos[0] - start_pos[0]) + abs(item_pos[1] - start_pos[1])
            if dist < min_distance:
                min_distance = dist
                closest_item = item_pos
        
        return closest_item

    def _find_path(self, start_pos, target_pos):
        """Führt eine Breitensuche (BFS) durch, um den kürzesten Pfad zu finden."""
        q = collections.deque([[start_pos]])
        visited = {start_pos}
        map_data = self.game_state.map_data
        
        while q:
            path = q.popleft()
            current_pos = path[-1]

            if current_pos == target_pos:
                return path

            x, y = current_pos
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                new_pos = (new_x, new_y)

                if self._is_valid_move(new_x, new_y) and new_pos not in visited:
                    visited.add(new_pos)
                    new_path = list(path)
                    new_path.append(new_pos)
                    q.append(new_path)
        
        return None

    def _get_random_valid_move(self, current_pos):
        """Findet eine zufällige, gültige Bewegung, falls die Pfadfindung fehlschlägt."""
        x, y = current_pos
        possible_moves = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if self._is_valid_move(new_x, new_y):
                possible_moves.append((new_x, new_y))
        
        return random.choice(possible_moves) if possible_moves else current_pos

    def _is_valid_move(self, x, y):
        """Überprüft, ob eine Bewegung gültig ist (innerhalb der Karte, keine Mauer)."""
        map_data = self.game_state.map_data
        if not (0 <= y < len(map_data) and 0 <= x < len(map_data[y])):
            return False
        return map_data[y][x] != '#' and map_data[y][x] != '\n'