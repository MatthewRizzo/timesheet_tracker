# Which File to Run

## Run Locally (i.e. not setup a system service)
* Just run install.sh
* In linux with `./install.sh`
* In Windows, `bash ./install.sh`
    * Prereq of needing git-bash
* install.sh runs os specific commands after determining what OS it is being run on
* Calls helper scripts in other folders

## Run on a Server - Currently only supports a linux server
This will allow for external users to access the exposed port and run off a central server location
* `sudo ./setup_service.sh`
* It perfoms extra steps, and ends up calling install.sh
* sudo is needed for permissioning to access the /etc/ folder
