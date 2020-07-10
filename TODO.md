## Higher level functionalities to implement

1. Add Mode's that are selected in task menu
    1. For now just law mode
    2. Have the mode correspond to how diff math is done 
        * Round to 1 decimal and always round up
        * Make it so that it rounds up to nearest 1/10 of an hour (6 min)
        * Exception is if exactly a 1/10 has been worked
2. Make a threaded logging class
    1. Periodically writes the current time/data json to a file 
    2. Will require a thread lock/mutex on the data in the time_manager class
3. Adding a task should also add another level to the time_manager json
    1. I.e. create a clean dict template but apply it behind the 'key' that is the new task