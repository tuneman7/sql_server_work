#!/bin/bash
gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8023 main:app --threads 20