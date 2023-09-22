#!/bin/bash
source ./env.sh

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
