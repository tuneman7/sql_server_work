#!/bin/bash
source ./env.sh

#if not all dependencies are set up
#get out of here
if [ $all_deps -eq 0 ]; then
    return
fi

deactivate
rm -rf ./${VENV_NAME}
python -m venv ${VENV_NAME}
source ./${VENV_NAME}/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

#create libraries symlink so jn can run isolated without
#root dir being cluttered

source_dir=$(pwd)/libraries
target_dir=$(pwd)/j_nbks/libraries

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi


source_dir=$(pwd)/db_artifacts
target_dir=$(pwd)/j_nbks/db_artifacts

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi

source_dir=$(pwd)/data
target_dir=$(pwd)/j_nbks/data

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi




#. ir.sh
