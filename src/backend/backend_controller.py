from backend.time_manager import TimeManager

class BackendController():
    def __init__(self, send_to_client):
        self.send_to_client = send_to_client
        self.timer = TimeManager()

        # TODO - add a class to manage writing json to file / storing it elsewhere

    ##################
    # Task Selection #
    ##################
    def add_task(self, new_task):
        """:brief Adds a task to the data json in time management
        \n:param new_task - The name of the task being added"""
        self.timer.add_task(new_task)

    #########################
    # End of Task Selection #
    #########################

    ##################
    # Timer Wrappers #
    ##################
    def start_timer(self, task_name):
        """Interface function between app_manager and time_manager for starting the timer"""
        self.timer.start_timer(task_name)

    def stop_timer(self, task_name):
        """Interface function between app_manager and time_manager for stopping the timer"""
        self.timer.stop_timer(task_name)
        self.timer.display_time_diff(task_name)

    def update_cur_timer(self, task_name):
        """Interface function between app_manager and time_manager for updating a tasks current the timer"""
        # TODO - Currently timer's function for update_cur_timer is empty
        self.timer.update_cur_timer(task_name)
    ################
    # End of Timer #
    ################

    