#!/bin/bash
#view this link
#https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash
#and this one
#https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-docker-container-configure?view=sql-server-ver16&pivots=cs1-bash

#the link says you need to run the docker run as sa -- inaccurate.

source ./env.sh
echo "docker stop ${mssql1_name}"
docker stop ${mssql1_name}
docker rm -f ${mssql1_name}
#docker rm ${mssql1_hostname}
echo "docker rm ${mssql1_name}" --purge
sqldir=$(pwd)/sql_data_files/${mssql1}
mkdir $(pwd)/sql_data_files/${mssql1}
echo sqldir=$sqldir
echo mssql1_pwd=$mssql1_pwd
chmod -R 777 $sqldir
ls $sqldir
echo "about to create docker"
sudo docker run -v $(pwd)/sql_data_files/${mssql1}:/mnt/myhost/sql  -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=${mssql1_pwd}" \
   -p 1433:1433 --name ${mssql1_name} --hostname ${mssql1_hostname} \
   -d \
   mcr.microsoft.com/mssql/server:2019-latest 
   

