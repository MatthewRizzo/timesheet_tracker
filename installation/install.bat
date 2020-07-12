set start_loc=%CD%
cd ../
set venv_dir_name=virtual_environment
set project_root_dir=%CD%
set venv_root_path=%project_root_dir%\%venv_dir_name%
set venv_scripts_path=%venv_root_path%\Scripts\
set python_program=python.exe

:: Create the venv
python -m venv %venv_root_path%

cd %venv_scripts_path%

:: Just in case, update pip
%python_program% -m pip install --upgrade pip

:: Install the modules (with their correct versions) to the venv
%python_program% -m pip install -r %start_loc%/requirements.txt

cd %start_loc%