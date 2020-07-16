"""File that stores class unaffiliated functions to be used elsewhere"""
import json
import pathlib

def load_json(path_to_json: pathlib.Path) -> dict:
    """:brief given a path, opens a json file, and returns its contents as a dict
    \n:param `path_to_json` - The path to the json to be opened
    \n:return The contents of the json
    """
    with open(path_to_json, 'r') as data_file:
        data = json.load(data_file)
    return data

def write_to_json(path_to_json: pathlib.Path, json_data: dict, indent=4):
    """:brief given a path, opens a json file, and writes the contents of json_data to it"""
    with open(path_to_json, 'w') as write_file:
        json.dump(json_data, write_file, indent=indent)

def get_project_root_path() -> pathlib.Path:
    """:return - Path absolute path to project root"""
    # Includes the file name
    path_to_current_file = pathlib.Path(__file__) 
    
    # Need to go up 2 dirs + 1 file to get to project root
    file_path_no_filename = path_to_current_file.parent
    file_path_to_root = file_path_no_filename.parent.parent 
    return file_path_to_root