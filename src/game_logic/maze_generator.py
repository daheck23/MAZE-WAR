import random
import os

class MazeGenerator:
    """
    Eine Klasse, die Methoden zum Generieren und Speichern von Labyrinthen bereitstellt.
    """
    @staticmethod
    def generate_maze(width, height):
        """
        Generiert ein Labyrinth mit leeren Feldern ('.') und Wänden ('#').
        
        Args:
            width (int): Die Breite des Labyrinths.
            height (int): Die Höhe des Labyrinths.
            
        Returns:
            list: Eine Liste von Listen, die das Labyrinth darstellt.
        """
        # Sicherstellen, dass die Dimensionen ungerade sind, da das Algorithmus-Design darauf basiert
        width = width if width % 2 != 0 else width + 1
        height = height if height % 2 != 0 else height + 1

        # Erstelle ein Gitter, das vollständig aus Wänden besteht
        maze = [['#' for _ in range(width)] for _ in range(height)]
        
        def carve_path(x, y):
            """
            Rekursiver Backtracking-Algorithmus zur Erstellung des Labyrinths.
            """
            # Setze die aktuelle Zelle als Weg
            maze[y][x] = '.'

            # Erstelle eine zufällige Liste von Richtungen
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2

                # Überprüfe, ob die neue Zelle innerhalb der Grenzen liegt und eine Wand ist
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == '#':
                    # Schlage einen Gang zwischen der aktuellen und der neuen Zelle
                    maze[y + dy][x + dx] = '.'
                    # Rufe die Funktion rekursiv für die neue Zelle auf
                    carve_path(nx, ny)

        # Beginne mit dem Schnitzen von einem zufälligen ungeraden Startpunkt
        start_x = random.randrange(1, width, 2)
        start_y = random.randrange(1, height, 2)
        carve_path(start_x, start_y)
        
        return maze

    @staticmethod
    def save_map(maze, file_path):
        """
        Speichert das generierte Labyrinth in einer .map-Datei.
        
        Args:
            maze (list): Die Labyrinth-Daten.
            file_path (str): Der Pfad, unter dem die Datei gespeichert werden soll.
        """
        with open(file_path, 'w') as f:
            for row in maze:
                f.write(''.join(row) + '\n')
        print(f"Labyrinth-Karte erfolgreich gespeichert unter: {file_path}")

if __name__ == "__main__":
    # Pfade für die Speicherung der Karte festlegen
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
    maps_dir = os.path.join(assets_dir, 'maps')
    
    if not os.path.exists(maps_dir):
        os.makedirs(maps_dir)
        print(f"Verzeichnis erstellt: {maps_dir}")

    # Beispiel für die Generierung und Speicherung einer 25x25-Karte
    map_width = 25
    map_height = 25
    map_filename = f"{map_width}x{map_height}_maze.map"
    map_path = os.path.join(maps_dir, map_filename)
    
    print(f"Generiere eine {map_width}x{map_height} Labyrinth-Karte...")
    new_maze = MazeGenerator.generate_maze(map_width, map_height)
    
    MazeGenerator.save_map(new_maze, map_path)
