"""File used to keep track of hardcoded constants / prevent magic numbers"""
# Converstion constants
SEC_PER_HOUR = 3600
SEC_PER_MIN  = 60
SIX_MINUTES_IN_HOURS = .1 # 6 min = .1 hr 


# Time management constants
TIME_PAIRINGS_INDICES = {
    'start_time' : 0,
    'stop_time'  : 1,
    "time_diff"  : 2,
}

TIME_UNITS_BY_MODE = {
    "law" : 'hours',
}