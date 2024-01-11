import pandas as pd
from libraries.utility import Utility as mutil
from libraries.db_base import db_base
import os
import time

from libraries.utility import Utility as mutil
from libraries.db_base import db_base
from libraries.db_ins_fake_data import fake_data_to_db
from libraries.custom_excel_output import custom_excel_output
import pandas as pd
import pandasql as psql
pd.options.display.max_columns = None
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
import warnings
import time
import os
import pandasql as psql
from IPython.core.display import Markdown as md
warnings.filterwarnings('ignore')

from IPython.core.display import display, HTML, Markdown, Latex
display(HTML(
    '<style>'
        '#notebook { padding-top:0px !important; } ' 
        '.container { width:100% !important; } '
        '.end_space { min-height:0px !important; } '
        '.end_space { min-height:0px !important; } '
        '.prompt {width: 0px; min-width: 0px; visibility: collapse } '
        '.parent{'
        '    display: grid;'
        '    grid-template-columns: 1fr 1fr;'
        '    column-gap: 5px;'
        '}    '
    '</style>'
))


from pyspark.sql import SparkSession




u = mutil()

bq_credential_file = os.path.join(u.get_this_dir(),"dbs","servers","bigquery","bigquery1","tokens","bigquery-token.json")

    #Location of database drivers
    #postgres
    #/usr/share/java/postgresql.jar
    #mysql
    #/usr/share/java/mysql-connector-j-8.2.0.jar
    #mssql
    #/usr/share/java/sqljdbc_12.4/enu/jars/mssql-jdbc-12.4.2.jre11.jar

def create_spark_sesssion():
    # Create SparkSession
    spark = SparkSession.builder \
        .appName("MasterSession") \
        .config("spark.jars", "/usr/share/java/sqljdbc_12.4/enu/jars/mssql-jdbc-12.4.2.jre11.jar") \
        .config("spark.jars", "/usr/share/java/postgresql.jar") \
        .config("spark.jars", "/usr/share/java/mysql-connector-j-8.2.0.jar") \
        .config('spark.jars.packages', 'com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.21.1') \
        .config('spark.jars', 'https://storage.googleapis.com/spark-lib/bigquery/spark-bigquery-latest_2.12.jar') \
        .config("credentialsFile", bq_credential_file) \
        .config("parentProject", "brave-sonar-367918") \
        .getOrCreate()
    return spark

def use_sql_server_connection(query,spark):
    

    # Start the timer
    start_time = time.time()
    


    # Database connection properties
    database_url = "jdbc:sqlserver://mssql1:1433;databaseName=products"
    database_properties = {
        "user": "sa",
        "password": "Python2028",
        "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        "encrypt": "true",
        "trustServerCertificate": "true"  # Add this line        
    }

    # Read data from MSSQL
    #df = spark.read.jdbc(url=database_url, table="products", properties=database_properties)

    # Read data from MSSQL
    df = spark.read.jdbc(url=database_url, table=query, properties=database_properties)

    # Show the data
    #df.show()
    
    # Stop the timer and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert elapsed time to minutes and seconds
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"Time elapsed: {minutes} minutes and {seconds} seconds")
    return df


def use_postgress_sql(query,spark):
  

    # Start the timer
    start_time = time.time()
    

    # Database connection properties
    database_url = "jdbc:postgresql://postsql1:5432/finance"
    database_properties = {
        "user": "postgres",
        "password": "Python2028",
        "driver": "org.postgresql.Driver",
        "encrypt": "true",
        "trustServerCertificate": "true"  # Add this line        
    }
    
    # Read data from MSSQL
    df = spark.read.jdbc(url=database_url, table=query, properties=database_properties)

    # Show the data
    #df.show()
    
    # Stop the timer and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert elapsed time to minutes and seconds
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"Time elapsed: {minutes} minutes and {seconds} seconds")
    return df

def use_mysql_server(query,spark):
    
    # Start the timer
    start_time = time.time()
    

    # Database connection properties
    database_url = "jdbc:mysql://mysql1:3306/customers"
    database_properties = {
        "user": "root",
        "password": "Python2028",
        "driver": "com.mysql.cj.jdbc.Driver",
        "encrypt": "true",
        "trustServerCertificate": "true"  # Add this line        
    }
    
    # Read data from MSSQL
    df = spark.read.jdbc(url=database_url, table=query, properties=database_properties)
    
    # Stop the timer and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert elapsed time to minutes and seconds
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"Time elapsed: {minutes} minutes and {seconds} seconds")
    
    return df
    




