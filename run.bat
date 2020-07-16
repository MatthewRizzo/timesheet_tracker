@echo off
:: Get path to venv python
SET path_to_windows_venv=%CD%\virtual_environment_windows\Scripts
SET python_program=python.exe
SET full_python_path=%path_to_windows_venv%\%python_program%

:: Check that the the venv is installed
if EXIST %full_python_path% ( 
    %path_to_windows_venv%\%python_program% src\__main__.py
) ELSE (
    echo The Windows Virtual Environment is not setup.
    echo Please run install\install.bat and then rerun this script 
)