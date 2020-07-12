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
3. Add ability to distinguish between users 
    * I.e. their times would be different
4. Add 'notes' section to time segements. 
    * User could input a note before or during a time session
    * That note would be stored with start time, stop time, diff time
    * That note would be displayed in general information 
    * That note would be dispalyed in the line item summary of time display
5. Make a calendar view mode


## Low Priority tasks once base functionality exists
1. Make login so that multiple people can use program without seeing each other's data
2. Add Scroll wheel to general info section. Enables not having to delete everytime another data point is added
    * Will have to encapsulate each message in a box / card
3. Change local host to a custom name like "Timekeeper"
4. Make pressing enter while in Enter New Task input also submit the task
5. Make the calculation mode and debug mode get controlled by flags (use argparse)
6. Find a way to turn of get_all_time in time-display.js when the stop watch is not running 
    * temporarily turn it back on if the dropdown menu every changes
