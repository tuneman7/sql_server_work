#!/bin/bash


#get variables
source ./env.sh

#stop redis
echo "redis stop ${redis_name}"
docker stop ${redis_name}
docker rm -f ${redis_name}
echo "redis rm ${redis_name}"


echo "about to create redis"
docker run  \
   -p $redis_port:6379 --name ${redis_name} --hostname ${redis_hostname} \
   -d \
   redis:alpine

#create firewall rule so other boxes on the network can see it.
echo "updating firewall rules for port:$redis_port"
sudo ufw allow $redis_port




