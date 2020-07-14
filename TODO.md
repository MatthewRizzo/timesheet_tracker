## Higher level priority functionalities to implement

1. Add Mode's that are selected in task menu
    1. For now just law mode
    2. Have the mode correspond to how diff math is done 
        * Round to 1 decimal and always round up
        * Make it so that it rounds up to nearest 1/10 of an hour (6 min)
        * Exception is if exactly a 1/10 has been worked
2. Add ability to distinguish between users 
    * I.e. their times would be different
3. Add 'notes' section to time segements. 
    * User could input a note before or during a time session
    * That note would be stored with start time, stop time, diff time
    * That note would be displayed in general information 
    * That note would be dispalyed in the line item summary of time display
4. Make a calendar view mode
5. Have a clean/dirty flag to prevent unnecessary writes to json if nothing has changed for a given user's data
6. Save Users + credentials to a database (that is gitignored)
    * Pull from this file on startup (prevent having to reregister)
    * Makes looking through users not O(n) because lookup times are faster 


## Low Priority tasks once base functionality exists
1. Make login so that multiple people can use program without seeing each other's data
2. Change local host to a custom name like "Timekeeper"
3. Make pressing enter while in Enter New Task input also submit the task
4. Make the debug mode get controlled by flags (use argparse)
5. Make the calculation mode get controlled by dropdown
    * Which mode a user defaults do should get stored in their task json and get loaded in on start
6. Find a way to turn of get_all_time in time-display.js when the stop watch is not running 
    * temporarily turn it back on if the dropdown menu every changes
7. make automatically openning the webpage happen via flag
    * Once deployed, every service start a new tab will be opened