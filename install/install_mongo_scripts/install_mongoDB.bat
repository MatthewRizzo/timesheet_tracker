@echo off
:: WARNING: This file should NEVER be called by anything but install_mongoDB.sh
:: @file: Needed to execute windows command mid bash by install-mongoDB.sh downloading for windows
:: Based on https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows-unattended/
:: accepts arguments:
:: arg 1 = path to mongoDB Installer
:: arg 2 = path of install dir -- extern/mongoDB
:: arg 3 = path to mongo client
:: arg 4 = path to mongo daemon executable

set mongo_installer=%1
set mongo_installer_dir=%2
set mongo_client_path=%3
set mongo_daemon_path=%4

:: Print important information of where user's mongoDB was installed
echo Path to mongoDB Installer: %mongo_installer%
echo Path to mongoDB Installation Folder: %mongo_installer_dir%

:: Run the Install for mongoDB

:: Line's Purpose
:: Path output log file
:: Path of mongoDB .msi install file that was fetched
:: Default downloads to "C:\Program Files\MongoDB"
:: ADDLOCAL : Download mongoDB Server, Client, and GUI
msiexec.exe ^
            /l*v %mongo_installer_dir%\mdbinstall.log ^
            /qb /i %mongo_installer% ^
            ADDLOCAL="ServerService,Client" ^
            SHOULD_INSTALL_COMPASS="1"

:: Inform user of their downloads' binary paths
echo mongoDB Client Path: %mongo_client_path% -- use this to access via command line
echo mongoDB Server/Daemon Path: %mongo_daemon_path%