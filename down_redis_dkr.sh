#!/bin/bash

#get variables
source ./env.sh


#stop docker
echo "docker stop ${redis_name}"
docker stop ${redis_name}
docker rm -f ${redis_name}
echo "docker rm ${redis_name}"


#add it to the array of docker images
a_svr_dkr_img+=($redis_name)
export a_svr_dkr_img=$a_svr_dkr_img


echo ""


