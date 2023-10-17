#!/bin/bash

source ./chk_dps.sh

if [ $all_deps -eq 0 ]; then
    return
fi


VENV_NAME=sql_server_env

#individual database setups

#bigquery
bigquery_keyfile="$(pwd)/dbs/servers/bigquery/tokens/brave-sonar-367918-74b1d5b6db90.json"

bigquery_name=bigquery1
bigquery_hostname=bigquery1
bigquery1=bigquery1
bigquery_pwd=Python2028
bigquery_loc_dir=$(pwd)/sql_data_files/bigquery/${bigquery1}
bigquery_port=1433
bigquery_sn=127.0.0.1
bigquery_up="bq ls"
bigquery_apiport=8028
bigquery_apidir=$(pwd)/fastapi/site_traffic

site_traffic_api_url="http://${bigquery_sn}:${bigquery_apiport}/"
export site_traffic_api_url=$site_traffic_api_url


#sql_server
mssql1_name=mssql1
mssql1_hostname=mssql1
mssql1=mssql1
mssql1_pwd=Python2028
mssql1_loc_dir=$(pwd)/sql_data_files/mssql/${mssql1}
mssql1_port=1433
mssql1_sn=127.0.0.1
mssql1_up="/opt/mssql-tools18/bin/sqlcmd -S ${mssql1_sn} -U SA -P ${mssql1_pwd} -C -Q 'exit()'"
mssql1_apiport=8023
mssql1_apidir=$(pwd)/fastapi/products

products_api_url="http://${mssql1_sn}:${mssql1_apiport}/"
export products_api_url=$products_api_url

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

customers_api_url="http://${mysql1_sn}:${mysql1_apiport}/"
export customers_api_url=$customers_api_url

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

finance_api_url="http://${postsql1_sn}:${postsql1_apiport}/"
export finance_api_url=$finance_api_url


#put fastapi urls into array:
#array of all bash files to destroy docker instances
fast_api_urls=("${products_api_url}")
fast_api_urls+=("${customers_api_url}")
fast_api_urls+=("${finance_api_url}")


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



#Dashboard configuration
dashboard_port=8026
dashboard_path=$(pwd)/dashboard
dashboard_host=127.0.0.1
dashboard_url="http://${dashboard_host}:${dashboard_port}"

#Dashboard Jupyter
dashboard_jn_port=8027
dashboard_jn_path=$(pwd)/dashboard/j_nbks
dashboard_jn_host=127.0.0.1
dashboard_jn_url="http://${dashboard_jn_host}:${dashboard_jn_port}"


#array of ports used by fastapi or dasboard
fast_api_ports=("${mssql1_apiport}")
fast_api_ports+=("${mysql1_apiport}")
fast_api_ports+=("${postsql1_apiport}")
fast_api_ports+=("${dashboard_port}")
fast_api_ports+=("${dashboard_jn_port}")


