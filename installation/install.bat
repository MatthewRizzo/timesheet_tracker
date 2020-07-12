set start_loc=%CD%
cd ../
set project_root_dir=%CD%
set venv_python_path=%project_root_dir%\virtual_environment\Scripts\
set python_program=python.exe
cd %venv_python_path%

:: Just in case, update pip
%python_program% -m pip install --upgrade pip

:: Unistall the current versions to the venv
%python_program% -m pip uninstall -r %start_loc%/requirements.txt -y

:: Install the correct versions to the venv
%python_program% -m pip install -r %start_loc%/requirements.txt

cd %start_loc%