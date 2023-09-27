from libraries.utility import Utility as Util
from libraries.db_base import db_base
import os
import subprocess
import argparse
from libraries.db_ins_fake_data import fake_data_to_db
import importlib.util
from pydantic_sqlalchemy import sqlalchemy_to_pydantic


mu=Util()

def get_sql_server_key(d,parent_key='',target_key=''):
    for key, value in d.items():
        new_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value,dict):
            if 'mssql' in parent_key:
                print(new_key)
                return new_key
            else:
                get_sql_server_key(value,new_key)

def create_sql_db(servername,server_objects,server_type="mssql"):
    for db in server_objects["dbs"]:
        print(db)
        #get myconnector
        cntr_path=os.path.join(mu.get_this_dir(),"cnctr",server_type,"{}.{}".format(servername,"sh"))
        if not os.path.exists(cntr_path):
            print("*"*30)
            print("File does not exist:")
            print(cntr_path)
            print("*"*30)
            return
        db_connector=mu.get_data_from_file(cntr_path).replace("\n","").replace("\r","")

        #get create cmd
        create_cmd_file=server_objects["dbs"][db]["create_db"]["create_db.sql"]
        input_pipe=None
        if "mssql" in server_type:
            input_pipe="-i"
        if "mysql" in server_type:
            input_pipe="<"
        if "postsql" in server_type:
            input_pipe="-f"

        
        cmd="{} {} {}".format(db_connector,input_pipe,create_cmd_file)
        print(cmd)
        subprocess.run(cmd,shell=True)

        #create all tables
        for schema in server_objects["dbs"][db]["schemas"]:
            for table in server_objects["dbs"][db]["schemas"][schema]["tables"]:
                tf = server_objects["dbs"][db]["schemas"][schema]["tables"][table]
                if "_content" not in table:
                    cmd="{} {} {}".format(db_connector,input_pipe,tf)
                    print(cmd)
                    subprocess.run(cmd,shell=True)



def setup_sql_server_dbs(server,server_type):
    for servername in server:
        create_sql_db(servername,server[servername],server_type)


def setup_dbs():
    dbs_d = os.path.join(mu.get_this_dir(),"dbs")
    m_dict = mu.get_subdirectories_dict(dbs_d,filetype=".sql")
    setup_sql_server_dbs(m_dict["servers"]["mssql"],"mssql")
    setup_sql_server_dbs(m_dict["servers"]["mysql"],"mysql")
    setup_sql_server_dbs(m_dict["servers"]["postsql"],"postsql")

def test_database():
    products = db_base("customers")

def print_title(title):
    print("*"*40)
    print(title)
    print("*"*40)

def populate_dbs():

    fdi = fake_data_to_db("products",svr_type='mssql')
    print_title("product_type")
    fdi.populate_fake_data(table_name='product_type',count=0)
    print_title("products")
    fdi.populate_fake_data(table_name='products',count=500)
    print_title("product_price")
    fdi.populate_fake_data(table_name='product_price',count=1000)
    print_title("product_price_history")
    fdi.populate_fake_data(table_name='product_price_history',count=1000)

    
    finance = fake_data_to_db("finance",svr_type='postsql')
    print_title("geo_geography")
    finance.populate_fake_data(table_name='geo_geography',count=800)
    print_title("fin_gl_accounts")
    finance.populate_fake_data(table_name='fin_gl_accounts',count=800)
    print_title("fin_distro_channel")
    finance.populate_fake_data(table_name='fin_distro_channel',count=800)
    print_title("fin_distro_channel_group")
    finance.populate_fake_data(table_name='fin_distro_channel_group',count=800)
    print_title("geo_postalcode_to_county_state")
    finance.populate_fake_data(table_name='geo_postalcode_to_county_state',count=800)
    print_title("geo_population_by_postalcode")
    finance.populate_fake_data(table_name='geo_population_by_postalcode',count=800)
    print_title("fin_distro_partner")
    finance.populate_fake_data(table_name='fin_distro_partner',count=800)
    print_title("geo_city_population")
    finance.populate_fake_data(table_name='geo_city_population',count=800)

    ci = fake_data_to_db("customers",svr_type='mysql')
    print_title("customer_info")
    ci.populate_fake_data(table_name="customer_info",count=13000)
    print_title("customer_product")
    ci.populate_fake_data(table_name="customer_product",count=5000)
    print_title("customer_product_history")
    ci.populate_fake_data(table_name="customer_product_history")

    print_title("fin_account_activity")
    finance = fake_data_to_db("finance",svr_type='postsql')
    finance.populate_fake_data(table_name='fin_account_activity',count=800)

import re

def create_model_files(inputfile,outputdirectory):
    print("got in here")
    # Split the input code into sections based on class definitions

    mu.nukepath(outputdirectory)

    # Read the content of the input file
    with open(inputfile, "r") as f:
        code_lines = f.readlines()

    # Initialize variables to track class definitions
    class_started = False
    class_lines = []
    class_files = []

    # Iterate through the lines in the input code
    for line in code_lines:
        # Check if a new class definition is encountered
        if line.strip().startswith("class "):
            # If a class has already started, save it to a separate file
            if class_started:
                class_content = "".join(class_lines)
                class_files.append(class_content)
                class_lines = []

            # Start tracking a new class
            class_started = True

        # Append the line to the current class
        class_lines.append(line)

    # Save each class to a separate file
    for i, class_content in enumerate(class_files):
        # Create a new filename based on the class name
        class_name = class_content.split("class ")[1].split("(")[0].strip()
        output_file = f"{class_name}.py"

        if i>0:
        # Add the first 8 lines to the beginning of each file
            class_content = "".join(code_lines[:8]) + class_content

        of = os.path.join(outputdirectory,output_file)
        mu.write_text_to_file(of,class_content)

        print(f"Created {output_file} ({i+1}/{len(class_files)})")

    print("Splitting complete.")

def create_pydantic_models(MODELS_DIR):

    # Dynamically import all SQLAlchemy models in the specified directory
    models = []
    for model_file in os.listdir(MODELS_DIR):
        if model_file.endswith(".py"):
            module_name = os.path.splitext(model_file)[0]
            module_path = os.path.join(MODELS_DIR, model_file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            models.extend([cls for cls in module.__dict__.values() if isinstance(cls, type)])

    # Generate Pydantic models from the discovered SQLAlchemy models
    for model in models:
        if hasattr(model, "__table__"):  # Check if it's an SQLAlchemy model
            pydantic_model = sqlalchemy_to_pydantic(model, exclude=["id"])
            pydantic_model_code = pydantic_model.schema_json(indent=2)
            print(pydantic_model_code)



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--Action", help = "Action to Perform")
    parser.add_argument("-i", "--inputfile", help = "Input File")
    parser.add_argument("-o", "--outfile", help = "Out File")

    args = parser.parse_args()
    print(args)

    if args.Action:
        print("Action is : {}".format(args.Action))
        if args.Action.lower() == "setup_dbs":
            setup_dbs()
            return
        if args.Action.lower() == "testdb":
            test_database()
        if args.Action.lower() == "populate_dbs":
            populate_dbs()
            return
        if args.Action.lower() == "create_model_files":
            if args.inputfile and args.outfile:
                create_model_files(args.inputfile,args.outfile)
        if args.Action.lower() == "create_pydantic_models":
            if args.inputfile:
                create_pydantic_models(args.inputfile)
            return




main()
