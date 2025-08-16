import time

class Soldier:
    """
    Repräsentiert einen einzelnen Soldaten im Spiel.
    """
    def __init__(self, team, soldier_id, start_position):
        self.team = team
        self.soldier_id = soldier_id
        self.position = start_position
        self.start_position = start_position
        self.health = 25
        self.attack = 1
        self.vision_range = 2
        self.is_alive = True
        self.last_death_time = 0
        self.respawn_delay = 5  # Sekunden
        self.inventory = {} # Inventar für gesammelte Waffen

    def take_damage(self, amount):
        """
        Reduziert die Gesundheit des Soldaten und überprüft, ob er tot ist.
        """
        self.health -= amount
        if self.health <= 0:
            self.is_alive = False
            self.last_death_time = time.time()
            print(f"Soldat {self.soldier_id} von Team {self.team} wurde getötet.")

    def update(self):
        """
        Aktualisiert den Zustand des Soldaten (z.B. Respawn-Timer).
        """
        if not self.is_alive:
            if time.time() - self.last_death_time >= self.respawn_delay:
                self.respawn()

    def respawn(self):
        """
        Setzt den Soldaten auf seine Basis zurück und stellt seine Anfangswerte wieder her.
        """
        self.is_alive = True
        self.health = 25
        self.attack = 1
        self.position = self.start_position
        self.inventory = {}  # Inventar wird geleert
        self.vision_range = 2 # Sichtweite wird zurückgesetzt
        print(f"Soldat {self.soldier_id} von Team {self.team} ist respawned.")

    def collect_item(self, item_type, item_properties):
        """
        Ein Soldat sammelt ein Objekt ein und passt seine Attribute an.
        """
        if item_type in ['knife', 'gun', 'grenade', 'nuke']:
            # Waffen werden gesammelt und der Angriffswert wird überschrieben
            self.inventory['weapon'] = item_type
            self.attack = item_properties.get('attack', 1)
            print(f"Soldat {self.soldier_id} hat {item_type} gesammelt. Neuer Angriff: {self.attack}")
        elif item_type == 'binoculars':
            # Fernglas erweitert die Sichtweite
            self.vision_range += item_properties.get('vision_boost', 0)
            self.inventory['binoculars'] = True
            print(f"Soldat {self.soldier_id} hat ein Fernglas gesammelt. Neue Sichtweite: {self.vision_range}")
        elif item_type == 'red pill':
            # Rote Pille erhöht die Gesundheit
            self.health += item_properties.get('health', 0)
            print(f"Soldat {self.soldier_id} hat eine rote Pille gesammelt. Neue Gesundheit: {self.health}")
        elif item_type == 'blue pill':
            # Blaue Pille erhöht die Gesundheit
            self.health += item_properties.get('health', 0)
            print(f"Soldat {self.soldier_id} hat eine blaue Pille gesammelt. Neue Gesundheit: {self.health}")
        elif item_type == 'flag':
            # Flagge wird gesammelt
            self.inventory['flag'] = True
            print(f"Soldat {self.soldier_id} hat die Flagge gesammelt!")
        elif item_type == 'fake_flag':
            # Falsche Flagge wird gesammelt
            self.inventory['fake_flag'] = True
            print(f"Soldat {self.soldier_id} hat eine falsche Flagge gesammelt.")
        elif item_type == 'pink duck':
            # Pinke Ente wird gesammelt
            self.inventory['pink duck'] = True
            print(f"Soldat {self.soldier_id} hat eine pinke Ente gesammelt.")

    def lose_flag(self):
        """
        Entfernt die Flagge aus dem Inventar des Soldaten.
        """
        if 'flag' in self.inventory:
            del self.inventory['flag']
            return True
        return False