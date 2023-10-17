#!/bin/bash

#view this link
#https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash
#and this one
#https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash

#the link says you need to run the docker run as sa -- inaccurate.

#get variables
source ./env.sh



#create a connector based on template
cnctr_dir=$(pwd)/cnctr/bigquery

mkdir -vp $cnctr_dir

export mssql_pw=$mssql1_pwd
export mssql_svr=$mssql1_sn

config_file="$(pwd)/templates/cnctr_template_bigquery.txt"

of=${cnctr_dir}/bigquery1.sh

export bigquery_keyfile=$bigquery_keyfile

envsubst < $config_file > $of

echo cf=$of

cat $of
echo ""

. $of


this_dir=$(pwd)/fastapi/site_traffic

mkdir -v $this_dir

echo "************************"
echo "Setting Up Fastapi connectors"
echo "************************"
config_file=$(pwd)/fastapi/site_traffic/templates/connector.template

of=$(pwd)/fastapi/site_traffic/connector.py

envsubst < $config_file > $of

echo cf=$of
chmod 777 $of

export bigquery_apiport=$bigquery_apiport

config_file=$(pwd)/fastapi/site_traffic/templates/genmodel.template

of=$(pwd)/fastapi/site_traffic/genmodel.sh

export bigquery_apidir=$bigquery_apidir

envsubst < $config_file > $of

echo cf=$of
chmod 777 $of

config_file=$(pwd)/fastapi/site_traffic/templates/run.template

of=$(pwd)/fastapi/site_traffic/run.sh

envsubst < $config_file > $of

echo cf=$of
chmod 777 $of


echo "************************"
echo "Setting Up Symlinks"
echo "************************"


#putting symlinks into api directories
source_dir=$(pwd)/libraries/
target_dir=${bigquery_apidir}/libraries
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi


source_dir=$(pwd)/db_artifacts/
target_dir=${bigquery_apidir}/db_artifacts
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi

source_dir=$(pwd)/data/
target_dir=${bigquery_apidir}/data
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi

