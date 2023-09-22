#!/bin/bash

all_deps=1

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
sqlcmd -?>/dev/null
if [ $? -eq 0 ]; then
    echo "sqlcmd is installed"
else
    echo "*********************************"
    echo "sqlcmd is not installed -- exiting"
    echo "visit:"
    echo "https://askubuntu.com/questions/1407533/microsoft-odbc-v18-is-not-find-by-apt"
    echo "https://dba.stackexchange.com/questions/174277/getting-sqlcmd-sqlcmd-command-not-found-in-linux"    
    echo "*********************************"
all_deps=0

fi


if [ $? -eq 0 ]; then
    echo "zip is installed"
cat ./scr/msgs/deps_fail.txt
echo ""
export all_deps=$all_deps
fi


