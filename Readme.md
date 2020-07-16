# Purpose

This code will keep track of timespent on a task(s) through a UI with a start/stop botton.

## How to Setup / Run the Timesheet Tracker
* All you need is python3.7 or greater!! 
* After cloning the Repository **(This only needs to be done once)**:
    1. Navigate to the install folder
    2. run install.bat (windows) or ./install.sh (linux)
        * These will create a virtual environment within the project for you
        * This is the only setup you need to do
* How to run:
    * Execute run.bat (windows) or ./run.sh (linux)
    * They will use the virtual environments created by the install scripts
* How to update:
    * Make sure you are on the Master branch of the repository
    * Pull for any changes
    * Rerun the install scripts
    * Done!!!

## Front-end

Consists of the "Task Selection", "Timer", and "Time Display" sections.

### How to Deploy to Linux Server
1. It is faily simple. run `install/setup_service.sh`
2. Use the scripts in `server_utility_scripts` to start, stop, and restart the service
3. Expose the port on your server used by the program (TODO to not have that port be hardcoded, and taken in as a flag)

### Task Selection

Will have 2 elements. 

1. Add Task
    1. There will be a text input box to input a new task. 
    2. This task will be added to the dropdown menu.
2. Select Task Dropdown
    1. Will include all previously added tasks.
    2. The timer, when run, will accure the elapsed time to the currently selected task

### Timer

It will consist of a start/stop button that toggles on click.

* When "Start" is clicked, a timestamp is recorded for the current time and associated with the currently selected task
* When "Stop" is clicked, a timestamp is recorded.
    * The difference between this timestamp and the one recorded at start will be calculated
    * This difference / timespan will be logged to the selected task for the day


### Time Display

* Will display all added tasks via another dropdown. 
* When a given task is selected, the total time spent on the task (for that day) will be displayed to the page.
* The timeframes worked on that task will also be shows 
    * i.e. Task A) 11-12, 2-4:30. Total time = 3.5 hrs.
* Time spent on a task will be calculated in hours and fractions of an hour (out to 2 decimal places).
    * Thus, every .6 minutes is another .01 hour.
    * Every 15 minutes is .25
    * etc...