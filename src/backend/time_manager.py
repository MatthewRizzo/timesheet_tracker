from datetime import datetime, timedelta
import math

from backend import constants

class TimeManager():
    def __init__(self):
        self._task_json = dict()

        self._datetimeFormat = '%H:%M:%S'
        self._is_timer_active = False

        # TODO - change this to have many modes. Default to law because that is the initial purpose of this program
        self._time_mode = "law"

    #####################
    # Public Functions  #
    #####################
    def add_task(self, task_name):
        """:brief - Create the standard format for a task. Add it to the json as a value for the key (input name)
        \n:param task_name - The name of the task being added"""
        if task_name in self._task_json:
            return 'Already Added'
        self._task_json[task_name] = dict()
        self._task_json[task_name]['total_time'] = 0

        # Will store tuples of (start time, stop time, time difference)
        self._task_json[task_name]['time_pairings'] = []
        return 'ACK'

    def start_timer(self, task_name):
        """:brief Record the start time for a given task
        \n:param task_name - The task being timed"""
        cur_time = self._get_current_time()
        self._task_json[task_name]['time_pairings'].append([None, None, None])
        self.set_latest_start_time(task_name, cur_time)
        self._is_timer_active = True

    def stop_timer(self, task_name):
        """:brief Stops the timer. Records the stop time for a given task. 
            Calculates time spent in this timer, adds it to total time.
        \n:param task_name - The task being timed"""
        # The current tuple will always be the last one, and the end time is always the 2nd element
        # self.get_latest_times(task_name)[constants.TIME_PAIRINGS_INDICES['stop_time']] = self._get_current_time()
        self.set_latest_stop_time(task_name, self._get_current_time())
        
        time_diff = self._calculate_time_diff(task_name)

        # Update the time difference for this pairing + total time
        # self.get_latest_times(task_name)[constants.TIME_PAIRINGS_INDICES['time_diff']] = time_diff
        self.set_latest_diff_time(task_name, time_diff)
        self._task_json[task_name]['total_time'] += time_diff
        self._is_timer_active = False

    def display_time_diff(self, task_name):
        """Displays the time difference of the most recently completed start/stop set for the given task"""
        for pairing in reversed(self._task_json[task_name]['time_pairings']):
            time_diff = pairing[constants.TIME_PAIRINGS_INDICES['time_diff']]
            if time_diff is not None:
                return time_diff

    def update_cur_timer(self, task_name):
        """Utility function. While timer active, calculate current time it has been running for."""
        #TODO - This once the rest of the basic functionality works

    ######################
    # Private Functions  #
    ######################
    def _calculate_time_diff(self, task_name):
        """:brief - Calculates the time difference for the last set of times of a given task
        """
        
        start_time = self.get_latest_start_time(task_name)
        end_time   = self.get_latest_stop_time(task_name)

        start_time_striped = datetime.strptime(start_time, self._datetimeFormat)
        end_time_striped   = datetime.strptime(end_time, self._datetimeFormat)
        elapsed_time = end_time_striped - start_time_striped
        
        # Get hours passed. 
        seconds_passed = elapsed_time.total_seconds()
        if self._time_mode == 'law':
            
            hours_passed = self._get_law_diff(seconds_passed)
            
        else:
            hours_passed = round((seconds_passed / constants.SEC_PER_HOUR), 2)

        return hours_passed

    def _get_current_time(self):
        """Utility function to return the current time in H:M:S format"""
        cur_time = datetime.now()
        
        time_string = cur_time.strftime(self._datetimeFormat)
        return time_string

    def _get_law_diff(self, time_diff_sec):
        """Getting the time difference for law firms is different, this function handles that.
        \nIncludes tenths decimal. In increments of 1. i.e. .1, .2, .3"""
        # Get the whole number of hours passed 
        hours_passed_raw = float(time_diff_sec / constants.SEC_PER_HOUR)

        # The practice is to always round up to the nearest 6 minutes (10th of an hour). 
        hours_passed_str, remaining_min_str = str(hours_passed_raw).split('.')
        remaining_min_tenth_str = remaining_min_str[0]

        # If the decimal place after a tenth is greater than 0, it means the time is somewhere between 0 and 6 minutes. 
        # Common practice is to round that up to a full 6 minutes no matter what
        remaining_min_less_than_tenth = int(remaining_min_str[1:])
        if remaining_min_less_than_tenth > 0:
            remaining_min_tenth_str = str(int(remaining_min_tenth_str) + 1)
        
        total_hours_passed_str = hours_passed_str + '.' + remaining_min_tenth_str
        return float(total_hours_passed_str)

    #####################
    # Getters / Setters #
    #####################
    def get_latest_times(self, task_name):
        """:brief Gets the latest existing start, stop, and diff times for the given task"""
        return self._task_json[task_name]['time_pairings'][-1]

    def get_latest_start_time(self, task_name):
        return self.get_latest_times(task_name)[constants.TIME_PAIRINGS_INDICES['start_time']]
    def set_latest_start_time(self, task_name, start_time):
        self.get_latest_times(task_name)[constants.TIME_PAIRINGS_INDICES['start_time']] = start_time

    def get_latest_stop_time(self, task_name):
        return self.get_latest_times(task_name)[constants.TIME_PAIRINGS_INDICES['stop_time']]
    def set_latest_stop_time(self, task_name, stop_time):
        self.get_latest_times(task_name)[constants.TIME_PAIRINGS_INDICES['stop_time']] = stop_time

    def get_latest_diff_time(self, task_name):
        return self.get_latest_times(task_name)[constants.TIME_PAIRINGS_INDICES['time_diff']]
    def set_latest_diff_time(self, task_name, diff_time):
        self.get_latest_times(task_name)[constants.TIME_PAIRINGS_INDICES['time_diff']] = diff_time

    @property
    def task_list(self):
        if self._task_json == {}:
            return []
        else:
            return list(self._task_json.keys() )