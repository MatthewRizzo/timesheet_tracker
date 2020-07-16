"""File that stores class unaffiliated functions to be used elsewhere"""
import json
import os
import pathlib
import sys
import platform
import re
import subprocess
import socket   # Used to determine local network IP that can be accessed

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

def is_running_windows() -> bool:
    """:return - True if running on widnows, False otherwise"""
    platform_in_use = platform.system()
    return platform_in_use == "Windows"

def is_running_linux():
    """:return - True if running on Linux, False otherwise"""
    platform_in_use = platform.system()
    return platform_in_use == "Linux"

def get_ip_addr():
    """:return Your computer's IP address that can be used by your router.
    \n:note - Especially needed when deploying to a server with an exposed port"""
    if is_running_windows():
        hostname = socket.gethostname()
        IP_addr = socket.gethostbyname(hostname)
        return IP_addr

    elif is_running_linux():
        ip_expression = r'inet ([^.]+.[^.]+.[^.]+.[^\s]+)'
        output = subprocess.check_output("ifconfig").decode()
        matches = re.findall(ip_expression, output)

        # Might have multiple ip loops running. It depends on system setup. Account for that.
        # The router only has access to the one starting with 192.168
        # https://qr.ae/pNs807
        potential_matches = lambda match: match.startswith("192.168.")
        IP_addr = list(filter(potential_matches, matches))[0]
        return IP_addr

def create_site_url(ip: str, extension: str, port: str) -> str:
    """:brief Given the url extension after http://ip:, returns the complete url for that site"""
    url = f"http://{ip}:{port}{extension}"
    return url