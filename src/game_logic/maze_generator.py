import random

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [['#' for _ in range(self.width)] for _ in range(self.height)]
        self.walls = []

    def _add_walls(self, x, y):
        # Fügt alle umliegenden Wände zur Liste hinzu
        if y > 1 and self.maze[y-2][x] == '#':
            self.walls.append((x, y-1))
        if y < self.height - 2 and self.maze[y+2][x] == '#':
            self.walls.append((x, y+1))
        if x > 1 and self.maze[y][x-2] == '#':
            self.walls.append((x-1, y))
        if x < self.width - 2 and self.maze[y][x+2] == '#':
            self.walls.append((x+1, y))

    def generate(self):
        # Wählt einen zufälligen Startpunkt
        start_x = random.randrange(1, self.width, 2)
        start_y = random.randrange(1, self.height, 2)
        
        # Setzt den Startpunkt als Pfad und fügt seine Wände hinzu
        self.maze[start_y][start_x] = ' '
        self._add_walls(start_x, start_y)
        
        while self.walls:
            # Wählt eine zufällige Wand aus
            wall_x, wall_y = random.choice(self.walls)
            self.walls.remove((wall_x, wall_y))
            
            # Findet die Zelle jenseits der Wand
            if wall_y > 0 and self.maze[wall_y-1][wall_x] == ' ': # Wand oben
                neighbor_x, neighbor_y = wall_x, wall_y+1
            elif wall_y < self.height-1 and self.maze[wall_y+1][wall_x] == ' ': # Wand unten
                neighbor_x, neighbor_y = wall_x, wall_y-1
            elif wall_x > 0 and self.maze[wall_y][wall_x-1] == ' ': # Wand links
                neighbor_x, neighbor_y = wall_x+1, wall_y
            elif wall_x < self.width-1 and self.maze[wall_y][wall_x+1] == ' ': # Wand rechts
                neighbor_x, neighbor_y = wall_x-1, wall_y
            else:
                continue

            # Wenn die Nachbarzelle nicht besucht wurde, bricht die Wand durch
            if self.maze[neighbor_y][neighbor_x] == '#':
                self.maze[wall_y][wall_x] = ' '
                self.maze[neighbor_y][neighbor_x] = ' '
                self._add_walls(neighbor_x, neighbor_y)
        
        # Gibt das generierte Labyrinth als Liste von Zeilen zurück
        return ["".join(row) for row in self.maze]