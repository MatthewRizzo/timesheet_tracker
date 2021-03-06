# -- External Packages -- #
import pathlib

# -- Project Defined Imports -- #
from backend import constants
from backend.data_logger import DataLogger
from backend.time_manager import TimeManager

class BackendController():
    def __init__(self, send_to_client, username: str):
        """:brief Class to provide wrappers over the entire backend capability. Each user will get their own BackendController
        \n:param send_to_client - The function from app_manager capable of sending messages up a socket to the frontend
        """
        self.send_to_client = send_to_client
        self._mode = "law" # TODO: make this an input to the file
        self._username = username

        self._path_to_project_root = constants.ABS_PATH_TO_PROJECT_ROOT 

        self.timer = TimeManager(self._mode)

        self.time_units = constants.TIME_UNITS_BY_MODE[self._mode]
        self.logger = DataLogger(username=self._username, get_data_func=self.get_time_data, path_to_project_root=self._path_to_project_root)

    def shutdown(self):
        """Function responsible for safetly closing all threads / cleaning up anything needed at logout"""
        # Stop the timer first so the logger can be sure it is flushing the most recent data
        self.timer.logout()

        if self.logger.isAlive():
            self.logger.join()
            self.logger = None

    ##################
    # Task Selection #
    ##################
    def add_task(self, new_task):
        """:brief Adds a task to the data json in time management
        \n:param new_task - The name of the task being added"""
        return_code = self.timer.add_task(new_task)
        if return_code == 'Already Added':
            self.send_to_client('update_info', {'info': f'Task \'{new_task}\' already exists'})
            return 'Already Added'
        return 'ACK'

    def get_task_list(self):
        """:brief returns a list of the tasks currently stored by time_manager"""
        return self.timer.task_list

    def get_username(self) -> str:
        """:returns the username of this BackendController object"""
        return self._username

    #########################
    # End of Task Selection #
    #########################

    ##################
    # Timer Wrappers #
    ##################
    def load_in_data_at_startup(self):
        """Wrapper function to get the data stored in the file and save it in the timer object"""
        data_to_load = self.get_data_at_startup()
        self.timer.load_in_previous_data(data_to_load)

    def start_timer(self, task_name):
        """Interface function between app_manager and time_manager for starting the timer"""
        self.timer.start_timer(task_name)

    def stop_timer(self, task_name):
        """Interface function between app_manager and time_manager for stopping the timer"""
        self.timer.stop_timer(task_name)
        start_time = self.timer.get_latest_start_time(task_name)
        start_time = self.timer.get_latest_stop_time(task_name)
        time_diff = self.timer.get_latest_diff_time(task_name)

        info_dict = {'difference': time_diff, 'task': task_name, 'start_time': start_time, 'stop_time': start_time}
        self.send_to_client('stop_timer_diff', info_dict)

    def get_current_diff(self, task_name):
        """Interface function between app_manager and time_manager for updating a tasks current the timer"""
        return self.timer.get_current_diff(task_name)

    def get_total_time(self, task_name):
        """Interface function between app_manager and time_manager for getting a tasks total time"""
        total_time = self.timer.get_total_time(task_name)
        return total_time

    def get_completed_time_list(self, task_name):
        """Interface function between app_manager and time_manager 
        for getting all of the completed time segements of a given task"""
        task_list = self.timer.get_completed_time_list(task_name)
        return task_list

    ################
    # End of Timer #
    ################

    ###############
    # Data Logger #
    ###############
    def get_time_data(self) -> dict():
        """:brief Function to handle getting the stored data from time_manager and returning it to whatever is calling it
        \n:return The data stored in time_manager
        \n:Note Used by data logger to get the data to save
        """
        data = self.timer.get_all_data()
        return data

    def get_data_at_startup(self) -> dict():
        """:brief Gets the data stored in the file at startup
        :return The data stored in the file from another run of the program"""
        return self.logger.get_data_in_file()


    ######################
    # End of Data Logger #
    ######################


    ######################
    # Private Functions  #
    ######################
