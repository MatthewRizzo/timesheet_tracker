#!/bin/bash

[[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]] && is_windows=true || is_windows=false

# if linux, need to check if using correct permissions
if [[ "${is_windows}" = false ]]; then
    if [ "$EUID" -ne 0 ]; then
        echo "Please run as root ('sudo')"
        exit
    fi
fi

# Go to the root of the install dir, regardless of where this script was run from
install_dir_path="$(readlink -fm $0/..)"
project_root_dir="$(readlink -fm ${install_dir_path}/..)"

# Go back to install folder
cd $install_dir_path

# Call the install file to make sure all environment factors are setup
sudo $install_dir_path/install.sh

# Create variable for path to environment file
# Info grabbed from https://serverfault.com/a/413408 to make a safe server service
environment_dir=/etc/sysconfig
environment_file=${environment_dir}/web_app_environ
echo "Environment file = ${environment_file}"

# If environ folder & file do not exist, add them. Prevents issues when saving to the file
test -d ${environment_dir} && echo "${environment_dir} Already Exists" || mkdir ${environment_dir}
test -f ${environment_file} && echo "${environment_file} Already Exists" || touch ${environment_file}

# Export any variables needed to the service file 
# create backup & save new version with updated path
sed -i.bak '/project_root_dir=/d' ${environment_file}
echo "project_root_dir=${project_root_dir}" >> ${environment_file}
source ${environment_file}
echo "project_root_dir: ${project_root_dir}"


echo "Deploying the Service File to the Server"
sys_service_dir=/etc/systemd/system
service_file_dir=${project_root_dir}/install${sys_service_dir}
service_file=$(find ${service_file_dir} -maxdepth 1 -name "*-app*" -print)
servic_file_name=$(basename "${service_file}")
cp ${service_file} ${sys_service_dir}/
echo "-- Deployed ${service_file} -> ${sys_service_dir}/${servic_file_name}"


# Start service after everything installed if linux
if [[ "${is_windows}" = false ]]; then
    echo "Starting Service"
    echo "-- Stopping ${servic_file_name} Daemon"
    systemctl stop ${servic_file_name} # stop daemon
    echo "-- Stopped ${servic_file_name} Daemon"
    systemctl daemon-reload # refresh service daemons
    echo "-- Reloaded ${servic_file_name} Daemon"
    systemctl start ${servic_file_name} # start daemon
    echo "-- Started ${servic_file_name} Daemon"
fi