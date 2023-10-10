#!/bin/bash

#get all variables not declared within file
#check dependencies
source ./env.sh


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
