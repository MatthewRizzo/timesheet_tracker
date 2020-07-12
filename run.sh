path_to_venv_python_dir=$PWD/virtual_environment_linux/bin
python_executable=python3.7
start_app_cmd=$PWD/src/__main__.py

if test -d "$path_to_venv_python_dir"; then 
    full_python_path=$path_to_venv_python_dir/$python_executable
    
    # Start the program
    $full_python_path $start_app_cmd
else 
    echo 'The Linux Virtual Environment is not setup.'
    echo 'Please run installation/install.sh and then rerun this script'
fi


