from libraries.utility import Utility as Util
import os

def get_sql_server_key(d,parent_key='',target_key=''):
    for key, value in d.items():
        new_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value,dict):
            if 'mssql' in parent_key:
                print(new_key)
                return new_key
            else:
                get_sql_server_key(value,new_key)

def create_sql_db(servername,db_objects):
    for db in db_objects["dbs"]:
        print(db)

def setup_sql_server_dbs(server):
    for servername in server:
        create_sql_db(servername,server[servername])

def main():
    mu = Util()
    dbs_d = os.path.join(mu.get_this_dir(),"dbs")
    m_dict = mu.get_subdirectories_dict(dbs_d,filetype=".sql")
    setup_sql_server_dbs(m_dict["servers"]["mssql"])





main()
