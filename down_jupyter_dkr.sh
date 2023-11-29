#!/bin/bash

#get variables
source ./env.sh


#stop docker
echo "docker stop ${pyspark_name}"
docker stop ${pyspark_name}
docker rm -f ${pyspark_name}
echo "docker rm ${pyspark_name}"


#add it to the array of docker images

echo ""


