#!/bin/bash



echo ""
echo "*********************************"
echo "Waiting for Dashboard to come up:"
echo "http://127.0.0.1:8027/tree"
echo "*********************************"

nohup jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token="" --NotebookApp.password="" --port=8027 --notebook-dir=./j_nbks > jupyter.log 2>&1 &

finished=false
while ! $finished; do
    response_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://127.0.0.1:8027/tree")
    if [ "$response_code" -eq 200 ]; then
        finished=true
        echo "*********************************"
        echo "* Jupyter is ready:             *"
        echo "  http://127.0.0.1:8027/tree?"
        echo "*********************************"
    else
        finished=false
    fi
done

