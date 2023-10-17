#!/bin/bash
source ./env.sh

#if not all dependencies are set up
#get out of here
if [ $all_deps -eq 0 ]; then
    return
fi

if [ -n "$skip_venv" ] && [ $skip_venv -eq 1 ]; then
    echo "Skipping Virtual Environment"
else
    deactivate
    rm -rf ./${VENV_NAME}
    python -m venv ${VENV_NAME}
    source ./${VENV_NAME}/bin/activate
fi


pip install --upgrade pip
pip install -r requirements.txt


#setup bigquery as needed
pip install google-cloud-bigquery


#create libraries symlink so jn can run isolated without
#root dir being cluttered

source_dir=$(pwd)/libraries/
target_dir=$(pwd)/j_nbks/libraries
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi


source_dir=$(pwd)/db_artifacts/
target_dir=$(pwd)/j_nbks/db_artifacts
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi

source_dir=$(pwd)/data/
target_dir=$(pwd)/j_nbks/data
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi



