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
mssql1_sn=127.0.0.1
mssql1_up="sqlcmd -S ${mssql1_sn} -U SA -P ${mssql1_pwd} -C -Q 'exit()'"
mssql1_apiport=8023
mssql1_apidir=$(pwd)/fastapi/products

#mysql
mysql1_name=mysql1
mysql1_hostname=mysql1
mysql1=mysql1
mysql1_pwd=Python2028
mysql1_loc_dir=$(pwd)/sql_data_files/mysql/${mysql1}
mysql1_port=3306
mysql1_sn=127.0.0.1
mysql1_up="mysql -h ${mysql1_sn} -u root -p'${mysql1_pwd}' -e'SHOW PROCESSLIST' 2>/dev/null"
mysql1_apiport=8024
mysql1_apidir=$(pwd)/fastapi/customers

#postgress
postsql1_name=postsql1
postsql1_hostname=postsql1
postsql1=postsql1
postsql1_pwd=Python2028
postsql1_loc_dir=$(pwd)/sql_data_files/postsql/${postsql1}
postsql1_port=5432
postsql1_sn=127.0.0.1
postsql1_up="PGPASSWORD=${postsql1_pwd} psql -h ${postsql1_sn} -U postgres -p'${postsql1_port}' -c'SELECT version()' >/dev/null"
postsql1_apiport=8025
postsql1_apidir=$(pwd)/fastapi/finance


mssql_servers=($mssql1)

#array of all bash files to create docker instances
server_up_dkr_l_cmds=("up_mysql1_dkr.sh")
server_up_dkr_l_cmds+=("up_mssql1_dkr.sh")
server_up_dkr_l_cmds+=("up_postsql1_dkr.sh")

#array of all bash files to destroy docker instances
server_down_dkr_l_cmds=("down_mssql1_dkr.sh")
server_down_dkr_l_cmds+=("down_mysql1_dkr.sh")
server_down_dkr_l_cmds+=("down_postsql1_dkr.sh")

#array all docker images
a_sql_dkr_img=($mssql1_name)
a_sql_dkr_img+=($mysql1_name)
a_sql_dkr_img+=($postsql1_name)

#array of commands to check for sql server to be up
a_sql_inline_command=("${mssql1_up}")
a_sql_inline_command+=("${mysql1_up}")
a_sql_inline_command+=("${postsql1_up}")

#array of commands to generate models from databases
of=$(pwd)/fastapi/products/genmodel.sh
a_gen_models=("${of}")
of=$(pwd)/fastapi/finance/genmodel.sh
a_gen_models+=("${of}")
of=$(pwd)/fastapi/customers/genmodel.sh
a_gen_models+=("${of}")

