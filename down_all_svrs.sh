#!/bin/bash
source ./env.sh

if [ $all_deps -eq 0 ]; then
echo ""
return
fi

echo "****************"
echo "Tearing down Servers in Docker"
echo "****************"
for m_mc in "${server_down_dkr_l_cmds[@]}"
do
echo "****************"
echo "Tearing down Server"
echo "****************"
	. $m_mc
done

#docker ps --filter "name=${mssql1_name}"

#wait for a few seoncds then query docker to make sure they're up.

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
