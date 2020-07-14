# -- External Packages -- #
import threading
import time
import json
import os
from pathlib import Path

# -- Project Defined Imports -- #
from backend import constants

class DataLogger(threading.Thread):
    def __init__(self, username: str, get_data_func, path_to_project_root: Path):
        """:brief Responsible for logging all existing data to an external file. Updates the file once every thread period
        \n:param get_data_func - A function that is capable of getting the current data from time_manager.py
        """
        # threading defines
        threading.Thread.__init__(self)
        self._thread_status = threading.Event() # Its isSet() can be used to check if thread has closed
        self._worker = threading.Thread(target = self.__thread_function)
        self._worker.daemon = True
    
        # Save inputs to class
        self._username = username
        self._get_data_func = get_data_func
        self._path_to_project_root = path_to_project_root

        # Class Variables
        self._path_to_json_dir = constants.RESULT_DATA_DIR_PATH.joinpath(self._username)
        self._path_to_json = self._path_to_json_dir.joinpath(constants.DATA_JSON_NAME)

        # TODO: Decide if this call should be moved to backend controller / under which cases it gets called
        self.start_thread()
        

    #####################
    # Public Functions  #
    #####################
    def start_thread(self):
        """:Note Clears any previously existing status flags and starts the worker"""
        self._thread_status.clear()
        self._worker.start()

    def stop_thread(self):
        """Close down the thread safetly and make sure the worker stops running"""
        # Thread worker will not be allowed to run
        self._thread_status.set()
        self._worker.join()

    def get_data_in_file(self) -> dict():
        """:brief Function used on startup of the system to get the data stored in the file
        :Note This function should ONLY be called once per user
        :return - The data from the data json
        """
        data = dict()
        with open(self._path_to_json, 'r') as json_file:
            data = json.load(json_file)
        return data

    ######################
    # Private Functions  #
    ######################
    def __thread_function(self):
        """:Note Worker function - DO NOT call this function anywhere
        \n:brief - On worker wakeup, periodically writes the contents of the applications data to a json
        """
        while not self._thread_status.isSet():
            # This controls the thread period / how often it runs
            time.sleep(constants.LOGGER_THREAD_PERIOD)
            current_data = self._get_data_func()
            self._write_data(current_data)

    def _write_data(self, data_to_write: dict()):
        """:brief writes the data to the file"""
        
        if self._path_to_json.exists() is False:
            self._path_to_json_dir.mkdir(parents=True, exist_ok=True)

        with open(self._path_to_json, 'w') as json_file:
            json.dump(data_to_write, json_file, indent=4)