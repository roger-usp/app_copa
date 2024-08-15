import os
import json

POINTS_TO_KEEP = [
    "centros_operativos.json",
    "depositos.json",
    "capitais_brasileiras.json",
    "portos.json"
]


def get_csv_to_keep(info_path, to_keep_list):
    # to_keep_list should be ARROWS_TO_KEEP or POINTS_TO_KEEP
    csv_to_keep = []
    for filename in to_keep_list:
        file_path = os.path.join(info_path, filename)

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                info_dict = json.load(file)

            csv_filename = info_dict["data_path"]
            csv_to_keep.append(csv_filename)
    
    return csv_to_keep



def delete_files_except(directory, files_to_keep):
    # Convert list of files to keep to a set for faster lookups
    files_to_keep_set = set(files_to_keep)
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if filename not in files_to_keep_set and os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                raise Exception(f"Error deleting {filename}: {e}")

    return



def delete_previous_runs(points_to_keep):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    database_dir = os.path.join(parent_dir, 'server', 'database')
    arrows_path = os.path.join(database_dir, 'arrows')
    points_path = os.path.join(database_dir, 'points')
    
    points_info_path = os.path.join(points_path, "info")
    points_data_path = os.path.join(points_path, "data")
    points_csv_to_keep = get_csv_to_keep(points_info_path, points_to_keep)
    delete_files_except(points_info_path, points_to_keep)
    delete_files_except(points_data_path, points_csv_to_keep)

    arrows_info_path = os.path.join(arrows_path, "info")
    arrows_data_path = os.path.join(arrows_path, "data")
    delete_files_except(arrows_info_path, [])
    delete_files_except(arrows_data_path, [])
    return
    



