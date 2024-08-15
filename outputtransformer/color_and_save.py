from random import shuffle, randint
import json
import os

def get_colors():
    return [
    "#00ff00",  # Lime Green
    "#0000ff",  # Blue
    "#00ffff",  # Cyan
    "#8a2be2",  # Blue Violet
    "#7fffd4",  # Aquamarine
    "#9932cc",  # Dark Orchid
    "#1e90ff",  # Dodger Blue
    "#2e8b57",  # Sea Green
    "#3cb371",  # Medium Sea Green
    "#4682b4",  # Steel Blue
    "#6a5acd",  # Slate Blue
    "#483d8b",  # Dark Slate Blue
    "#40e0d0",  # Turquoise
    "#191970",  # Midnight Blue
    "#7b68ee",  # Medium Slate Blue
    "#006400",  # Dark Green
    "#556b2f",  # Dark Olive Green
    "#6495ed",  # Cornflower Blue
]


def get_random_hex_color():
    # Generate a random integer between 0 and 0xFFFFFF (16777215 in decimal)
    random_color = randint(0, 0xFFFFFF)
    # Format the integer as a hex string, padded with zeros if necessary, and prepend with #
    hex_color = f'#{random_color:06X}'
    return hex_color


def color_info(colorless_dict):
    color_list = get_colors().copy()
    shuffle(color_list)

    colored_dict = {}

    item_idx = 0
    for k, v in colorless_dict.items():
        data, info = v
        try:
            info["color"] = color_list[item_idx]
        except IndexError:
            info["color"] = get_random_hex_color()

        colored_dict[k] = [data, info]
        item_idx += 1
    
    return colored_dict



def get_path(arrows, points):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    database_dir = os.path.join(parent_dir, 'server', 'database')

    if arrows and points:
        raise Exception("arrows and points can't be True at the same time")
    
    elif (not arrows) and (not points):
        raise Exception("kwargs arrows or points must be True")

    elif arrows:
        path = os.path.join(database_dir, 'arrows')
    
    else:
        path = os.path.join(database_dir, 'points')
    
    return path



def save_colored_dict(colored_dict, arrows=False, points=False):
    path = get_path(arrows, points)
    
    for k,v in colored_dict.items():
        data, info = v
        json_filename = f"{k}.json"
        json_path = os.path.join(path,"info",json_filename)

        with open(json_path, "w") as f:
            json.dump(info, f)
        
        csv_path = os.path.join(path,"data",info["data_path"])
        data.to_csv(csv_path, index=False)
    
    




