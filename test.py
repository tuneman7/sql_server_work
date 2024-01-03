from libraries.utility import Utility as mutil
import boto3 
import psycopg2
import pandas as pd
import os

u = mutil()

filename = os.path.join(u.get_this_dir(),"outfile.csv")


result_df = pd.read_csv(filename)


#AWS Redshift Credentials
import json
import os
from io import StringIO

#Path to the uploaded file using os.path.join
#dbs/servers/redshift/test_data/tokens
file_path = os.path.join(u.get_this_dir(),"dbs","servers","redshift","test_data","tokens","redshift_iam.json")

# Opening the JSON file
with open(file_path, 'r') as file:
    credentials = json.load(file)

# Storing the credentials in variables
AWS_redshift_access_key = credentials.get('access_key')
AWS_redshift_secret_access_key = credentials.get('secret_access_key')
AWS_redshift_database = credentials.get('redshift_database')
AWS_redshift_admin_user = credentials.get('redshift_admin_user')
AWS_redshift_admin_pw = credentials.get('redshift_admin_pw')
bucket_name = credentials.get('bucket_name')

#S3 Bucket Details
bucket_name = bucket_name
object_name = 'your-object-name.csv'

# Save DataFrame to an in-memory buffer
csv_buffer = StringIO()
result_df.to_csv(csv_buffer, index=False)

# Create S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_redshift_access_key, aws_secret_access_key=AWS_redshift_secret_access_key)

# Upload the DataFrame to S3
s3_client.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key=object_name)


print("completed the s3 upload")


import psycopg2

# JDBC URL details
jdbc_url = "jdbc:redshift://shift4-example.789668808708.us-west-2.redshift-serverless.amazonaws.com:5439/dev"
split_url = jdbc_url.split("//")[1].split(":")
redshift_endpoint = split_url[0]
redshift_port = split_url[1].split("/")[0]
AWS_redshift_database = split_url[1].split("/")[1]

# Establish a connection to Redshift
conn = psycopg2.connect(
    dbname=AWS_redshift_database,
    user=AWS_redshift_admin_user,
    password=AWS_redshift_admin_pw,
    host=redshift_endpoint,
    port=redshift_port
)
cursor = conn.cursor()

create_table_sql = f"""
CREATE TABLE IF NOT EXISTS financial_data
(
  customer_id BIGINT,
  f_name VARCHAR(255),
  l_name VARCHAR(255),
  product_name VARCHAR(255),
  product_type VARCHAR(255),
  amt_usd VARCHAR(255),
  post_date TIMESTAMP,
  channel_desc VARCHAR(255),
  partner_desc VARCHAR(255),
  location_name VARCHAR(255),
  account_name VARCHAR(255),
  account_type VARCHAR(255)
);
"""

# Execute the create table command
cursor.execute(create_table_sql)

s3_path = f"s3://{bucket_name}/{object_name}"

# SQL COPY command to load data from S3 to Redshift
copy_cmd = f"""
COPY {table_name}
FROM '{s3_path}'
ACCESS_KEY_ID '{AWS_redshift_access_key}'
SECRET_ACCESS_KEY '{AWS_redshift_secret_access_key}'
CSV;  -- Assuming the file is in CSV format, modify if necessary
"""


# Execute the COPY command
cursor.execute(copy_cmd)
conn.commit()

# Close the connection
cursor.close()
conn.close()

