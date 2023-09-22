#!/bin/bash
source ./env.sh
deactivate
rm -rf ./${VENV_NAME}
python3 -m venv ${VENV_NAME}
source ./${VENV_NAME}/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
#. ir.sh
