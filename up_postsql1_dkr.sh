#!/bin/bash
#view this link
#https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash
#and this one
#https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash

#the link says you need to run the docker run as sa -- inaccurate.

#get variables
source ./env.sh

#stop docker
echo "docker stop ${postsql1_name}"
docker stop ${postsql1_name}
docker rm -f ${postsql1_name}
echo "docker rm ${postsql1_name}"


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

#test
get rid of db directory
rm -rf $postsql1_loc_dir
mkdir -vp $postsql1_loc_dir
sudo chmod -R 777 $postsql1_loc_dir

echo postsql1_pwd=$postsql1_pwd

echo "about to create docker"
	
#docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
docker run -v $postsql1_loc_dir:/var/lib/postgresql/data  -e "POSTGRES_PASSWORD=${postsql1_pwd}" \
   -p $postsql1_port:5432 --name ${postsql1_name} --hostname ${postsql1_hostname} \
   -d \
   postgres


#create firewall rule so other boxes on the network can see it.
echo "updating firewall rules for port:$postsql1_port"
sudo ufw allow $postsql1_port


#create a connector based on template
cnctr_dir=$(pwd)/cnctr/postsql

mkdir -vp $cnctr_dir

export postsql_pw=$postsql1_pwd
export postsql_svr=$postsql1_sn

config_file=$(pwd)/templates/cnctr_template_postsql.txt

of=${cnctr_dir}/${postsql1_hostname}.sh

envsubst < $config_file > $of

echo cf=$of

cat $of
cp $of $cnctr_dir/$postsql1_sn.sh
echo ""
echo postsql1_up=$postsql1_up

