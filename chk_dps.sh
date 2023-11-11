#!/bin/bash

export all_deps=1

redis-cli --version>/dev/null
if [ $? -eq 0 ]; then
    echo "redis-cli is installed"
else
    echo "*********************************"
    echo "redis-cli is not installed -- exiting"
    echo " run sudo apt install redis-tools "
    echo "*********************************"
all_deps=0
    #return
fi


jq --version>/dev/null
if [ $? -eq 0 ]; then
    echo "jq is installed"
else
    echo "*********************************"
    echo "jq is not installed -- exiting"
    echo "visit:"
    echo "https://jqlang.github.io/jq/download/"
    echo "*********************************"
all_deps=0
    #return
fi

zip --version>/dev/null
if [ $? -eq 0 ]; then
    echo "zip is installed"
else
    echo "*********************************"
    echo "zip is not installed -- exiting"
    echo "visit:"
    echo "https://www.tecmint.com/install-zip-and-unzip-in-linux/#zipubuntu"
    echo "*********************************"
all_deps=0

fi

#exalmple
/opt/mssql-tools18/bin/sqlcmd -?>/dev/null
if [ $? -eq 0 ]; then
    echo "/opt/mssql-tools18/bin/sqlcmd is installed"
else
    echo "*********************************"
    echo "/opt/mssql-tools18/bin/sqlcmd is not installed -- exiting"
    echo "visit:"
    echo "https://askubuntu.com/questions/1407533/microsoft-odbc-v18-is-not-find-by-apt"
    echo "https://dba.stackexchange.com/questions/174277/getting-/opt/mssql-tools18/bin/sqlcmd-/opt/mssql-tools18/bin/sqlcmd-command-not-found-in-linux"    
    echo "*********************************"
all_deps=0

fi

#exalmple
mysql --help>/dev/null
if [ $? -eq 0 ]; then
    echo "mysql is installed"
else
    echo "*********************************"
    echo "mysql is not installed -- exiting"
    echo "visit:"
    echo ""
    echo "sudo apt-get install mysql-client"    
    echo "*********************************"
all_deps=0

fi

#exalmple
psql --help>/dev/null
if [ $? -eq 0 ]; then
    echo "psql is installed"
else
    echo "*********************************"
    echo "psql is not installed -- exiting"
    echo "visit:"
    echo ""
    echo "sudo apt install postgresql-client-common"
    echo "sudo apt-get install -y postgresql-client"    
    echo "*********************************"
all_deps=0

fi

#exalmple
pip >/dev/null
if [ $? -eq 0 ]; then
    echo "pip is installed"
else
    echo "*********************************"
    echo "pip is not installed -- exiting"
    echo "visit:"
    echo ""
    echo "apt install python3-pip"    
    echo "*********************************"
all_deps=0

fi


#exalmple
gunicorn --help >/dev/null
if [ $? -eq 0 ]; then
    echo "gunicorn is installed"
else
    echo "*********************************"
    echo "gunicorn is not installed -- exiting"
    echo "visit:"
    echo ""
    echo "apt install gunicorn"    
    echo "*********************************"
all_deps=0

fi

#exalmple
gcloud --help >/dev/null
if [ $? -eq 0 ]; then
    echo "gcloud is installed"
else
    echo "*********************************"
    echo "gcloud is not installed -- exiting"
    echo "try:"
    echo ""
    echo "curl https://sdk.cloud.google.com | bash"    
    echo "*********************************"
all_deps=0

fi







if [ $all_deps -eq 0 ]; then
    echo "zip is installed"
cat ./scr/msgs/deps_fail.txt
echo ""
export all_deps=$all_deps
fi


