# Purpose

This code will keep track of timespent on a task(s) through a UI with a start/stop botton.

## How to use it
* All you need is python!! 
* Package Versions??? Eventually a virtual environment will be added.
    * For now, just make sure you pip every module in installation/requirements.txt.
    * This is easily doable by running installation/install.bat (Windows) or installation/install.sh (Linux)
* Use the run.bat (windows) or run.sh (linux) file to start up the program. 
* Enjoy having a streamlined process to keep track of tasks for your timesheets!!!!

## Front-end

Consists of the "Task Selection", "Timer", and "Time Display" sections.

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