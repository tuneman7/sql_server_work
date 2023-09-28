#!/bin/bash
gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8025 main:app --threads 20