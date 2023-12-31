#!/bin/bash

source ./chk_dps.sh

if [ $all_deps -eq 0 ]; then
    return
fi

NETWORK_NAME="ENTERPRISE_NETWORK1"
export NETWORK_NAME=$NETWORK_NAME
docker network create $NETWORK_NAME

VENV_NAME=sql_server_env

#individual database setups

#bigquery
bigquery_keyfile="$(pwd)/dbs/servers/bigquery/bigquery1/tokens/brave-sonar-367918-74b1d5b6db90.json"

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

#redis
redis_name=redis
redis_hostname=redis
redis=redis
redis_port=6379
redis_sn=127.0.0.1
redis_up="redis-cli -h "$redis_sn" -p "$redis_port" ping"


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

#pyspark
pyspark_name="spark_pyspark_jupyter"
pyspark_sn="127.0.0.1"
pyspark_port=8888

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
server_up_dkr_l_cmds+=("up_redis_dkr.sh")


#array of all bash files to destroy docker instances
server_down_dkr_l_cmds=("down_mssql1_dkr.sh")
server_down_dkr_l_cmds+=("down_mysql1_dkr.sh")
server_down_dkr_l_cmds+=("down_postsql1_dkr.sh")
server_down_dkr_l_cmds+=("down_redis_dkr.sh")
server_down_dkr_l_cmds+=("down_jupyter_dkr.sh")




#array all docker images
a_svr_dkr_img=($mssql1_name)
a_svr_dkr_img+=($mysql1_name)
a_svr_dkr_img+=($postsql1_name)
a_svr_dkr_img+=($redis_name)
a_svr_dkr_img+=("spark_pyspark_jupyter")

#array of commands to check for sql server to be up
a_server_up_inline_command=("${mssql1_up}")
a_server_up_inline_command+=("${mysql1_up}")
a_server_up_inline_command+=("${postsql1_up}")
a_server_up_inline_command+=("${redis_up}")


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
server_ports_used=("${mssql1_apiport}")
server_ports_used+=("${mysql1_apiport}")
server_ports_used+=("${postsql1_apiport}")
server_ports_used+=("${dashboard_port}")
server_ports_used+=("${dashboard_jn_port}")

# Exporting each URL as a separate environment variable
export BIGQUERY_API_URL="http://${bigquery_sn}:${bigquery_apiport}/docs"
export PRODUCTS_API_URL="http://${mssql1_sn}:${mssql1_apiport}/docs"
export CUSTOMERS_API_URL="http://${mysql1_sn}:${mysql1_apiport}/docs"
export FINANCE_API_URL="http://${postsql1_sn}:${postsql1_apiport}/docs"
export DASHBOARD_URL="http://${dashboard_host}:${dashboard_port}"
export DASHBOARD_JN_URL="http://${dashboard_jn_host}:${dashboard_jn_port}/?tree"
export PYSPARK_JN_URL="http://${pyspark_sn}:${pyspark_port}/?tree"

