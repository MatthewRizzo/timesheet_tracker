#!/bin/bash
# @File: Downloads MongoDB
# Note: Important Files are mongod.exe (it is the daemon for the server) & mongo.exe (client for mango)
# Windows: It defaults to downloading to: C:\Program Files\MongoDB\Server\4.2\bin
# Linux: Unknown

[[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]] && isWindows=true || isWindows=false
# CLI Flags
print_flags () {
    echo "=========================================================================================================="
    echo "Usage: install_mongoDB.sh"
    echo "=========================================================================================================="
    echo "Helper utility to download the correct version of mongoDB"
    echo "=========================================================================================================="
    echo "How to use:" 
    echo "  To Start: ./install_mongoDB.sh [flags]"
    echo "=========================================================================================================="
    echo "Needed Flags:"
    echo "  --project-root-dir <dir> : Absolute path to the root of the repo"
    echo "  --install-dir <dir> Absolute path to the install directory of the repo (this folder)"
    echo "  --user-data-dir <dir> Absolute path to the user data directory of the repo"
    echo "  --download-mongo <bool>: If set, will download mongo. Don't set the flag if mongo is already installed."
    echo "=========================================================================================================="
}

# Check the command line args for relevant variables
root_dir=""
install_dir=""
user_data_dir=""
download_mongo=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --project-root-dir )
            root_dir="$2"
            shift
            ;;
        --install-dir )
            install_dir="$2"
            shift
            ;;
        --user-data-dir )
            user_data_dir="$2"
            shift
            ;;
        --download-mongo )
            download_mongo=true
            ;;
        -h | --help )
            print_flags
            exit 0
            ;;
        * )
            echo "... Unrecognized Command: $1"
            print_flags
            exit 1
    esac
    shift
done


# $1 is the path being converted
# returns a  windows path -- capture with res=$(linux_to_win_path <path>)
# WARNING: Path cannot have spaces in it
function linux_to_win_path() {
    # get arg
    local path_linux=$1

    # remove first '/' (/d/...)
    local path_drive=${path_linux:1}
    # capitalize drive letter -- https://stackoverflow.com/a/12487455
    local path_drive="${path_drive^}"
    # insert ':' between first & second char
    local path_drive_colon=${path_drive:0:1}:${path_drive:1}
    # replace all '/' with '\' -- https://stackoverflow.com/a/13210909 - ${parameter//pattern/string}
    local windows_path=${path_drive_colon////\\}

    # return
    echo "${windows_path}"
}

# $1 is path to convert
# returns windows path with double backslash ('\\') -- capture with res=$(escape_backslash <path>)
function escape_backslash() {
    local original_path=$1
    # find and replace each '\' with '\\'
    double_backslash=${original_path//\\/\\\\}

    # return
    echo "${double_backslash}"
}

# Variables used by linux and/or windows
server_scripts_dir=${root_dir}/server_utility_scripts

mongo_dir=${root_dir}/mongoDB
database_log_path=${mongo_dir}/log/mongodb.log
start_mongo_script=${server_scripts_dir}/start_mongoDB.sh
stop_mongo_script=${server_scripts_dir}/stop_mongoDB.sh

mongo_default_install_dir="/c/Program Files/MongoDB/Server/4.2"
mongo_client_path="${mongo_default_install_dir}/bin/mongo.exe"
mongo_daemon_path="${mongo_default_install_dir}/bin/mongod.exe"


# Actually run the install
if [[ ${isWindows} == true ]]; then
    # Might need Admin Privelages for windows

    # These are some of the basic paths
    download_name="mongodb-win32-x86_64-enterprise-windows-64-4.2.8-signed.msi"
    win_download_URL=https://downloads.mongodb.com/win32/${download_name}
    download_path=${mongo_dir}/${download_name} # needed for curl command
    install_batch_script=${install_dir}/install_mongo_scripts/install_mongoDB.bat

    # Only download the .msi if the flag is set properly
    if [[ ${download_mongo} == true ]]; then
        # Get the .msi install file from the internet using curl
        curl --url ${win_download_URL} --output ${download_path}
    fi

    # Call the batch script indirectly due to differences between bash and batch
    # Eencapsualte command in quotes, but rightmost quote cannot be escaped and is added to the path
    # See the script for all its arguments
    ${install_batch_script} \
        $(linux_to_win_path ${download_path}) \
        $(linux_to_win_path ${mongo_dir}) \
        "${mongo_client_path}" \
        "${mongo_daemon_path}"

    # Create & Register the Database Dir (default path)
    db_data_dir=$(linux_to_win_path ${user_data_dir})
    database_log_path_win=$(linux_to_win_path ${database_log_path})
    echo "Database Data Directory: ${db_data_dir}"
    echo "Database Log File: ${database_log_path_win}"

else
    # Handles Linux
    # Import the MongoDB public GPG key −
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

    # Create a /etc/apt/sources.list.d/mongodb.list file
    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
    # Update and install will occur later on
fi

# Start mongoDB to Create the Database
bash ${start_mongo_script}

# Inform user how to stop mongoDB Daemon
echo -e "Stop mongoDB Server/Daemon with '${stop_mongo_script}'\n"