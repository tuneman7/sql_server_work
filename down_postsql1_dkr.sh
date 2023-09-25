#!/bin/bash
#view this link
#https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash
#and this one
#https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash

#the link says you need to run the docker run as sa -- inaccurate.

#get variables
source ./env.sh

mkdir -vp $postsql1_loc_dir
echo postsql1_loc_dir=$postsql1_loc_dir

echo "Changing permissions on \$postsql1_loc_dir"
sudo chmod -R 777 $postsql1_loc_dir

#back things up if they're there
this_day_id=$(date +"%Y%m%d")
backup_dir=$(pwd)/backups_sql_df/postsql/${postsql1_name}/${this_day_id}
echo backup_dir=$backup_dir
mkdir -vp $backup_dir

cp -rf $postsql1_loc_dir $backup_dir
echo "Changing permissions on \$backup_dir"
sudo chmod -R 777 $postsql1_loc_dir

#stop docker
echo "docker stop ${postsql1_name}"
docker stop ${postsql1_name}
docker rm -f ${postsql1_name}
echo "docker rm ${postsql1_name}"

#delete connector
cnctr_dir=$(pwd)/cnctr/postsql

rm -rf $cnctr_dir

echo ""


