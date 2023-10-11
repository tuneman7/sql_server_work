#!/bin/bash
source ./env.sh
deactivate
rm -rf ./${VENV_NAME}
#. ir.sh

#check if the user wants to exit
if [[ "$do_exit" -eq 1 ]]
then

    #If yess, kill all the processes running fastapi / guinicorn
    for m_port in "${fast_api_ports[@]}"
    do

        pid_to_kill=$(lsof -t -i :$m_port -s TCP:LISTEN)

        echo "pid_to_kill=$pid_to_kill"

        #Check if the variable is defined and if it has values
        #and if it has values in it.
        if [[ $pid_to_kill && ${pid_to_kill-_} ]]; then
        for ptk in "${pid_to_kill[@]}" ; do
            sudo kill -9 ${ptk}
        done
        fi

    done

fi

