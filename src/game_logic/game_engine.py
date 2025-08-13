import random

def place_objects_on_map(map_data, objects_to_place):
    """
    Platziert Objekte zufällig auf der Karte.

    Args:
        map_data (list of list): Die 2D-Liste, die die Karte darstellt.
        objects_to_place (list): Eine Liste von Objektnamen oder -typen.
    """
    map_height = len(map_data)
    map_width = len(map_data[0]) if map_height > 0 else 0
    
    empty_positions = []
    for y in range(map_height):
        for x in range(map_width):
            if map_data[y][x] == ' ': # ' ' steht für eine leere Position
                empty_positions.append((x, y))

    random.shuffle(empty_positions)
    
    for i, obj in enumerate(objects_to_place):
        if i < len(empty_positions):
            x, y = empty_positions[i]
            map_data[y][x] = obj
            print(f"Objekt '{obj}' wurde bei Position ({x}, {y}) platziert.")
        else:
            print(f"Warnung: Nicht genug Platz für alle Objekte. '{obj}' konnte nicht platziert werden.")

# Beispiel für die Verwendung
# Die Karte könnte so aussehen:
# maze_map = [
#     ['#', '#', '#', '#', '#'],
#     ['#', ' ', ' ', ' ', '#'],
#     ['#', ' ', '#', ' ', '#'],
#     ['#', ' ', ' ', ' ', '#'],
#     ['#', '#', '#', '#', '#']
# ]

# objects = ['flag', 'weapon', 'pill']
# place_objects_on_map(maze_map, objects)
