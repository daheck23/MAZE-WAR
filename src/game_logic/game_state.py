import random
import numpy as np

class GameState:
    def __init__(self, maze_data, team_count=2):
        self.maze_data = maze_data
        self.team_count = team_count
        self.teams = self.initialize_teams()

    def initialize_teams(self):
        team_names = ["Team Red", "Team Blue", "Team Pink", "Team Green", "Team Gold"]
        team_colors = {
            "Team Red": (255, 0, 0),
            "Team Blue": (0, 0, 255),
            "Team Pink": (255, 105, 180),
            "Team Green": (0, 128, 0),
            "Team Gold": (255, 215, 0)
        }
        
        selected_teams = {}
        shuffled_team_names = random.sample(team_names, self.team_count)
        
        for name in shuffled_team_names:
            selected_teams[name] = {
                'color': team_colors[name],
                'position': None,
                'score': 0
            }
        
        self.set_random_base_positions(selected_teams)
        
        return selected_teams

    def set_random_base_positions(self, teams):
        open_positions = self.find_open_positions()
        
        if len(open_positions) < len(teams):
            print("Nicht genügend freie Positionen für alle Teams.")
            return

        assigned_positions = []
        for team_name in teams:
            valid_position_found = False
            for _ in range(1000): # Versuche, eine gültige Position zu finden
                position = random.choice(open_positions)
                if self.is_position_valid(position, assigned_positions):
                    teams[team_name]['position'] = position
                    assigned_positions.append(position)
                    open_positions.remove(position) # Position aus der Liste der möglichen Positionen entfernen
                    valid_position_found = True
                    break
            
            if not valid_position_found:
                print(f"Konnte keine gültige Position für {team_name} finden. Generierung fehlgeschlagen.")
                # Hier könnte man eine Fehlerbehandlung hinzufügen
                return

    def is_position_valid(self, new_position, assigned_positions):
        x1, y1 = new_position
        for x2, y2 in assigned_positions:
            distance_sq = (x1 - x2)**2 + (y1 - y2)**2
            if distance_sq < 3**2: # Mindestabstand von 3
                return False
        return True

    def find_open_positions(self):
        # Find all path cells (value 0) in the maze
        path_cells = np.argwhere(self.maze_data == 0)
        
        # Convert to a list of tuples (x, y)
        return [(cell[1], cell[0]) for cell in path_cells]
