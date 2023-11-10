import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandasql as psql
from  libraries.utility import Utility
from libraries.custom_excel_output import custom_excel_output
from libraries.db_base import db_base
import pandasql as psql



class database_aggregator(Utility):

    def __init__(self,load_data_from_url=False):
        super().__init__()


    def get_customer_data(self):
        dbprod = db_base("products")
        prod_info = dbprod.run_query_with_single_df(query_key="get_product_info")
        dbfin = db_base("finance",svr_type='postsql')
        fin_account_activity = dbfin.run_query_with_single_df(query_key="get_account_activity")
        dbcust = db_base("customers",svr_type='mysql')
        sql = self.get_data_from_file(os.path.join(self.get_this_dir(),"libraries","psql_queries","aggregate_customer_info.psql"))
        df = psql.sqldf(sql)
        print(sql)

    def print_internal_directory(self):

        for k,v in self.__dict__.items():
            print("{} is \"{}\"".format(k,v))


