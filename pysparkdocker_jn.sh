#!/bin/bash

# Name of the Docker image and container
IMAGE_NAME="spark_pyspark_jupyter"
CONTAINER_NAME="spark_pyspark_jupyter"
DOCKERFILE_PATH="Dockerpyspark"
NETWORK_NAME="ENTERPRISE_NETWORK1"
export NETWORK_NAME=$NETWORK_NAME
docker network create $NETWORK_NAME

sudo chmod -R 777 ./

# Function to check if a Docker image exists
check_image_exists() {
    docker image inspect $IMAGE_NAME > /dev/null 2>&1
}

# Function to remove a Docker image
remove_image() {
    docker rmi -f $IMAGE_NAME
}

# Function to check and remove an existing container with the same name
check_and_remove_container() {
    if [ "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
        echo "Removing existing container with name $CONTAINER_NAME."
        docker rm -f $CONTAINER_NAME
    fi
}

# Function to build a Docker image
build_image() {
    docker build -f $DOCKERFILE_PATH -t $CONTAINER_NAME .
}

# Function to run the Docker container
run_container() {
    check_and_remove_container
    docker run -p 8888:8888 -v "$PWD":/workspace -d --name ${CONTAINER_NAME} --network $NETWORK_NAME $IMAGE_NAME
}
docker stop $CONTAINER_NAME
# Main script logic
if check_image_exists; then
    # while true; do
    #     echo "*********************************"
    #     read -p "* Image $IMAGE_NAME exists. Remove and rebuild? (y/n) " answer
    #     echo "*********************************"
    #     case $answer in
    #         [Yy]* ) remove_image; build_image; echo "Image $IMAGE_NAME has been rebuilt."; break;;
    #         [Nn]* ) echo "Using existing image to run the container."; break;;
    #         * ) echo "Please answer 'y' or 'n'.";;
    #     esac
    # done
    run_container
    echo "Container with image $IMAGE_NAME is running."
else
    echo "Image $IMAGE_NAME does not exist. Building image..."
    build_image
    echo "Image $IMAGE_NAME has been built."
    run_container
    echo "Container with image $IMAGE_NAME is running."
fi

echo ""
echo "*********************************"
echo "* Waiting for Jupyter to come up:"
echo "* http://127.0.0.1:8888          *"
echo "*********************************"

finished=false
while ! $finished; do
    response_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://127.0.0.1:8888/tree?")
    if [ "$response_code" -eq 200 ]; then
        finished=true
        echo "*********************************"
        echo "* Jupyter is ready:             *"
        echo "* http://127.0.0.1:8888/tree?   *"
        echo "*********************************"
    else
        finished=false
    fi
done

# URLs to open
URL1="http://localhost:8888"

# Open URLs in new tabs in Google Chrome
google-chrome "$URL1" &



# while true; do
#     echo "*********************************"
#     echo "*                               *"
#     echo "*    Do you wish to exit?       *"
#     echo "* (this will shut down Jupyter) *"
#     echo "*                               *"
#     echo "*********************************"
#     read -p "Do you wish to exit? [y/n]:" yn
#     case $yn in
#         [Yy]* ) echo "Exiting..."; docker stop $CONTAINER_NAME; break;;
#         [Nn]* ) echo "Continuing..."; break;;
#         * ) echo "Please answer 'y' or 'n'.";;
#     esac
# done



sudo chmod -R 777 ./

#microk8s kubectl get pods | grep $CONTAINER_NAME
