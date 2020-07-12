# Store the start loc to go back to it when done
start_loc=$PWD

# Go to project root - navigate to the installation folder and backup one to get to project root
script_dir_path=$(cd `dirname $0` && pwd)
cd $script_dir_path
cd ../
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
echo Upgrading pip
$venv_bin_path/$pip_script install --upgrade pip

# Install the modules (with their correct versions) to the venv
echo Installing modules
$venv_bin_path/$pip_script install -r $project_root_dir/installation/requirements.txt

# Go back to starting location after install complete
cd $start_loc
