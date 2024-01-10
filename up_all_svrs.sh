#!/bin/bash

#get all variables not declared within file
#check dependencies
source ./env.sh

#clear out pycache
#find . -type d -name __pycache__ -exec rm -r {} \+

if ! [ -n "$VIRTUAL_ENV" ]; then
    if [ -d "./${VENV_NAME}" ]; then
        source ./${VENV_NAME}/bin/activate
    else
        . setup_venv.sh        
    fi
fi


if [ $all_deps -eq 0 ]; then
echo ""
return
fi

echo "****************"
echo "Bringing up Servers in Docker"
echo "****************"
for m_mc in "${server_up_dkr_l_cmds[@]}"
do
echo "****************"
echo "Bringing up Server"
echo "****************"
	. $m_mc
done

#docker ps --filter "name=${mssql1_name}"
echo "****************"
echo "Bringing up pyspark docker image"
echo "****************"

. ./pysparkdocker_jn.sh

echo "****************"
echo "Finished bringing up pyspark docker image"
echo "****************"

#wait for a few seoncds then query docker to make sure they're up.

sleep 3

echo "****************"
echo "Looking at servers in docker"
echo "****************"

for m_i_nm in "${a_svr_dkr_img[@]}"
do
echo "****************"
echo "Looking looking at $m_i_nm"
echo "****************"
    echo "docker ps -a --filter \"name=$m_i_nm\" "
    docker ps -a --filter "name=$m_i_nm"
done

echo "****************"
echo "Checking if database servers are up"
echo "****************"


finished=false
while ! $finished; do

    declare -a s_up=()

    for u_c in "${a_server_up_inline_command[@]}"
    do
        echo "#!/bin/bash">my_runner.sh
        echo "$u_c">>my_runner.sh
        . my_runner.sh >/dev/null
        #add return code to array
        s_up+=($?)

        sleep 1
    done
    rm my_runner.sh

    allup=true
    #loop through my return codes
    for i in "${s_up[@]}"
    do
        #echo "$i"

        if [[ $i -eq 1 ]]
        then
            allup=false
        fi

    done

    finished=$allup

done
echo""
echo "****************"
echo "All databases servers up"
echo "****************"

echo""

echo "****************"
echo "Setting up databases"
echo "****************"

time python setup_dbs.py -a setup_dbs

echo "****************"
echo "setup complete"
echo "****************"

echo "****************"
echo "Populating Databases"
echo "****************"

time python setup_dbs.py -a populate_dbs

echo "****************"
echo "Database Population Complete"
echo "****************"


echo "****************"
echo "Trying to bring up fastapi models"
echo "****************"

# sqlacodegen "postgresql://postgres:${postsql_pw}@${postsql_svr}/finance"  --outfile ${postsql1_apidir}/models.py

# echo "python setup_dbs.py -a create_model_files -i ${postsql1_apidir}/models.py -o ${postsql1_apidir}/models"
# python setup_dbs.py -a create_model_files -i ${postsql1_apidir}/models.py -o ${postsql1_apidir}/models
# python setup_dbs.py -a create_model_files -i ${postsql1_apidir}/models

    for u_c in "${a_gen_models[@]}"
    do
        echo "#!/bin/bash">my_runner.sh
        echo "$u_c">>my_runner.sh
        chmod 777 my_runner.sh
        . my_runner.sh >/dev/null
        #add return code to array
        s_up+=($?)

    done
    rm my_runner.sh


echo "****************"
echo "Pydantic fastapi up"
echo "****************"

echo "****************"
echo "Spinning up FASTAPI front-ends"
echo "****************"

. ./spin_up_fastapi.sh

echo "****************"
echo "Completed up FASTAPI front-ends"
echo "****************"


echo "****************"
echo "Spinning up DASHBOARD"
echo "****************"

. ./spin_up_dashboard.sh

echo "****************"
echo "Completed Spinning up DASHBOARD"
echo "****************"


if [ -n "$skip_venv" ] && [ $skip_venv -eq 1 ]; then

    #because there are background servers running continually
    #this will never exit.
    wait

else
   echo "No override letting it through."
fi

#open up bigquery
google-chrome "https://console.cloud.google.com/bigquery?hl=en&project=brave-sonar-367918&ws=!1m0" &

sleep 1
#open redshift
google-chrome "https://us-west-2.console.aws.amazon.com/sqlworkbench/home?region=us-west-2#/client" &

sleep 1

#because there are background port forwarding commands running continually
#this will never exit.
#wait

. ./do_exit.sh


#check if the user wants to exit
if [[ "$do_exit" -eq 1 ]]
then
rm server_ports_used.txt
touch server_ports_used.txt
    #If yess, kill all the processes running fastapi / guinicorn
    for m_port in "${server_ports_used[@]}"
    do
        echo $m_port >>server_ports_used.txt

        pid_to_kill=$(lsof -t -i :$m_port -s TCP:LISTEN)

        echo "pid_to_kill=$pid_to_kill"

        #Check if the variable is defined and if it has values
        #and if it has values in it.
        if [[ $pid_to_kill && ${pid_to_kill-_} ]]; then
        for ptk in "${pid_to_kill[@]}" ; do
            sudo kill -9 ${ptk}
        done
        fi

    done
. down_all_svrs.sh
fi

