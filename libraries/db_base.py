from codecs import iterdecode
from copyreg import pickle
from itertools import count
import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp
#from tkinter import S
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandasql as psql
from  libraries.utility import Utility
import pickle
import sympy
from pprint import pprint
import time
import pyodbc
pyodbc. pooling=False
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import mysql.connector as mysqlcon
import re

class db_base(Utility):
    '''
    Simulate some data
    '''
    CONNECTION_STRINGS = None
    CURRENT_DATABASE = None
    QUERIES = None

    def __init__(self,current_database=None,svr_type='mssql',artifact_dir='db_artifacts'):
        super().__init__()
        global CONNECTION_STRINGS
        self.CURRENT_DATABASE = current_database
        
        connection_string_dir = os.path.join(self.get_this_dir(),artifact_dir,svr_type,"connections")

        files_in_directory, file_names_only, file_loc_dict, pandas_dict, file_content_dict = self.load_directory_files(
                        directory=connection_string_dir,
                        file_filter="*.txt",
                        print_files=False,
                        print_file_names_only=False,
                        return_pandas_data_frames=False,
                        skip_list=None,
                        load_data_files_into_strings=True)

        CONNECTION_STRINGS = {}
        for key in file_content_dict.keys():
            CONNECTION_STRINGS[key.replace(".txt","")] = file_content_dict[key]

        if(current_database is not None):
            self.CURRENT_DATABASE = current_database

        global QUERIES
        query_dir = os.path.join(self.get_this_dir(),artifact_dir,svr_type,"queries")
        QUERIES = self.load_subdirs_into_dict(parent_directory=query_dir,filetype="sql",get_content=True)

        self.test_db_connection()

    def test_db_connection(self,current_database=None,sql_text_test="select top 10 * from sysobjects"):
        global CONNECTION_STRINGS
        if current_database is None and self.CURRENT_DATABASE is None:
            print("no database specified")
            return
        if current_database is not None:
            self.CURRENT_DATABASE = current_database

        #return

        #implicit else
        try:
            conn = self.get_connection(current_database=current_database)
            cursor = conn.cursor()
            cursor.execute(sql_text_test)
            print("Database : {}, Connection Good: {}".format(self.CURRENT_DATABASE,True))
            return True
        except Exception as e:
            print(str(e))
            print("Database : {}, Connection Good: {}".format(self.CURRENT_DATABASE,False))
            return False

    def get_connection(self,current_database=None):
        global CONNECTION_STRINGS
        CURRENT_DATABASE = self.CURRENT_DATABASE
        if current_database is None and CURRENT_DATABASE is None:
            print("no database specified")
            return
        if current_database is not None:
            CURRENT_DATABASE = current_database

        str_con = CONNECTION_STRINGS[CURRENT_DATABASE].replace("\n","")            
        return pyodbc.connect(r'{}'.format(str_con))

    def get_connection_string(self,current_database=None):
        global CONNECTION_STRINGS
        CURRENT_DATABASE = self.CURRENT_DATABASE
        if current_database is None and CURRENT_DATABASE is None:
            print("no database specified")
            return
        if current_database is not None:
            CURRENT_DATABASE = current_database

        str_con = CONNECTION_STRINGS[CURRENT_DATABASE].replace("\n","")            
        return r'{}'.format(str_con)


    def run_and_print_all_queries(self,current_database=None):
        global QUERIES
        CURRENT_DATABASE = self.CURRENT_DATABASE

        if current_database is None and CURRENT_DATABASE is None:
            print("no database specified")
            return
        if current_database is not None:
            CURRENT_DATABASE = current_database
        
        my_conn = self.get_connection(CURRENT_DATABASE)

        for items in QUERIES[CURRENT_DATABASE]:
            for key in items.keys():
                if  "content" in key:
                    query = items[key]
                    print("results for : {}".format(key.replace("_content","")))
                    self.run_and_print_raw_results(connection=my_conn,query=query)

    def get_all_queries(self,current_database=None,print_query_names=False):
        global QUERIES
        CURRENT_DATABASE = self.CURRENT_DATABASE

        if current_database is None and CURRENT_DATABASE is None:
            print("no database specified")
            return
        if current_database is not None:
            CURRENT_DATABASE = current_database
        
        my_conn = self.get_connection(CURRENT_DATABASE)

        for items in QUERIES[CURRENT_DATABASE]:
            for key in items.keys():
                if  "content" in key:
                    query = items[key]
                    if print_query_names:
                        print("query_name : {}".format(key.replace(".sql_content","")))
                        #print("query_file : {}".format(items[key.replace("_content","")]))
                    #self.run_and_print_raw_results(connection=my_conn,query=query)


    def print_all_internal_keys(self,current_database=None):
        global QUERIES
        CURRENT_DATABASE = self.CURRENT_DATABASE

        if current_database is None and CURRENT_DATABASE is None:
            print("no database specified")
            return
        if current_database is not None:
            CURRENT_DATABASE = current_database

        for items in QUERIES[CURRENT_DATABASE]:
            for key in items.keys():
                print(key)


    def run_count_query(self,query_key=None,query_text=None,current_database=None):

        global QUERIES
        CURRENT_DATABASE = self.CURRENT_DATABASE

        if current_database is None and CURRENT_DATABASE is None:
            print("no database specified")
            return
        if current_database is not None:
            CURRENT_DATABASE = current_database
        
        my_conn = self.get_connection(CURRENT_DATABASE)

        if query_key is not None:
            for item in QUERIES[CURRENT_DATABASE]:
                sql_query_key = "{}{}".format(query_key,".sql_content")
                if sql_query_key in item.keys():
                    query_text = item[sql_query_key]
    
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query_text)

        for i in cursor:
            return(i[0])



    def run_and_print_raw_results(self, connection=None, query=None):

        cursor = connection.cursor()
        cursor.execute(query)

        for i in cursor:
            print(i)

        
    def run_query_with_multiple_df_return(self,query_key=None,query_text=None,current_database=None):

        global QUERIES
        CURRENT_DATABASE = self.CURRENT_DATABASE

        if current_database is None and CURRENT_DATABASE is None:
            print("no database specified")
            return
        if current_database is not None:
            CURRENT_DATABASE = current_database
        
        my_conn = self.get_connection(CURRENT_DATABASE)

        if query_key is not None:
            for item in QUERIES[CURRENT_DATABASE]:
                sql_query_key = "{}{}".format(query_key,".sql_content")
                if sql_query_key in item.keys():
                    query_text = item[sql_query_key]


        df_list = []

        connection = self.get_connection()
        with connection:
            cursor = connection.cursor()
            rows = cursor.execute(query_text).fetchall()

            columns = [column[0] for column in cursor.description]
            df_list.append(pd.DataFrame.from_records(rows, columns=columns))
            

            while (cursor.nextset()): 
                try:
                    rows = cursor.fetchall()
                    columns = [column[0] for column in cursor.description]
                    df_list.append(pd.DataFrame.from_records(rows, columns=columns))
                except Exception as e:
                    fido=str(e)
        
        
            cursor.close()

        connection.close()

        return df_list

    def get_sql_query_from_query_key(self,query_key=None,current_database=None):

        query_text = ""
        global QUERIES
        CURRENT_DATABASE = self.CURRENT_DATABASE

        if current_database is None and CURRENT_DATABASE is None:
            print("no database specified")
            return
        if current_database is not None:
            CURRENT_DATABASE = current_database
        
        if query_key is not None:
            for item in QUERIES[CURRENT_DATABASE]:
                sql_query_key = "{}{}".format(query_key,".sql_content")
                if sql_query_key in item.keys():
                    query_text = item[sql_query_key] 

        return query_text

               

    def run_query_with_single_df_tokenify(self,query_key=None,query_text=None,current_database=None,token_replacements=dict()):
        sql_query = ""
        if query_key is not None:
            sql_query = self.get_sql_query_from_query_key(query_key=query_key)
        
        file_suffix=self.CURRENT_DATABASE
        for key in token_replacements.keys():
            sql_query = sql_query.replace(key,"{}".format(token_replacements[key]))


        file_name = "{}_{}.sql".format(query_key,file_suffix)
        output_file_name = os.path.join(self.get_this_dir(),"debug_text_output",file_name)
        print(output_file_name)
        self.write_text_to_file(output_file_name,sql_query)

        return self.run_query_with_single_df(query_text=sql_query)

    def run_query_with_single_df(self,query_key=None,query_text=None,current_database=None):
        if query_key is not None:
            return self.run_query_with_multiple_df_return(query_key)[0]
        if query_text is not None:
            return self.run_query_with_multiple_df_return(query_text=query_text)[0]

        return df.DataFrame()

    def get_alchecmy_engine(self):
        connection_url = URL.create(
            "mssql+pyodbc",
            query={"odbc_connect":self.get_connection_string()}
        )
        #print(self.get_connection_string())
        return create_engine(connection_url)

    def push_dataframe_to_sql_server(self,df,target_table,textfile,current_database=None):
        cs = self.get_connection_string()
        engine = self.get_alchecmy_engine()
        df.to_sql(target_table,engine,if_exists="replace",index=False, method='multi')
        bcp_cmd = self.get_bcp_command_from_connection(cs,textfile,target_table)
        print(bcp_cmd)
        os.system(bcp_cmd)
        return ""

    def get_bcp_command_from_connection(self,cs,textfile,tablename,delimiter=",",schema='parsystem'):
        try:
            cs = cs.replace("Driver={ODBC Driver 17 for SQL Server};","")
            cs = cs.replace("Server="," -S ")
            cs = cs.replace("Database="," -d ")
            cs = cs.replace("uid="," -U ")
            cs = cs.replace("pwd="," -P ")
            cs = cs.replace(";"," ")
            tablename = schema + "." + tablename if len(schema)>0 else tablename
            bcp_command = "bcp {} in {} {} -q -c".format(tablename,textfile,cs)
            return(bcp_command)
        except:
            return ""
