#!/bin/bash

#get all variables not declared within file
#check dependencies
source ./env.sh



for m_port in "${server_ports_used[@]}"
do

    pid_to_kill=$(lsof -t -i :$m_port -s TCP:LISTEN)

    echo "pid_to_kill=$pid_to_kill"

    #Check if the variable is defined and if it has values
    #and if it has values in it.
    if [[ ${pid_to_kill} && ${pid_to_kill-_} ]]; then
    for ptk in "${pid_to_kill[@]}" ; do
        sudo kill -9 ${ptk}
    done
    fi

done


#array of commands to check for sql server to be up
this_dir=$(pwd)
cd ./fastapi/products/ 
. run.sh & 
this_pid=$?
fastapi_pids=("${this_pid}")
cd $this_dir
cd ./fastapi/customers/
. run.sh &
this_pid=$?
#fastapi_pids=+("${this_pid}")
fastapi_pids[${#fastapi_pids[@]}]="${this_pid}"
cd $this_dir
cd ./fastapi/finance/
. run.sh &
this_pid=$?
#fastapi_pids=+("${this_pid}")
fastapi_pids[${#fastapi_pids[@]}]="${this_pid}"
cd $this_dir

    for u_c in "${fastapi_pids[@]}"
    do
        echo "$u_c"
    done

sleep 2

for m_url in "${fast_api_urls[@]}"
do

    m_url_doc="${m_url}docs"
    echo "*************************************"
    echo " Waiting for URL to be up:"
    echo " $m_url_doc "
    echo "*************************************"
    sleep 1
    finished=false
    while ! $finished; do
        health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "${m_url_doc}")
        if [ $health_status == "200" ]; then
            finished=true
            echo "*********************************"
            echo "*  FastAPI Up:                   *"
            echo "   ${m_url_doc}"
            echo "*                                *"
            echo "*********************************"
            google-chrome "${m_url_doc}" &            
        else
            finished=false
        fi
    done

    

done

