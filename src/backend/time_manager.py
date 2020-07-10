from datetime import datetime, timedelta
import math

class TimeManager():
    def __init__(self):
        self._task_json = dict()

        self._datetimeFormat = '%H:%M:%S'
        self._is_timer_active = False
        self._sec_per_hour = 3600
        self._sec_per_min  = 60

    #####################
    # Public Functions  #
    #####################
    def add_task(self, task_name):
        """:brief - Create the standard format for a task. Add it to the json as a value for the key (input name)
        \n:param task_name - The name of the task being added"""
        if task_name in self._task_json:
            return
        self._task_json[task_name] = dict()
        self._task_json[task_name]['total_time'] = 0

        # Will store tuples of (start time, stop time)
        self._task_json[task_name]['time_pairings'] = []

    def start_timer(self, task_name):
        """:brief Record the start time for a given task
        \n:param task_name - The task being timed"""
        cur_time = self._get_current_time()
        self._task_json[task_name]['time_pairings'].append((cur_time, None))
        self._is_timer_active = True

    def stop_timer(self, task_name):
        """:brief Stops the timer. Records the stop time for a given task. 
            Calculates time spent in this timer, adds it to total time.
        \n:param task_name - The task being timed"""
        # The current tuple will always be the last one, and the end time is always the 2nd element
        self._task_json[task_name]['time_pairings'][-1][1] = self._get_current_time()
        
        time_diff = self._calculate_time_diff(task_name)

        self._task_json[task_name]['total_time'] = time_diff
        self._is_timer_active = False

    def update_cur_timer(self, task_name):
        """Utility function. While timer active, calculate current time it has been running for."""
        #TODO - This once the rest of the basic functionality works

    ######################
    # Private Functions  #
    ######################
    def _calculate_time_diff(self, task_name):
        """:brief - Calculates the time difference for the last set of times of a given task
        """
        tuple_to_calc = self._task_json[task_name]['time_pairings'][-1]
        start_time = tuple_to_calc[0]
        end_time   = tuple_to_calc[1]
        
        start_time_striped = datetime.datetime.strptime(start_time, self._datetimeFormat)
        end_time_striped   = datetime.datetime.strptime(end_time, self._datetimeFormat)
        elapsed_time = end_time_striped - start_time_striped
        
        # Get hours passed, includes remaining minutes up to 2 digits
        seconds_passed = elapsed_time.total_seconds()
        hours_passed = round((seconds_passed / self._sec_per_hour), 2)

    def _get_current_time(self):
        """Utility function to return the current time in H:M:S format"""
        cur_time = datetime.now()
        
        time_string = cur_time.strftime(self._datetimeFormat)
        return time_string
