#!/bin/bash
[[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]] && is_windows=true || is_windows=false

# if linux, need to check if using correct permissions
if [[ "${is_windows}" = false ]]; then
    if [ "$EUID" -ne 0 ]; then
        echo "Please run as root ('sudo')"
        exit
    fi
fi

# Store the start loc to go back to it when done
install_dir_path="$(readlink -fm $0/..)"
project_root_dir="$(readlink -fm ${install_dir_path}/..)"

# Go to project root - navigate to the install folder and backup one to get to project root
cd $project_root_dir

# Download python3.7
python_version=3.7
python_name=python${python_version}

add-apt-repository -y ppa:deadsnakes/ppa
apt update -y
apt upgrade -y
apt install -y \
    ${python_name} \
    ${python_name}-venv

# Delete any currently existing venv's
echo Deleting any existing virtual environment
rm -rf $project_root_dir/virtual_environment_linux

# Create the venv
echo Creating the virtual environment
$python_name -m venv virtual_environment_linux

# Setup Path's relative to project root
venv_dir_name='virtual_environment_linux'
venv_root_path=$project_root_dir/$venv_dir_name
venv_bin_path=$venv_root_path/bin

# This needs to be what the python executable in the venv is called
pip_script=pip3

echo Moving to bin at $venv_bin_path
cd $venv_bin_path

# Just in case, update pip
echo Upgrading pip
$venv_bin_path/$pip_script install --upgrade pip

# Install the modules (with their correct versions) to the venv
echo Installing modules
$venv_bin_path/$pip_script install -r $project_root_dir/install/requirements.txt

# Go back to starting location after install complete
cd $start_loc
