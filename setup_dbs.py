from libraries.utility import Utility as Util
from libraries.db_base import db_base
import os
import subprocess
import argparse
from libraries.db_ins_fake_data import fake_data_to_db

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

def populate_dbs():
    fdi = fake_data_to_db("products",svr_type='mssql')
    fdi.populate_fake_data(table_name='product_type',count=0)
    fdi.populate_fake_data(table_name='products',count=1000)
    fdi.populate_fake_data(table_name='product_price',count=1000)
    fdi.populate_fake_data(table_name='product_price_history',count=1000)
    finance = fake_data_to_db("finance",svr_type='postsql')
    finance.populate_fake_data(table_name='geography',count=800)
    finance.populate_fake_data(table_name='gl_accounts',count=800)
    finance.populate_fake_data(table_name='distro_channel',count=800)
    finance.populate_fake_data(table_name='distro_channel_group',count=800)
    ci = fake_data_to_db("customers",svr_type='mysql')
    ci.populate_fake_data(table_name="customer_info",count=3000)
    ci.populate_fake_data(table_name="customer_product",count=30000)
    ci = fake_data_to_db("customers",svr_type='mysql')
    ci.populate_fake_data(table_name="customer_product_history")




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--Action", help = "Action to Perform")

    args = parser.parse_args()
    print(args)

    if args.Action:
        print("Action is : {}".format(args.Action))
        if args.Action.lower() == "setup_dbs":
            setup_dbs()
        if args.Action.lower() == "testdb":
            test_database()
        if args.Action.lower() == "populate_dbs":
            populate_dbs()


main()
