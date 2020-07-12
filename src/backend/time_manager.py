from datetime import datetime, timedelta
import math

from backend import constants

class TimeManager():
    def __init__(self, mode):
        self._task_json = dict()

        self._datetimeFormat = '%H:%M:%S'
        self._is_timer_active = False

        # TODO - change this to have many modes. Default to law because that is the initial purpose of this program
        self._time_mode = mode

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
        time_diff = self._calculate_time_diff_at_end(task_name)

        # Update the time difference for this pairing + total time
        self.set_latest_diff_time(task_name, time_diff)
        new_total_diff_time = self._task_json[task_name]['total_time'] + time_diff

        # Adjust for potential issues
        if self._time_mode == "law":
            new_total_diff_time = self.total_time_diff_calc_law(new_total_diff_time)
        
        # Set the total time after any adjustements are made
        self._task_json[task_name]['total_time'] = new_total_diff_time

        self._is_timer_active = False

    def display_time_diff(self, task_name):
        """Displays the time difference of the most recently completed start/stop set for the given task"""
        for pairing in reversed(self.get_time_pairings(task_name)):
            time_diff = pairing[constants.TIME_PAIRINGS_INDICES['time_diff']]
            if time_diff is not None:
                return time_diff

    def get_current_diff(self, task_name) -> float:
        """Utility function. While timer active, calculate current time it has been running for.
        \n:return The time Difference (in hours)"""
        cur_time = self._get_current_time()
        start_time = self.get_latest_start_time(task_name)
        
        cur_diff_time = self._calculate_time_diff(start_time, cur_time)
        return cur_diff_time

    def get_completed_time_list(self, task_name):
        """:brief Gets the list of completed time segments for the current task
        \n:note If there are no completed tasks, it will return an empty list
        """
        # This is for the moment between the task's creation, and the backend not having created it's key yet
        if task_name not in self._task_json:
            return []

        full_time_list = self.get_time_pairings(task_name)
        stop_time_index = constants.TIME_PAIRINGS_INDICES['stop_time']

        if len(full_time_list) == 0:
            return []
        # Check if the last time set is incomplete, if so exclude it 
        elif full_time_list[-1][stop_time_index] is None:
            return full_time_list[:-1]
        else:
            return full_time_list


    ######################
    # Private Functions  #
    ######################
    def _calculate_time_diff(self, start_time: datetime, end_time: datetime) -> float:
        """Given a start and end time, returns the time difference (in hours)"""
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

    def _calculate_time_diff_at_end(self, task_name):
        """:brief - Calculates the time difference for the last set of times of a given task"""
        
        start_time = self.get_latest_start_time(task_name)
        end_time   = self.get_latest_stop_time(task_name)
        return self._calculate_time_diff(start_time, end_time)
        

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
        hours_passed_str, hour_dec_str = str(hours_passed_raw).split('.')
        hours_remaining_float = float("." + hour_dec_str) # recreate it in the form .xxxxxxxx
        tenths_digit = hour_dec_str[0] # This is the 1/10'ths place

        # If the decimal place after a tenth is greater than 0, it means the time is somewhere between 0 and 6 minutes. 
        # Common practice is to round that up to a full 6 minutes no matter what
        if self._fraction_mod(hours_remaining_float, constants.SIX_MINUTES_IN_HOURS) > 0:
            # proof: .52 mod .1 = .02 > 0
            tenths_digit = str(int(tenths_digit) + 1)[0]
        total_hours_passed_str = hours_passed_str + '.' + tenths_digit
        return float(total_hours_passed_str)

    def _fraction_mod(self, value, modulus):
        """:brief in order to mod with fractions, the following algorithm must be used -> a (mod b) = a - b*floor(a/b)
        \n:Note:
            \n - Doing a%b when a and b are both < 1 leads to rounding and floating point errors. The result is incorrect. This method has valid answers.
            \n- The proof for this came from https://math.stackexchange.com/questions/864568/is-it-possible-to-do-modulo-of-a-fraction 
        \n:return The result of the mod
        """
        value = float(value)
        modulus = float(modulus)
        division = math.floor(value/modulus)
        return value - (division * modulus)

    def total_time_diff_calc_law(self, new_total_time_diff):
        """:brief Calculating the total difference time for law is harder due to it being prone to floating point errors.
        This function works to account for, and fix that problem
        """
        # Make sure there is only 1 decimal place - in testing floating point errors made total go beyond that
        hours, decimal = str(new_total_time_diff).split(".", maxsplit=1)

        # Floating point error also sometimes leaves digits after .1. Check for that and add round accordingly
        shifted_dec = float(decimal[0] + "." + decimal[1:])
        fixed_dec_str = str(round(shifted_dec, 0))

        recreataed_diff_str = hours + "." + fixed_dec_str[0]
        return float(recreataed_diff_str)
    #####################
    # Getters / Setters #
    #####################
    def get_time_pairings(self, task_name):
        return self._task_json[task_name]['time_pairings']

    def get_latest_times(self, task_name):
        """:brief Gets the latest existing start, stop, and diff times for the given task"""
        return self.get_time_pairings(task_name)[-1]

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

    def get_total_time(self, task_name):
        if task_name not in self._task_json:
            return "No time yet"
        else:
            return self._task_json[task_name]['total_time']

    @property
    def task_list(self):
        if self._task_json == {}:
            return []
        else:
            return list(self._task_json.keys() )