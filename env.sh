#!/bin/bash

source ./chk_dps.sh

VENV_NAME=sql_server_env


#individual database setups

#sql_server
mssql1_name=mssql1
mssql1_hostname=mssql1
mssql1=mssql1
mssql1_pwd=Python2028
mssql1_loc_dir=$(pwd)/sql_data_files/mssql/${mssql1}
mssql1_port=1433
mssql1_sn=localhost

#mysql
mysql1_name=mysql1
mysql1_hostname=mysql1
mysql1=mysql1
mysql1_pwd=Python2028
mysql1_loc_dir=$(pwd)/sql_data_files/mysql/${mysql1}
mysql1_port=3306
mysql1_sn=localhost


mssql_servers=($mssql1)

#array of all bash files to create docker instances
server_up_dkr_l_cmds=("up_mssql1_dkr.sh")
server_up_dkr_l_cmds+=("up_mysql1_dkr.sh")

#array of all bash files to destroy docker instances
server_down_dkr_l_cmds=("down_mssql1_dkr.sh")
server_down_dkr_l_cmds+=("down_mysql1_dkr.sh")

#array all docker images
a_sql_dkr_img=($mssql1_name)
a_sql_dkr_img+=($mysql1_name)



