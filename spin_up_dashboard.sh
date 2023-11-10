#!/bin/bash

#get all variables not declared within file
#check dependencies
source ./env.sh


    pid_to_kill=$(lsof -t -i :$dashboard_port -s TCP:LISTEN)

    echo "pid_to_kill=$pid_to_kill"

    #Check if the variable is defined and if it has values
    #and if it has values in it.
    if [[ ${pid_to_kill} && ${pid_to_kill-_} ]]; then
    for ptk in "${pid_to_kill[@]}" ; do
        sudo kill -9 ${ptk}
    done
    fi


echo "************************"
echo "Setting Up Symlinks"
echo "************************"


#putting symlinks into dashboard directories
source_dir=$(pwd)/libraries/
target_dir=${dashboard_path}/libraries/db_libraries
rm -rf $target_dir

target_dir=${dashboard_path}/libraries
# Loop through each file in the source directory
for file in "$source_dir"/*; do
    # Extract just the filename
    filename=$(basename "$file")

    # Create a symlink in the target directory
    ln -s "$file" "$target_dir/$filename"
done

#putting symlinks into dashboard directories
source_dir=$(pwd)/j_nbks/
target_dir=${dashboard_path}/j_nbks
rm -rf $target_dir


if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi

#putting symlinks into dashboard directories
source_dir=$(pwd)/db_artifacts/
target_dir=${dashboard_path}/db_artifacts
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi

#putting symlinks into dashboard directories
source_dir=${dashboard_path}/
target_dir=${dashboard_path}/j_nbks/dashboard
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi


#putting symlinks into dashboard directories
source_dir=$(pwd)/db_artifacts/
target_dir=${dashboard_path}/db_artifacts
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi



#todo: setup run command with appropriate port

export dashboard_port=$dashboard_port
export dashboard_host=$dashboard_host
export dashboard_url=$dashboard_url
export response_code="\$response_code"
export interval="\$interval"
export finished="\$finished"
export dashboard_jn_port=$dashboard_jn_port
export dashboard_jn_url=$dashboard_jn_url



#Flask URL
config_file="${dashboard_path}/run_dashboard.template"

of=${dashboard_path}/run_dashboard.sh


envsubst < $config_file > $of

echo cf=$of
chmod 777 $of

#JN URL
config_file="${dashboard_path}/run_jn.template"

of=${dashboard_path}/run_jn.sh

envsubst < $config_file > $of

echo cf=$of
chmod 777 $of


this_dir=$(pwd)
cd ./dashboard
. ./run_dashboard.sh 
. ./run_jn.sh
cd $this_dir

