#!/bin/bash
#view this link
#https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash
#and this one
#https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash

#the link says you need to run the docker run as sa -- inaccurate.

#get variables
source ./env.sh

mkdir -vp $mysql1_loc_dir
echo mysql1_loc_dir=$mysql1_loc_dir

echo "Changing permissions on \$mysql1_loc_dir"
sudo chmod -R 777 $mysql1_loc_dir

#back things up if they're there
this_day_id=$(date +"%Y%m%d")
backup_dir=$(pwd)/backups_sql_df/mysql/${mysql1_name}/${this_day_id}
echo backup_dir=$backup_dir
mkdir -vp $backup_dir

cp -rf $mysql1_loc_dir $backup_dir
echo "Changing permissions on \$backup_dir"
sudo chmod -R 777 $mysql1_loc_dir

#stop docker
echo "docker stop ${mysql1_name}"
docker stop ${mysql1_name}
docker rm -f ${mysql1_name}
echo "docker rm ${mysql1_name}"

#delete connector
cnctr_dir=$(pwd)/cnctr/mysql

mkdir -vp $cnctr_dir

of=${cnctr_dir}/${mysql1_hostname}.sh

rm -rf $of

echo ""


