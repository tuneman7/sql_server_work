#!/bin/bash

url="http://127.0.0.1:8026"  # Replace with your URL
interval=5  # Adjust the interval between requests in seconds

while true; do
    response_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$response_code" -eq 200 ]; then
        echo "up"
        break  # Exit the loop when the response code is 200
    else
        echo "Response code: $response_code"
    fi
    sleep "$interval"
done
