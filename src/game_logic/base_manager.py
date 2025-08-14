import time

class BaseManager:
    """
    Verwaltet die Logik für eine einzelne Basis, einschließlich Gesundheit,
    Verteidigung und Kommunikation mit den eigenen Agenten.
    """
    def __init__(self, team_name, start_position, team_agents, map_data):
        self.team_name = team_name
        self.position = start_position
        self.health = 150
        self.is_active = True
        self.team_agents = team_agents # Liste der KI-Agenten dieses Teams
        self.map_data = map_data
        self.vision_range = 4 # Sichtweite in Steps
        self.last_warning_time = 0 # Zeitstempel für letzte Warnung
        self.warning_cooldown = 10 # Sekunden

    def take_damage(self, damage_amount, damage_type='normal'):
        """
        Verringert die Gesundheit der Basis.
        Berücksichtigt eine Schadensbegrenzung für Nukes.
        """
        if not self.is_active:
            return 0 # Basis ist bereits zerstört

        if damage_type == 'nuke' and damage_amount > 100:
            damage_amount = 100 # Max. 100 Schaden durch eine Nuke

        self.health -= damage_amount
        print(f"Basis von Team {self.team_name} erleidet {damage_amount} Schaden. Neue Health: {self.health}")

        if self.health <= 0:
            self.is_active = False
            print(f"Basis von Team {self.team_name} wurde zerstört!")
            return 100 # Punkte für das Zerstören der Basis
        
        return 0

    def check_for_enemies(self, all_player_positions):
        """
        Sucht innerhalb der Sichtweite nach feindlichen Spielern.
        """
        if not self.is_active:
            return False

        current_time = time.time()
        if (current_time - self.last_warning_time) < self.warning_cooldown:
            return False # Cooldown aktiv, keine neue Warnung senden
        
        base_x, base_y = self.position
        
        for player_name, pos in all_player_positions.items():
            player_x, player_y = pos
            distance = ((player_x - base_x)**2 + (player_y - base_y)**2)**0.5
            
            # Prüft die Entfernung und ob der Spieler nicht zum eigenen Team gehört
            if distance <= self.vision_range and self._get_player_team(player_name) != self.team_name:
                print(f"Basis von Team {self.team_name} hat einen Feind gesichtet!")
                self._warn_team_members(player_name)
                self.last_warning_time = current_time
                return True
        return False
    
    def _warn_team_members(self, enemy_name):
        """
        Sendet eine Warnung an alle Agenten des eigenen Teams.
        """
        for agent in self.team_agents:
            message = f"Dringend! Unsere Basis wird von {enemy_name} angegriffen! Kehrt sofort zur Verteidigung zurück!"
            agent.send_message(agent.team_mate, message)
            
    def _get_player_team(self, player_name):
        # Hilfsfunktion, um das Team eines Spielers anhand des Namens zu finden
        for agent in self.team_agents:
            if agent.name == player_name:
                return self.team_name
        # Annahme: der gegnerische Agent befindet sich im `all_player_positions` Dict
        # Diese Logik müsste erweitert werden, um das Team des Gegners zu finden.
        return 'opponent'