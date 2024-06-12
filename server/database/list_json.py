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


def get_info_list(directory):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    directory = directory[:-1] if directory[-1] == "/" else directory
    directory = os.path.join(script_dir, *directory.split("/"))

    valid_files = list_files(directory)
    info_list = []
    for filename in valid_files:
        info_element = {}
        with open(f"{directory}/{filename}", "r") as f:
            file_content = json.load(f)

        option_value = filename[:-5]  # removes .json from the end
        info_element["optionValue"] = option_value

        if "legend" in file_content.keys():
            info_element["optionInnerHTML"] = file_content["legend"]

        elif "value_title" in file_content.keys():
            info_element["optionInnerHTML"] = file_content["value_title"]

        if "optgroup" in file_content.keys():
            optgroup = file_content["optgroup"]
            info_element["optgroupLabel"] = optgroup
        
        info_list.append(info_element)
    
    return info_list


        
