#!/bin/bash

#clear out any pycache folders 
find . -type d -name __pycache__ -exec rm -r {} \+



gunicorn --bind 0.0.0.0:8026 app:app --threads 20 &

echo ""
echo "*********************************"
echo "Waiting for Dashboard to come up:"
echo "http://127.0.0.1:8026"
echo "*********************************"

finished=false
while ! $finished; do
    response_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://127.0.0.1:8026")
    if [ "$response_code" -eq 200 ]; then
        finished=true
        echo "*********************************"
        echo "* Flask is ready:               *"
        echo "  http://127.0.0.1:8026"
        echo "*********************************"
    else
        finished=false
    fi
done

