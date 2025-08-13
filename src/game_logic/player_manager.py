import time

class PlayerManager:
    """
    Verwaltet das Spawnen und Respawn von Spielern auf der Karte.
    """
    def __init__(self, map_data, teams_config, base_managers):
        self.map_data = map_data
        self.teams_config = teams_config  # Format: {'blue': [agent1, agent2], 'red': [agent3, agent4]}
        self.base_managers = base_managers # Format: {'blue': BaseManager, 'red': BaseManager}
        self.player_positions = {}
        self.respawn_timers = {}

    def initial_spawn(self):
        """Platziert alle Soldaten am Anfang des Spiels."""
        for team, players in self.teams_config.items():
            base_manager = self.base_managers.get(team)
            if base_manager:
                base_pos = base_manager.position
                for player in players:
                    self.player_positions[player.name] = base_pos
                    self.respawn_timers[player.name] = 0
                    print(f"Soldat {player.name} von Team {team} wurde bei {base_pos} gespawnt.")
        
        self._inform_agents_of_spawn()

    def handle_death(self, player_name, cause_of_death):
        """Startet den Respawn-Timer nach einem Tod."""
        respawn_time = 5  # Standard-Respawn-Zeit
        if cause_of_death == 'nuke':
            respawn_time = 15
        
        self.respawn_timers[player_name] = time.time() + respawn_time
        print(f"Soldat {player_name} ist gestorben. Respawn in {respawn_time} Sekunden.")

    def update_respawns(self):
        """Überprüft und führt Respawn durch, wenn die Basis noch aktiv ist."""
        current_time = time.time()
        
        for player_name, respawn_time in self.respawn_timers.items():
            if respawn_time > 0 and current_time >= respawn_time:
                team = self._get_player_team(player_name)
                base = self.base_managers.get(team)
                
                if base and base.is_active:
                    base_pos = base.position
                    self.player_positions[player_name] = base_pos
                    self.respawn_timers[player_name] = 0
                    print(f"Soldat {player_name} wurde bei {base_pos} respawned.")
                    self._inform_agents_of_respawn(player_name)
                else:
                    print(f"Soldat {player_name} kann nicht respawnen, da die Basis von Team {team} zerstört ist!")

    def _get_player_team(self, player_name):
        """Findet das Team eines Spielers anhand des Namens."""
        for team, agents in self.teams_config.items():
            for agent in agents:
                if agent.name == player_name:
                    return team
        return None
    
    def get_all_player_positions(self):
        """Gibt die aktuellen Positionen aller Spieler zurück."""
        return self.player_positions
    
    def _inform_agents_of_spawn(self):
        # TODO: Implementiere die Logik, um die Agenten über ihre Startpositionen zu informieren
        pass

    def _inform_agents_of_respawn(self, player_name):
        # TODO: Implementiere die Logik, um die Agenten über ihren Respawn zu informieren
        pass
