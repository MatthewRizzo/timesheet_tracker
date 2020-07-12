# Activate the venv to activate it
start_loc=$PWD

# Go to project root
cd ../

# Setup Pathing variables
project_root_dir=$PWD

# Delete any currently existing venv's
echo Deleting any existing virtual environment
rm -rf $project_root_dir/virtual_environment_linux

# Create the venv
echo Creating the virtual environment
python3.7 -m venv virtual_environment_linux

# Setup Path's relative to project root
venv_dir_name='virtual_environment_linux'
venv_root_path=$project_root_dir/$venv_dir_name
venv_bin_path=$venv_root_path/bin

# This needs to be what the python executable in the venv is called
pip_script=pip3

echo Moving to bin at $venv_bin_path
cd $venv_bin_path

# Just in case, update pip
echo upgrading pip
$venv_bin_path/$pip_script install --upgrade pip

# Install the modules (with their correct versions) to the venv
echo Installing modules
$venv_bin_path/$pip_script install -r $start_loc/requirements.txt

# Go back to starting location after install complete
cd $start_loc
