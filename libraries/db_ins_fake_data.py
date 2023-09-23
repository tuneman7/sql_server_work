from libraries.utility import Utility as mutil
from libraries.db_base import db_base
from faker import Faker
import mysql.connector
import random
from datetime import datetime
from datetime import timedelta

# Create an instance of the Faker generator
fake = Faker()

# Define custom provider for generating unique names
class CustomNameProvider:
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

    def populate_fake_data(self,table_name,count):
        if self.SERVERTYPE=="mysql":
            return self.populate_fake_mysql_data(table_name=table_name,count=count)
        if self.SERVERTYPE=="mssql":
            return self.populate_fake_mssql_data(table_name,count)
        
    def populate_fake_mssql_data(self,table_name,count):
        if table_name=="product_type":
            self.populate_product_types()
        if table_name=="products":
            self.populate_products(count)
        if table_name=="product_price":
            self.populate_product_price()
    
    def populate_product_price(self):
        l_pids = self.get_list_from_sql()
        conn = self.get_connection()
        cursor = conn.cursor()
        for i in range(len(l_pids)):  # Insert 1000 rows as an example
            product_id = l_pids[i]  # Replace with your product ID logic
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
        id_list = []
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql_text)

        for row in cursor.fetchall():
            id_list.append(row[0])

        return id_list

    def populate_products(self,count):
        id_list = self.get_list_from_sql()
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fake = Faker()
        fake_pn = Faker()
        fake_pn.add_provider(CustomNameProvider)
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


    def populate_fake_mysql_data(self,table_name,count):
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        table_schema = cursor.fetchall()
        fake = Faker()

        # SQL query to insert data
        insert_query = f"INSERT INTO {table_name} ("
        insert_query += ", ".join(column[0] for column in table_schema)  # Column names
        insert_query += ") VALUES ("
        insert_query += ", ".join("%s" for _ in table_schema)  # Placeholders

        for col in table_schema:
            print(str(col[1]).replace('b','').replace("'",""))

        for _ in range(count):
            data_to_insert = [fake.random_element() if str(col[1]).replace('b','').replace("'","").startswith("enum") else fake.format(str(col[1]).replace('b','').replace("'","")) for col in table_schema]
            cursor.execute(insert_query, data_to_insert)

        # Commit the changes
        conn.commit()
        conn.close()

