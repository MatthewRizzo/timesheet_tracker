@echo off
:: Save the start location for when the script ends
set start_loc=%CD% 

:: Go to installation folder - folder containing this script. 
set script_loc=%~dp0

:: Ensures path's will always be relative to install folder and project root
cd %script_loc%
cd ..

@echo off
set project_root_dir=%CD%

:: Delete any currently existing venv's
rmdir /S /Q %project_root_dir%\virtual_environment_windows
@echo on

:: Create the venv
python -m venv virtual_environment_windows

@echo off
:: Setup the variables relative to the venv
set venv_dir_name=virtual_environment_windows
set venv_root_path=%project_root_dir%\%venv_dir_name%
set venv_scripts_path=%venv_root_path%\Scripts\

:: This needs to be what the python executable in the venv is called
set python_program=python.exe
@echo on

cd %venv_scripts_path%

:: Just in case, update pip
echo Updating Pip
%python_program% -m pip install --upgrade pip

:: Install the modules (with their correct versions) to the venv
echo Installing python modules
%python_program% -m pip install -r %script_loc%\requirements.txt

:: Go back to starting location after install complete
cd %start_loc%