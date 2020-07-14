"""File used to keep track of hardcoded constants / prevent magic numbers"""
# -- External Packages -- #
import pathlib

# -- Project Defined Imports -- #
from backend import utils

# Converstion constants
SEC_PER_HOUR = 3600
SEC_PER_MIN  = 60
SIX_MINUTES_IN_HOURS = .1 # 6 min = .1 hr 

# Thread Periods (in seconds)
LOGGER_THREAD_PERIOD =5


# Time management constants
TIME_PAIRINGS_INDICES = {
    'start_time' : 0,
    'stop_time'  : 1,
    "time_diff"  : 2,
}

TIME_UNITS_BY_MODE = {
    "law" : 'hours',
}

# Path constants - their full paths
ABS_PATH_TO_PROJECT_ROOT = utils.get_project_root_path()
PATH_TO_RESULT_DATA_DIR =  pathlib.Path(ABS_PATH_TO_PROJECT_ROOT.joinpath('stored_results'))
PATH_TO_SRC_DIR =  pathlib.Path(ABS_PATH_TO_PROJECT_ROOT.joinpath('src'))
PATH_TO_BACKEDND_DIR = pathlib.Path(PATH_TO_SRC_DIR.joinpath('backend'))
PATH_TO_STATIC_DIR =  pathlib.Path(PATH_TO_SRC_DIR.joinpath('frontend'))
PATH_TO_TEMPLATES_DIR =  pathlib.Path(PATH_TO_SRC_DIR.joinpath('templates'))
PATH_TO_USER_DATA =  pathlib.Path(PATH_TO_BACKEDND_DIR.joinpath('user_data_dir'))
PATH_TO_COOKIES_DATA = pathlib.Path(PATH_TO_USER_DATA.joinpath("user_cookies.json"))

# Path constants - the ones relative to project root. Used to construct other paths with other variables
DATA_JSON_NAME = "times.json"



# Flask Site Pathing for sites that need to be references in multiple places
SITE_PATHS = {
    "homepage":    "/",
    "login":       "/login",
}