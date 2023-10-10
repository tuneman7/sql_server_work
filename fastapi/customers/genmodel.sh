#!/bin/bash
sqlacodegen "mysql+mysqlconnector://root:Python2028@127.0.0.1/customers"  --outfile /data/sql_server_work/fastapi/customers/models.py
