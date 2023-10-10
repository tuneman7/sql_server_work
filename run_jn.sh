#!/bin/bash
source ./env.sh
if ! [ -n "$VIRTUAL_ENV" ]; then
    if [ -d "./${VENV_NAME}" ]; then
        source ./${VENV_NAME}/bin/activate
    else
        . setup_venv.sh        
    fi
fi

jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token="" --NotebookApp.password="" --port=8888 --notebook-dir=./j_nbks