#Now that all the functions are set up
#bring the actual work

u = mutil()
# Start the timer
start_time = time.time()

# Initialize a SparkSession
spark = create_spark_sesssion()

#instantiate product db instance,
#extract the get_product_info query
dbprod = db_base("products")
get_product_info_sql=dbprod.get_sql_query_from_query_key("get_product_info")

#wrap it in sparksql speak. -- Then execute the query.
query= "(" + get_product_info_sql + ") AS query_table"
prod_info=use_sql_server_connection(query=query,spark=spark)

#instantiate the finance database
#get the account activity query.
dbfin = db_base("finance",svr_type='postsql')
get_account_activity = dbfin.get_sql_query_from_query_key("get_account_activity")

#prep and execute against pyspark.
query= "(" + get_account_activity + ") AS query_table"
fin_account_activity=use_postgress_sql(query,spark)

#customer product history.
dbcust = db_base("customers",svr_type='mysql')
query = dbcust.get_sql_query_from_query_key("get_customer_product_history1")

#prep and execute against pyspark.
query = "(" + query + ") AS query_table"
cust_products = use_mysql_server(query,spark)



# Now that the extraction is complete. ...
# Register DataFrames as temporary views
cust_products.createOrReplaceTempView("cust_products")
prod_info.createOrReplaceTempView("prod_info")
fin_account_activity.createOrReplaceTempView("fin_account_activity")


#Now we can join all of these disparate sources together with SQL. ...
# SQL query
sql_query = '''
SELECT
    DISTINCT
    cp.id AS customer_id,
    cp.f_name,
    cp.l_name,
    p.product_name,
    p.product_type,
    fa.amt_usd,
    fa.post_date,
    fa.channel_desc,
    fa.partner_desc,
    fa.location_name,
    fa.account_name,
    fa.account_type
FROM cust_products cp
JOIN prod_info p ON p.id = cp.product_id
JOIN fin_account_activity fa ON fa.customer_id = cp.id AND fa.product_id = cp.product_id
'''

# Execute SQL query
result_rdd = spark.sql(sql_query)


#make a copy of the RDD into a pands DF
result_df = result_rdd.toPandas()
#result_df_bq = result_rdd.toDF()



#Write the stuff to my bigquery database.
result_rdd.write \
  .format("bigquery") \
  .option("project", "brave-sonar-367918") \
  .option("table", "site_traffic.financial_data") \
  .option("writeMethod", "direct") \
  .mode("append") \
  .save()


#Now push things into redshift
#To-do solve the issue of doing it within pyspark.

from libraries.utility import Utility as mutil
import boto3 
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
s3_client = boto3.client('s3', aws_access_key_id=AWS_redshift_access_key, aws_secret_access_key=AWS_redshift_secret_access_key)

# Upload the DataFrame to S3
s3_client.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key=object_name)

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
CREATE TABLE IF NOT EXISTS customer_financial_data
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


table_name = "customer_financial_data"

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

# Execute the COPY command
cursor.execute(copy_cmd)


conn.commit()
conn.close()
    



# Stop the SparkSession when done
spark.stop()


# Stop the timer and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time

# Convert elapsed time to minutes and seconds
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

print(f"Overall Time: {minutes} minutes and {seconds} seconds")


# Show the results
result_df.head()

dbcust = custom_excel_output(current_database="customers",svr_type='mysql')        

#Create an excel -- everyone loved excel.
file_name = os.path.join(dbcust.get_this_dir(),"project_data","tempdir","customer_account_activity.xlsx")

result_df["amt_usd"] = result_df["amt_usd"].replace('[\$,]', '', regex=True).astype(float)

l_dfs = []
l_dfs.append(result_df)
dbcust.write_excel_from_dfs(list_of_dfs=l_dfs,file_name=file_name,add_subtotal_on_top=True)

href_tag = dbcust.get_embedded_href_tag_from_image_file(file_name)
dbcust.nukefile(file_name)
display(HTML(href_tag))
shuffled_df = result_df.sample(frac=1)
display(shuffled_df.head(5).style.set_properties(**{'text-align': 'left'}).set_table_styles([dict(selector = 'th', props=[('text-align', 'left')])]))



