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

redshift_endpoint = credentials.get('redshift_endpoint')

redshift_port = credentials.get('redshift_port')

#S3 Bucket Details
bucket_name = bucket_name
object_name = 'your-object-name.csv'

# Save DataFrame to an in-memory buffer
csv_buffer = StringIO()
result_df.to_csv(csv_buffer, index=False)

# Create S3 client
#s3_client = boto3.client('s3', aws_access_key_id=AWS_redshift_access_key, aws_secret_access_key=AWS_redshift_secret_access_key)

# Upload the DataFrame to S3
#s3_client.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key=object_name)


print("completed the s3 upload")


import psycopg2

import redshift_connector
conn = redshift_connector.connect(
     host='final-test.789668808708.us-west-2.redshift-serverless.amazonaws.com',
     database='dev',
     user='admin',
     password=AWS_redshift_admin_pw,
     timeout=5
  )



create_table_sql = f"""
CREATE TABLE IF NOT EXISTS financial_data
(
customer_id BIGINT,
f_name VARCHAR(500),
l_name VARCHAR(500),
product_name VARCHAR(500),
product_type VARCHAR(500),
amt_usd VARCHAR(500),
post_date TIMESTAMP,
channel_desc VARCHAR(500),
partner_desc VARCHAR(500),
location_name VARCHAR(500),
account_name VARCHAR(500),
account_type VARCHAR(500)
);
"""
cursor = conn.cursor()
# Execute the create table command
cursor.execute(create_table_sql)
conn.commit()
table_name = "financial_data"

s3_path = f"s3://{bucket_name}/{object_name}"

# SQL COPY command to load data from S3 to Redshift
copy_cmd = f"""
COPY {table_name}
FROM '{s3_path}'
ACCESS_KEY_ID '{AWS_redshift_access_key}'
SECRET_ACCESS_KEY '{AWS_redshift_secret_access_key}'
IGNOREHEADER 1
CSV;  -- Assuming the file is in CSV format, modify if necessary
"""

print(copy_cmd)

#result_df.to_sql(table_name,conn,index=False,if_exists='append')

# Execute the COPY command
cursor.execute(copy_cmd)


conn.commit()
conn.close()

    
