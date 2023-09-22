#!/bin/bash

VENV_NAME=sql_server_env


#individual database setups
mssql1_name=mssql1
mssql1_hostname=mssql1
mssql1=mssql1
mssql1_pwd=Python2028
mssql1_loc_dir=$(pwd)/sql_data_files/mssql/${mssql1}
mssql1_port=1433
mssql1_sn=localhost

msql_servers=($mssql1)

#array of all bash files to create docker instances
server_up_dkr_l_cmds=("up_mssql1_dkr.sh")

#array of all bash files to destroy docker instances
server_down_dkr_l_cmds=("down_mssql1_dkr.sh")

#array all docker images
a_sql_dkr_img=()



