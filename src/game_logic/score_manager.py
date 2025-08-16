import time

class ScoreManager:
    def __init__(self, teams):
        self.scores = {team: 0 for team in teams}
        self.round_start_time = time.time()
        self.round_duration = 300  # Rundenzeit in Sekunden (5 Minuten)
        self.points = {
            'flag_collect': 25,
            'flag_return': 50,
            'friendly_fire': -3,
            'suicide': -5,
            'kill': 5,
            'pink_duck': 3,
            'base_destroyed': 100
        }

    def add_points(self, team, reason):
        """Fügt einem Team Punkte hinzu, basierend auf dem Grund."""
        if reason in self.points:
            points_to_add = self.points[reason]
            self.scores[team] += points_to_add
            print(f"Team {team} bekommt {points_to_add} Punkte für {reason}. Neuer Stand: {self.scores[team]}")

    def get_current_scores(self):
        """Gibt die aktuellen Punktestände zurück."""
        return self.scores

    def get_time_left(self):
        """Gibt die verbleibende Rundenzeit zurück."""
        elapsed_time = time.time() - self.round_start_time
        time_left = self.round_duration - elapsed_time
        return max(0, int(time_left))
        
    def reset_round(self, teams):
        """Setzt die Punkte und den Timer für eine neue Runde zurück."""
        self.scores = {team: 0 for team in teams}
        self.round_start_time = time.time()
        print("Runde zurückgesetzt. Neue Runde startet.")