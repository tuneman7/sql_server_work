#!/bin/bash
#view this link
#https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash
#and this one
#https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash

#the link says you need to run the docker run as sa -- inaccurate.

#get variables
source ./env.sh

#stop docker
echo "docker stop ${mysql1_name}"
docker stop ${mysql1_name}
docker rm -f ${mysql1_name}
echo "docker rm ${mysql1_name}"


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

#remove the files so I can start from scratch
rm -rf $mysql1_loc_dir
mkdir -vp $mysql1_loc_dir
echo mysql1_loc_dir=$mysql1_loc_dir

echo "Changing permissions on \$mysql1_loc_dir"
sudo chmod -R 777 $mysql1_loc_dir


echo mysql1_pwd=$mysql1_pwd

echo "about to create docker"
docker run -v $mysql1_loc_dir:/var/lib/mysql -e "MYSQL_ROOT_PASSWORD=${mysql1_pwd}" \
   -p $mysql1_port:3306 --name ${mysql1_name} --hostname ${mysql1_hostname} \
   -d \
   mysql:latest

#create firewall rule so other boxes on the network can see it.
echo "updating firewall rules for port:$mysql1_port"
sudo ufw allow $mysql1_port


#create a connector based on template
cnctr_dir=$(pwd)/cnctr/mysql

mkdir -vp $cnctr_dir

export mysql_pw=$mysql1_pwd
export mysql_svr=$mysql1_sn

config_file=$(pwd)/templates/cnctr_template_mysql.txt

of=${cnctr_dir}/${mysql1_hostname}.sh

envsubst < $config_file > $of

my_sql_up="$(envsubst < $config_file) -e'SHOW PROCESSLIST'"
echo my_sql_up=$my_sql_up

echo cf=$of

cat $of
cp $of $cnctr_dir/$mysql1_sn.sh
echo ""


echo "************************"
echo "Setting Up Fastapi connectors"
echo "************************"
config_file=$(pwd)/fastapi/customers/templates/connector.template

of=$(pwd)/fastapi/customers/connector.py

envsubst < $config_file > $of

echo cf=$of
chmod 777 $of

export mysql1_apiport=$mysql1_apiport

config_file=$(pwd)/fastapi/customers/templates/genmodel.template

of=$(pwd)/fastapi/customers/genmodel.sh

export mysql1_apidir=$mysql1_apidir

envsubst < $config_file > $of

echo cf=$of
chmod 777 $of

config_file=$(pwd)/fastapi/customers/templates/run.template

of=$(pwd)/fastapi/customers/run.sh

envsubst < $config_file > $of

echo cf=$of
chmod 777 $of


echo "************************"
echo "Setting Up Symlinks"
echo "************************"


#putting symlinks into api directories
source_dir=$(pwd)/libraries/
target_dir=${mysql1_apidir}/libraries
rm -rf $target_dir


if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi


source_dir=$(pwd)/db_artifacts/
target_dir=${mysql1_apidir}/db_artifacts
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi

source_dir=$(pwd)/data/
target_dir=${mysql1_apidir}/data
rm -rf $target_dir

if ! [ -d "${target_dir}" ]; then
    ln -s $source_dir $target_dir
fi

