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
from psycopg2.extras import execute_values

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

        self.account_type_accounts = {
            "Asset":["Building","Equipment","Vehicles","Machinery","Patent","Cash on Hand","Royalties","Property Rights","Music Catalog","Movie Catalog"],
            "Liability":["Debt","Future Interest Due","Tax Liability","Bad Debt"],
            "Equity":["Internal Shares","External Shares","Goodwill"],
            "Revenue":["Streaming Cash","Sell-Through Income","Distribution Income","Rental Income","Interest Income","Theatrical Income","Music Income"],
            "Expense":["Payroll","Overhead","Capital Expense","TV Royalties","Movie Royalties","Tax Expense","Production Cost"]
        }        

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

    def populate_customer_products(self,count,products_per_customer=3):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:

            p_db = fake_data_to_db("products")
            l_pi = p_db.get_list_from_sql(sql_text="select id from products")
            df_p_types = p_db.run_query_with_single_df(query_key="get_product_id_and_product_type")
            #Fetch the IDs of existing customers from the customer_info table
            cursor.execute("SELECT id FROM customer_info")
            customer_ids = [row[0] for row in cursor.fetchall()]
            for i in range(len(customer_ids)):

                # Simulate normal distribution to select a random customer_id
                customer_id = customer_ids[i]
                
                for i in range(products_per_customer):

                    # Generate other random data
                    product_id = random.choice(l_pi)
                    product_type_desc = df_p_types.loc[df_p_types['product_id'] == product_id, 'product_type_desc'].values[0]
                    
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
                        INSERT INTO customer_product (product_id, customer_id, created_by, purchase_dt, expiration_dt,product_type_desc)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (product_id, customer_id, created_by, purchase_dt, expiration_dt,product_type_desc)
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

        fin_db = db_base("finance","postsql")
        results = fin_db.run_query_with_single_df(query_key="get_population_and_state_from_geo")

        results = results[(results != 0).all(axis=1)]

        # return
        column_name = 'zip_population'
        zip_population = results.columns.get_loc(column_name)
        column_name = 'city_name'
        city_name = results.columns.get_loc(column_name)
        column_name = 'postalcode'
        postalcode = results.columns.get_loc(column_name)
        column_name = 'province'
        province = results.columns.get_loc(column_name)


        # return
        # Calculate total population and distribution
        total_population = sum([int(results.iloc[ind,zip_population]) for ind in range(len(results))])
        customer_distribution = [(results.iloc[ind,city_name],results.iloc[ind,postalcode],results.iloc[ind,province], (int(results.iloc[ind,zip_population]) / total_population) * count) for ind in range(len(results))]



        conn = self.get_connection()
        cursor = conn.cursor()

        # try:
        for city_name, postalcode, province, city_customers in customer_distribution:
            for _ in range(int(city_customers)):

                # Generate random first and last names
                f_name = fake.first_name()
                l_name = fake.last_name()

                # Generate a unique email address for the "irwinanalytics.com" domain
                email_address = f"{f_name.lower()}.{l_name.lower()}@irwinanalytics.com"

                # Generate a random created_dt within the last five years
                today = datetime.now()
                five_years_ago = today - timedelta(days=365 * 5)
                created_dt = fake.date_time_between(start_date=five_years_ago, end_date=today)

                country="USA"
                # Insert the generated data into the database
                cursor.execute(
                    """
                    INSERT INTO customers.customer_info (f_name, l_name, email_address, created_dt,postalcode,city_name,country,province)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (f_name, l_name, email_address, created_dt,postalcode,city_name,country,province)
                )

        conn.commit()
        cursor.close()
        conn.close()

        # except Exception as e:
        #     print(f"Error: {e}")
        # finally:
        #     if conn:
        #         conn.close()


    def populate_fake_postsql_data(self,table_name,count):
        if table_name=="geo_geography":
            self.populate_geo_geography()
        if table_name=="fin_gl_accounts":
            self.populate_fin_gl_accounts(count)
        if table_name=="fin_distro_channel":
            self.populate_fin_distro_channel()            
        if table_name=="fin_distro_channel_group":
            self.populate_fin_distro_channel_group()
        if table_name=="geo_population_by_postalcode":
            self.populate_geo_population_by_postalcode()
        if table_name=="geo_postalcode_to_county_state":
            self.populate_geo_postalcode_to_county_state()
        if table_name=="fin_distro_partner":
            self.populate_fin_distro_partner(count)
        if table_name=="geo_city_population":
            self.populate_geo_city_population()
        if table_name=="fin_account_activity":
            self.populate_fin_account_activity(count)


    def populate_fin_account_activity(self,count=4000):

        df_gl_acct = self.run_query_with_single_df(query_text="select * from fin_gl_accounts")
        df_d_chnl = self.run_query_with_single_df(query_text="select * from fin_distro_channel")
        df_d_part = self.run_query_with_single_df(query_text="select * from fin_distro_partner")
        df_geo    = self.run_query_with_single_df(query_text="select * from geo_geography")

        cust = db_base("customers","mysql")
        df_cust = cust.run_query_with_single_df(query_text="select * from customer_info")
        df_c_prod = cust.run_query_with_single_df(query_text="select * from customer_product")
        df_c_prod_h = cust.run_query_with_single_df(query_text="select * from customer_product_history")
        
        prod = db_base("products","mssql")
        #df_prod = prod.run_query_with_single_df(query_text="select * from products")
        df_prod_price = prod.run_query_with_single_df(query_text="select * from product_price")

        data_to_insert = []

        #customer products inserted
        cpi=set()

        fn = os.path.join(self.get_this_dir(),"temp_data","fin_account_activity.csv")
        self.nukefile(fn)

        #got through customer's historical products
        for i in range(len(df_c_prod_h)):

            #post_date
            l_purchase_dt=df_c_prod_h.columns.get_loc("purchase_dt")
            post_date=df_c_prod_h.iloc[i,l_purchase_dt]


            #product_id
            l_product_id=df_c_prod_h.columns.get_loc("product_id")
            product_id=df_c_prod_h.iloc[i,l_product_id]

            cpi.add(product_id)

            #come back to this with date comparison on the price it was at the time purchased
            #for the time being keep this simple.
            amt_usd=df_prod_price.loc[df_prod_price["product_id"]==product_id,"usd_price"].values[0]

            #customer_id
            l_customer_id=df_c_prod_h.columns.get_loc("customer_id")
            customer_id=df_c_prod_h.iloc[i,l_customer_id]

            #gl_account_id
            gl_account_id=random.choice(df_gl_acct.loc[df_gl_acct['account_type'] == "Revenue", 'id'].values)
            
            #geography_id
            c_postalcode=df_cust.loc[df_cust["id"]==customer_id,"postalcode"].values[0]
            geography_id=df_geo.loc[df_geo["postalcode"]==c_postalcode,"id"].values[0]

            #fin_distro_channel_id
            fin_distro_channel_id=random.choice(df_d_chnl["id"].values)

            #fin_distro_partner_id
            fin_distro_partner_id=random.choice(df_d_part["id"].values)

            line_to_write="{},{},{},{},{},{},{},{}".format(str(post_date),str(product_id),str(customer_id),str(gl_account_id),str(amt_usd),str(geography_id),str(fin_distro_channel_id),str(fin_distro_partner_id))

            self.write_line_to_file(fn,line_to_write)


        #now go through current products
        for i in range(len(df_c_prod)):

            #post_date
            l_purchase_dt=df_c_prod.columns.get_loc("purchase_dt")
            post_date=df_c_prod.iloc[i,l_purchase_dt]

            #product_id
            l_product_id=df_c_prod.columns.get_loc("product_id")
            product_id=df_c_prod.iloc[i,l_product_id]

            cpi.add(product_id)

            #come back to this with date comparison on the price it was at the time purchased
            #for the time being keep this simple.
            amt_usd=str(df_prod_price.loc[df_prod_price["product_id"]==product_id,"usd_price"].values[0])

            #customer_id
            l_customer_id=df_c_prod.columns.get_loc("customer_id")
            customer_id=df_c_prod.iloc[i,l_customer_id]

            #gl_account_id
            gl_account_id=random.choice(df_gl_acct.loc[df_gl_acct['account_type'] == "Revenue", 'id'].values)
            
            #geography_id
            c_postalcode=df_cust.loc[df_cust["id"]==customer_id,"postalcode"].values[0]
            geography_id=df_geo.loc[df_geo["postalcode"]==c_postalcode,"id"].values[0]

            #fin_distro_channel_id
            fin_distro_channel_id=random.choice(df_d_chnl["id"].values)

            #fin_distro_partner_id
            fin_distro_partner_id=random.choice(df_d_part["id"].values)

            line_to_write="{},{},{},{},{},{},{},{}".format(str(post_date),str(product_id),str(customer_id),str(gl_account_id),str(amt_usd),str(geography_id),str(fin_distro_channel_id),str(fin_distro_partner_id))

            self.write_line_to_file(fn,line_to_write)


        #line_to_write="{},{},{},{},{},{},{},{}".format(str(post_date),str(product_id),str(customer_id),str(gl_account_id),str(amt_usd),str(geography_id),str(fin_distro_channel_id),str(fin_distro_partner_id))

        # Connect to the database
        connection = self.get_connection()

        # Create a cursor
        cursor = connection.cursor()

        # Use the COPY command to load data from the CSV file into the table
        copy_sql = f"""
                COPY fin_account_activity(post_date,product_id,customer_id,account_id,amt_usd,geo_geography_id,fin_distro_channel_id,fin_distro_partner_id) 
                FROM stdin 
                DELIMITER as ','
                """
        with open(fn, 'r') as file:
            cursor.copy_expert(sql=copy_sql, file=file)
            cursor.close()
            connection.commit()

        # Close the database connection
        connection.close()        


    def populate_geo_city_population(self):
        self.run_update_from_cli_connector("populate_geo_city_population")



    def populate_fin_distro_partner(self,count=1000):
        connection = self.get_connection()
        cursor = connection.cursor()

        generated_partner_desc = set()
        while len(generated_partner_desc)<count:
            company_name = fake.company()
            if company_name not in generated_partner_desc:
                generated_partner_desc.add(company_name)

        for partner_desc in generated_partner_desc:
            created_by = fake.name()
            updated_by = fake.name()
            
            cursor.execute(
                "INSERT INTO fin_distro_partner (partner_desc, created_by, updated_by) VALUES (%s, %s, %s)",
                (partner_desc, created_by, updated_by)
            )

        connection.commit()
        cursor.close()


    def populate_geo_postalcode_to_county_state(self):
        file_path = os.path.join(self.get_this_dir(),"data","geography","postal_to_county_state.csv")
        # Table name in PostgreSQL
        table_name = 'public.geo_postalcode_to_county_state'

        # Connect to the database
        connection = self.get_connection()

        # Create a cursor
        cursor = connection.cursor()

        # Use the COPY command to load data from the CSV file into the table
        copy_sql = f"""
                COPY {table_name}
                FROM stdin WITH CSV HEADER
                DELIMITER as ','
                """
        with open(file_path, 'r') as file:
            cursor.copy_expert(sql=copy_sql, file=file)
            cursor.close()
            connection.commit()

        # Close the database connection
        connection.close()        


    def populate_geo_population_by_postalcode(self):
        file_path = os.path.join(self.get_this_dir(),"data","geography","cleaned_pop.csv")
        # Table name in PostgreSQL
        table_name = 'public.geo_population_by_postalcode'

        # Connect to the database
        connection = self.get_connection()

        # Create a cursor
        cursor = connection.cursor()

        # Use the COPY command to load data from the CSV file into the table
        copy_sql = f"""
                COPY {table_name}
                FROM stdin WITH CSV HEADER
                DELIMITER as ','
                """
        with open(file_path, 'r') as file:
            cursor.copy_expert(sql=copy_sql, file=file)
            cursor.close()
            connection.commit()

        # Close the database connection
        connection.close()        

    
    def populate_fin_distro_channel_group(self):
        self.run_update_from_cli_connector("populate_fin_distro_channel_group")

    def populate_fin_distro_channel(self):
        self.run_update_from_cli_connector("populate_fin_distro_channel")


    def populate_fin_gl_accounts(self,count):

        l_keys=[key for key in self.account_type_accounts.keys()]
        fake = Faker()
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            for _ in range(count):

                # Generate random account name and account code
                account_code = fake.unique.random_number(digits=6, fix_len=True)
                account_type = random.choice(l_keys)

                account_name = random.choice(self.account_type_accounts[account_type]) + " " + account_type + " " + str(account_code)
                
                # Generate other random account data
                #account_balance = round(random.uniform(10000000, 10000000), 2)
                created_by = fake.name()
                updated_by = fake.name()
                
                # Insert the generated data into the database
                cursor.execute(
                    """
                    INSERT INTO fin_gl_accounts (account_code, account_name, account_type, created_by)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (account_code, account_name, account_type,created_by)
                )

            conn.commit()
            cursor.close()
        except Exception as e:
            print(str(e))
            conn.close()

    def populate_geo_geography(self):
        df = self.read_geo_file()
        # Create a cursor to execute SQL queries
        con = self.get_connection()
        cursor = con.cursor()

        # Loop through the rows of the dataframe and insert data into the SQL table
        for index, row in df.iterrows():
            cursor.execute(
                """
                INSERT INTO geo_geography (postalcode, country, location_name, msa)
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
            created_dt = self.create_random_date(starting_years_ago=5,ending_years_ago=3)

            # SQL query to insert data
            sql_query = """
            INSERT INTO products (product_name, product_type_id, created_dt)
            VALUES (?, ?, ?)
            """

            cursor.execute(sql_query, (product_name, product_type,created_dt))

            # Commit the changes
            conn.commit()



    def populate_product_types(self):

        conn = self.get_connection()
        cursor = conn.cursor()

        product_types = ["Movie", "Subscription", "Game", "Single View Movie", "Bundle", "TV Series", "TV Season", "TV Episode", "Event","Download","Pay TV"]

        for product_type in product_types:
            # SQL query to insert data
            sql_query = """
            INSERT INTO product_type (product_type_desc)
            VALUES (?)
            """

            cursor.execute(sql_query, (product_type,))

        # Commit the changes
        conn.commit()

