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
        return_code = self.timer.add_task(new_task)
        if return_code == 'Already Added':
            self.send_to_client('update_info', {'info': f'Task \'{new_task}\' already exists'})
            return 'Already Added'
        return 'ACK'

    def get_task_list(self):
        """:brief returns a list of the tasks currently stored by time_manager"""
        return self.timer.task_list

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
        start_time = self.timer.get_latest_start_time(task_name)
        start_time = self.timer.get_latest_stop_time(task_name)
        time_diff = self.timer.get_latest_diff_time(task_name)

        info_dict = {'difference': time_diff, 'task': task_name, 'start_time': start_time, 'stop_time': start_time}
        self.send_to_client('stop_timer_diff', info_dict)

    def update_cur_timer(self, task_name):
        """Interface function between app_manager and time_manager for updating a tasks current the timer"""
        # TODO - Currently timer's function for update_cur_timer is empty
        self.timer.update_cur_timer(task_name)
    ################
    # End of Timer #
    ################

    