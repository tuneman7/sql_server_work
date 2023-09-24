#!/bin/bash
#view this link
#https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash
#and this one
#https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash

#the link says you need to run the docker run as sa -- inaccurate.

#get variables
source ./env.sh

#stop docker
echo "docker stop ${mssql1_name}"
docker stop ${mssql1_name}
docker rm -f ${mssql1_name}
echo "docker rm ${mssql1_name}"


mkdir -vp $mssql1_loc_dir
echo mssql1_loc_dir=$mssql1_loc_dir

echo "Changing permissions on \$mssql1_loc_dir"
sudo chmod -R 777 $mssql1_loc_dir

#back things up if they're there
this_day_id=$(date +"%Y%m%d")
backup_dir=$(pwd)/backups_sql_df/mssql/${mssql1_name}/${this_day_id}
echo backup_dir=$backup_dir
mkdir -vp $backup_dir

cp -rf $mssql1_loc_dir $backup_dir
echo "Changing permissions on \$backup_dir"
sudo chmod -R 777 $mssql1_loc_dir

#test
#get rid of db directory
rm -rf $mssql1_loc_dir
mkdir -vp $mssql1_loc_dir
sudo chmod -R 777 $mssql1_loc_dir

echo mssql1_pwd=$mssql1_pwd

echo "about to create docker"
docker run -v $mssql1_loc_dir:/var/opt/mssql  -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=${mssql1_pwd}" \
   -p $mssql1_port:1433 --name ${mssql1_name} --hostname ${mssql1_hostname} \
   -d \
   mcr.microsoft.com/mssql/server:2022-latest

#create firewall rule so other boxes on the network can see it.
echo "updating firewall rules for port:$mssql1_port"
sudo ufw allow $mssql1_port

#add it to the array of docker images
a_sql_dkr_img+=($mssql1_name)
#export a_sql_dkr_img=$a_sql_dkr_img



#create a connector based on template
cnctr_dir=$(pwd)/cnctr/mssql

mkdir -vp $cnctr_dir

export mssql_pw=$mssql1_pwd
export mssql_svr=$mssql1_sn

config_file=$(pwd)/templates/cnctr_template_mssql.txt

of=${cnctr_dir}/${mssql1_hostname}.sh

envsubst < $config_file > $of

echo cf=$of

cat $of
echo ""


