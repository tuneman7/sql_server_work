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


#putting symlinks into api directories
source_dir=$(pwd)/libraries
target_dir=${dashboard_path}/libraries/db_libraries

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




config_file="${dashboard_path}/run_dashboard.template"

of=${dashboard_path}/run_dashboard.sh


envsubst < $config_file > $of

echo cf=$of
chmod 777 $of

this_dir=$(pwd)
cd ./dashboard
return
. ./run_dashboard.sh &
cd $this_dir

