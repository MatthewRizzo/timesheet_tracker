#!/bin/bash
# This script starts up the application in a service. It will live  even after ssh logout.

alias start_timesheet_app="sudo systemctl start timesheet-tracker-app.service"
$start_timesheet_app