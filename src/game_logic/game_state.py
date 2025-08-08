import random
import numpy as np

class GameState:
    def __init__(self, maze_data, team_count):
        self.maze = maze_data
        self.width = maze_data.shape[1]
        self.height = maze_data.shape[0]
        self.teams = {}
        self.objects = []
        self.flag = None
        self.initialize_teams(team_count)
        self.set_random_base_positions()
        
        self.max_objects = int((self.width * self.height) / 50)
        
        self.object_spawn_config = {
            'knife': {'frequency': 40, 'max_on_map': 5},
            'gun': {'frequency': 30, 'max_on_map': 3},
            'grenade': {'frequency': 20, 'max_on_map': 2},
            'nuke': {'frequency': 1, 'max_on_map': 1},
            'bonus': {'frequency': 5, 'max_on_map': 10},
        }

        self._place_initial_objects()

    def initialize_teams(self, team_count):
        team_colors = [
            (255, 0, 0),
            (0, 0, 255),
            (0, 255, 0),
            (255, 192, 203),
            (255, 255, 0),
            (128, 0, 128)
        ]
        team_names = ["Team Red", "Team Blue", "Team Green", "Team Pink", "Team Gold", "Team Purple"]
        
        for i in range(team_count):
            self.teams[team_names[i]] = {
                'score': 0,
                'color': team_colors[i],
                'base_position': None,
                'position': None,
                'team_members': []
            }

    def find_open_positions(self):
        occupied_positions = set()
        
        for team_name in self.teams:
            if self.teams[team_name]['base_position'] is not None:
                occupied_positions.add(self.teams[team_name]['base_position'])
        
        for obj in self.objects:
            occupied_positions.add(obj['position'])

        if self.flag is not None:
            occupied_positions.add(self.flag['position'])
            
        path_positions = np.argwhere(self.maze == 0).tolist()
        
        free_positions = [tuple(pos) for pos in path_positions if tuple(pos) not in occupied_positions]
        
        return free_positions

    def set_random_base_positions(self):
        print(f"Versuche, Basen für {len(self.teams)} Teams zu platzieren...")
        free_positions = self.find_open_positions()
        
        if len(free_positions) < len(self.teams):
            raise ValueError("Nicht genügend freie Plätze für alle Teams.")

        base_positions = random.sample(free_positions, len(self.teams))
        
        for i, (team_name, team_data) in enumerate(self.teams.items()):
            team_data['base_position'] = base_positions[i]
            team_data['position'] = base_positions[i]
            print(f"Basis für {team_name} gesetzt bei Position: {team_data['base_position']}")

    def _place_initial_objects(self):
        self._place_flag()
        
        num_initial_objects = int(self.max_objects / 2)
        for _ in range(num_initial_objects):
            self.place_object()

    def _place_flag(self):
        if self.flag is None:
            free_positions = self.find_open_positions()
            if free_positions:
                new_pos = random.choice(free_positions)
                self.flag = {'type': 'flag', 'position': new_pos}

    def place_object(self, is_bonus_spawn=False):
        free_positions = self.find_open_positions()
        current_object_count = len(self.objects)
        
        if not free_positions or current_object_count >= self.max_objects:
            return
            
        if is_bonus_spawn:
            new_pos = random.choice(free_positions)
            self.objects.append({'type': 'bonus', 'position': new_pos})
            return

        spawn_pool = []
        for obj_type, config in self.object_spawn_config.items():
            if obj_type != 'bonus':
                spawn_pool.extend([obj_type] * config['frequency'])
        
        if not spawn_pool:
            return

        object_to_spawn = random.choice(spawn_pool)
        
        if self.get_object_counts()[object_to_spawn] >= self.object_spawn_config[object_to_spawn]['max_on_map']:
            return
        
        new_pos = random.choice(free_positions)
        self.objects.append({'type': object_to_spawn, 'position': new_pos})

    def get_object_counts(self):
        counts = {obj_type: 0 for obj_type in self.object_spawn_config}
        for obj in self.objects:
            counts[obj['type']] += 1
        return counts