#!/bin/bash
source ./env.sh
if ! [ -n "$VIRTUAL_ENV" ]; then
    if [ -d "./${VENV_NAME}" ]; then
        source ./${VENV_NAME}/bin/activate
    else
        . setup_venv.sh        
    fi
fi



