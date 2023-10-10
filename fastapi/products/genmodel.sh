#!/bin/bash
sqlacodegen "mssql+pyodbc://sa:Python2028@127.0.0.1/products?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"  --outfile /data/sql_server_work/fastapi/products/models.py
