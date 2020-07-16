#!/bin/bash
# This script re-starts up the application in a service. It will live  even after ssh logout.

alias restart_timesheet_app="sudo systemctl restart timesheet-tracker-app.service"
$restart_timesheet_app