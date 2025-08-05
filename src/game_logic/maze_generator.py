
import numpy as np
import random

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # 0: Wall, 1: Path
        self.maze = np.ones((height * 2 + 1, width * 2 + 1), dtype=int)
        self.visited = np.zeros((height, width), dtype=bool)

    def generate(self):
        self.carve_paths_from(0, 0)
        return self.maze

    def carve_paths_from(self, x, y):
        self.visited[y, x] = True
        
        # Directions: 0: up, 1: right, 2: down, 3: left
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= ny < self.height and 0 <= nx < self.width and not self.visited[ny, nx]:
                # Carve path in the maze grid
                self.maze[2 * y + 1 + dy, 2 * x + 1 + dx] = 0
                self.maze[2 * ny + 1, 2 * nx + 1] = 0
                
                self.carve_paths_from(nx, ny)

if __name__ == "__main__":
    # Example usage:
    maze_gen = MazeGenerator(20, 20)
    maze_array = maze_gen.generate()
    
    # Print the maze (0=path, 1=wall)
    for row in maze_array:
        print("".join(["#" if cell == 1 else " " for cell in row]))
