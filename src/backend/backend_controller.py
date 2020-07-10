from backend.time_manager import TimeManager

class BackendController():
    def __init__(self):
        self.timer = TimeManager()

        # TODO - add a class to manage writing json to file / storing it elsewhere

    ####################
    # Timer Functions  #
    ####################
    def start_timer(self, task_name):
        """Interface function between app_manager and time_manager for starting the timer"""
        self.timer.start_timer(task_name)

    def stop_timer(self, task_name):
        """Interface function between app_manager and time_manager for stopping the timer"""
        self.timer.stop_timer(task_name)

    def update_cur_timer(self, task_name):
        """Interface function between app_manager and time_manager for updating a tasks current the timer"""
        # TODO - Currently timer's function for update_cur_timer is empty
        self.timer.update_cur_timer(task_name)
    ###########################
    # End of Timer Functions  #
    ###########################

    