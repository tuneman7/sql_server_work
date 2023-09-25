from libraries.utility import Utility as mutil
from libraries.db_base import db_base
from faker import Faker
import mysql.connector
import random
from datetime import datetime
from datetime import timedelta
import pandas as pd
import os
import numpy as np

# Create an instance of the Faker generator
fake = Faker()

# Define custom provider for generating unique names
class MovieGameTV_NameProvider:
    def __init__(self, faker):
        self.fake = faker
        self.used_names = set()
        self.verb_descriptors = [
            "Wild Ride", "Date With Destiny", "Amazing Race",
            "Crazy Comedy", "Big Romance", "Date in the City",
            "Trip in the Wild", "Spy Thriller", "Monster Madness", "Great War","Patriotic Duty"
        ]

    def unique_movie_game_tv_name(self):
        while True:
            # Generate a random name
            name = fake.first_name()
            
            # Append "'s" to the name
            name += "'s"
            
            # Append a random verb descriptor
            name += " " + random.choice(self.verb_descriptors)
            
            # Ensure the generated name is unique
            if name not in self.used_names:
                self.used_names.add(name)
                return name

class fake_data_to_db(db_base):
    def __init__(self,current_database=None,svr_type='mssql',artifact_dir='db_artifacts'):
        super().__init__(current_database=current_database,svr_type=svr_type,artifact_dir=artifact_dir)

    def populate_fake_data(self,table_name,count=500):
        if self.SERVERTYPE=="mysql":
            return self.populate_fake_mysql_data(table_name=table_name,count=count)
        if self.SERVERTYPE=="mssql":
            return self.populate_fake_mssql_data(table_name,count)
        if self.SERVERTYPE=="postsql":
            return self.populate_fake_postsql_data(table_name,count)

    def populate_fake_mysql_data(self,table_name,count):
        if table_name=="customer_info":
            return self.populate_customer_info_table(count)
        if table_name=="customer_product":
            return self.populate_customer_products(count)
        if table_name=="customer_product_history":
            return self.populate_customer_product_history()
        
    def populate_customer_product_history(self):
        #the adapter has difficulty running complex sql updates
        #pipe the update file into the cli
        self.run_update_from_cli_connector("populate_customer_product_history")

    def populate_customer_products(self,count):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            p_db = fake_data_to_db("products")
            l_pi = p_db.get_list_from_sql(sql_text="select id from products")
            df_p_types = p_db.run_query_with_single_df(query_key="get_product_id_and_product_type")
            print(df_p_types.head())
            # Fetch the IDs of existing customers from the customer_info table
            cursor.execute("SELECT id FROM customer_info")
            customer_ids = [row[0] for row in cursor.fetchall()]

            for _ in range(count):
                # Simulate normal distribution to select a random customer_id
                customer_id = int(np.random.normal(loc=np.mean(customer_ids), scale=np.std(customer_ids)))

                # Ensure the selected customer_id is within the range of available IDs
                customer_id = max(min(customer_id, max(customer_ids)), min(customer_ids))

                # Generate other random data
                product_id = random.choice(l_pi)
                product_type = df_p_types.loc[df_p_types['product_id'] == product_id, 'product_type'].values[0]
                
                #product_type = fake.word()
                created_by = fake.name()
                # Generate purchase_dt in a range between two days and one year ago
                purchase_dt = fake.date_time_between(start_date="-1y-2d", end_date="-2d")

                end_date=purchase_dt + timedelta(days=random.choice([1, 30, 90, 365]))
                # Generate expiration_dt as one day, one month, three months, or one year after purchase_dt
                expiration_dt = fake.date_time_between_dates(purchase_dt,end_date)

                # Insert the generated data into the database
                cursor.execute(
                    """
                    INSERT INTO customer_product (product_id, customer_id, created_by, purchase_dt, expiration_dt,product_type)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (product_id, customer_id, created_by, purchase_dt, expiration_dt,product_type)
                )

            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()        
        
    def populate_customer_info_table(self,count):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:

            for _ in range(count):
                # Generate random first and last names
                f_name = fake.first_name()
                l_name = fake.last_name()

                # Generate a unique email address for the "irwinanalytics.com" domain
                email_address = f"{f_name.lower()}.{l_name.lower()}@irwinanalytics.com"

                # Generate a random created_dt within the last five years
                today = datetime.now()
                five_years_ago = today - timedelta(days=365 * 5)
                created_dt = fake.date_time_between(start_date=five_years_ago, end_date=today)

                # Insert the generated data into the database
                cursor.execute(
                    """
                    INSERT INTO customer_info (f_name, l_name, email_address, created_dt)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (f_name, l_name, email_address, created_dt)
                )

            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if conn:
                conn.close()


    def populate_fake_postsql_data(self,table_name,count):
        if table_name=="geography":
            self.populate_geography()
        if table_name=="gl_accounts":
            self.populate_gl_accounts(count)
        if table_name=="account_activity":
            self.populate_account_activity(count)
        if table_name=="distro_channel":
            self.populate_distro_channel()            
        if table_name=="distro_channel_group":
            self.populate_distro_channel_group()             
    
    def populate_distro_channel_group(self):
        self.run_update_from_cli_connector("populate_distro_channel_group")

    def populate_distro_channel(self):
        self.run_update_from_cli_connector("populate_distro_channel")

    def populate_account_activity(self,count):
        this_obj = fake_data_to_db("products")
        p_list = this_obj.get_list_from_sql()


    def populate_gl_accounts(self,count):
        names = ["Streaming","Production","Overhead","Capital","Theatrical","Marketing","Promotion","Sales","Printing","Music","Sound Track","Distribution"]
        fake = Faker()
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            for _ in range(count):

                # Generate random account name and account code
                account_code = fake.unique.random_number(digits=6, fix_len=True)
                account_type = random.choice(["Asset", "Liability", "Equity", "Revenue", "Expense"])

                account_name = random.choice(names) + " " + account_type + " " + str(account_code)
                
                # Generate other random account data
                #account_balance = round(random.uniform(10000000, 10000000), 2)
                created_by = fake.name()
                updated_by = fake.name()
                
                # Insert the generated data into the database
                cursor.execute(
                    """
                    INSERT INTO gl_accounts (account_code, account_name, account_type, created_by)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (account_code, account_name, account_type,created_by)
                )

            conn.commit()
            cursor.close()
        except Exception as e:
            print(str(e))
            conn.close()

    def populate_geography(self):
        df = self.read_geo_file()
        # Create a cursor to execute SQL queries
        con = self.get_connection()
        cursor = con.cursor()

        # Loop through the rows of the dataframe and insert data into the SQL table
        for index, row in df.iterrows():
            cursor.execute(
                """
                INSERT INTO geography (zipcode, country, location_name, msa)
                VALUES (%s, %s, %s, %s)
                """,
                (row["postal_code"], row["country_code"], row["place_name"], row["admin_name3"])
            )

        # Commit the changes to the database
        con.commit()

        # Close the cursor and the connection
        cursor.close()
        con.close()


    def read_geo_file(self):
        file_path = os.path.join(self.get_this_dir(),"data","geography","US.txt")

        column_headers = [
            "country_code",
            "postal_code",
            "place_name",
            "admin_name1",
            "admin_code1",
            "admin_name2",
            "admin_code2",
            "admin_name3",
            "admin_code3",
            "latitude",
            "longitude",
            "accuracy"
        ]

        try:
            # Read the tab-delimited text file into a dataframe
            df = pd.read_csv(file_path, sep='\t', encoding='utf8', header=None, names=column_headers)

            # Optionally, you can perform additional data cleaning or processing here

            return df

        except Exception as e:
            print(f"Error reading the data: {e}")
            return None


    def populate_fake_mssql_data(self,table_name,count):
        if table_name=="product_type":
            self.populate_product_types()
        if table_name=="products":
            self.populate_products(count)
        if table_name=="product_price":
            self.populate_product_price()
        if table_name=="product_price_history":
            self.populate_product_price_history()

    def populate_product_price_history(self):
        self.run_update_query("populate_product_price_history")
    
    def populate_product_price(self):
        l_pids = self.get_list_from_sql("select id from products")
        conn = self.get_connection()
        cursor = conn.cursor()
        #For all products populate product_price
        for i in range(len(l_pids)):  
            product_id = l_pids[i] 
            usd_price = round(random.uniform(2.99, 34.99), 2)
            pricing_start_dt = datetime.now() - timedelta(days=random.randint(1, 365))
            pricing_end_dt = pricing_start_dt + timedelta(days=365)

            # SQL query to insert data
            sql_query = """
            INSERT INTO product_price (product_id, usd_price, pricing_start_dt, pricing_end_dt)
            VALUES (?, ?, ?, ?)
            """

            cursor.execute(sql_query, (product_id, usd_price, pricing_start_dt, pricing_end_dt))

            # Commit the changes
        conn.commit()


    def get_list_from_sql(self,sql_text="SELECT id FROM product_type"):
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql_text)

        id_list = [row[0] for row in cursor.fetchall()]
        return id_list

    def populate_products(self,count):
        id_list = self.get_list_from_sql()
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fake = Faker()
        fake_pn = Faker()
        fake_pn.add_provider(MovieGameTV_NameProvider)
        product_names = [fake_pn.unique_movie_game_tv_name() for _ in range(count)]

        for i in range(count):  
            product_name = product_names[i]
            created_by = fake.first_name()
            product_type =random.choice(id_list)
            created_dt = fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)

            # SQL query to insert data
            sql_query = """
            INSERT INTO products (product_name, product_type, created_by)
            VALUES (?, ?, ?)
            """

            cursor.execute(sql_query, (product_name, product_type,created_dt))

            # Commit the changes
            conn.commit()



    def populate_product_types(self):

        conn = self.get_connection()
        cursor = conn.cursor()

        product_types = ["Movie", "Subscription", "Game", "Single View Movie", "Bundle", "TV Series", "TV Season", "TV Episode", "Event"]

        for product_type in product_types:
            # SQL query to insert data
            sql_query = """
            INSERT INTO product_type (product_type)
            VALUES (?)
            """

            cursor.execute(sql_query, (product_type,))

        # Commit the changes
        conn.commit()

