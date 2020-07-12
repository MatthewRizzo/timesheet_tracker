## Higher level priority functionalities to implement

1. Add Mode's that are selected in task menu
    1. For now just law mode
    2. Have the mode correspond to how diff math is done 
        * Round to 1 decimal and always round up
        * Make it so that it rounds up to nearest 1/10 of an hour (6 min)
        * Exception is if exactly a 1/10 has been worked
2. Make a threaded logging class
    1. Periodically writes the current time/data json to a file 
    2. Will require a thread lock/mutex on the data in the time_manager class

## Low Priority tasks once base functionality exists
1. Make login so that multiple people can use program without seeing each other's data
2. Add Scroll wheel to general info section. Enables not having to delete everytime another data point is added
    * Will have to encapsulate each message in a box / card
3. Setup a venv for this program. Ensures server running backend does not have to change its native packages
4. Change local host to a custom name like "Timekeeper"
5. Make pressing enter while in Enter New Task input also submit the task
6. Make the calculation mode and debug mode get controlled by flags (use argparse)
7. Find a way to turn of get_all_time in time-display.js when the stop watch is not running 
    * temporarily turn it back on if the dropdown menu every changes
