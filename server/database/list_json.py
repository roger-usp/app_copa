import os
import json

def is_valid_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json.load(file)
        return True
    except (ValueError, json.JSONDecodeError) as error:
        return False


def validate_files(directory, files):
    directory = directory[:-1] if directory[-1] == "/" else directory
    valid_files = []
    for file_name in files:
        if not file_name.endswith(".json"):
            continue
        
        file_path = f"{directory}/{file_name}"
        if is_valid_json(file_path):
            valid_files.append(file_name)

    return valid_files


def list_files(directory):
    files = os.listdir(directory)
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
    valid_files = validate_files(directory, files)
    return valid_files







