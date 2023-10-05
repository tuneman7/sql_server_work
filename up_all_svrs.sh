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
echo "Bringing up SQL Servers in Docker"
echo "****************"
for m_mc in "${server_up_dkr_l_cmds[@]}"
do
echo "****************"
echo "Bringing up SQL Server"
echo "****************"
	. $m_mc
done

#docker ps --filter "name=${mssql1_name}"

#wait for a few seoncds then query docker to make sure they're up.

sleep 3

echo "****************"
echo "Looking at servers in docker"
echo "****************"

for m_i_nm in "${a_sql_dkr_img[@]}"
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


# for u_c in "${a_sql_inline_command[@]}"
# do
#     #run the bash command
#     echo "$u_c"
#     #add return code to array


# done
# return

finished=false
while ! $finished; do

    declare -a s_up=()

    for u_c in "${a_sql_inline_command[@]}"
    do
        echo "#!/bin/bash">my_runner.sh
        echo "$u_c">>my_runner.sh
        . my_runner.sh >/dev/null
        #add return code to array
        s_up+=($?)

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


. ./do_exit.sh


#check if the user wants to exit
if [[ "$do_exit" -eq 1 ]]
then

    #If yess, kill all the processes running fastapi / guinicorn
    for m_port in "${fast_api_ports[@]}"
    do

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

fi

