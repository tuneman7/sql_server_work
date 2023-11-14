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
from libraries.utility import Utility
from libraries.custom_excel_output import custom_excel_output
from libraries.db_base import db_base
import redis
import copy

class database_aggregator(Utility):

    # Define cache_key as a class attribute
    cache_key = 'customer_product_data'

    def __init__(self, load_data_from_url=False):
        super().__init__()
        # Attempt to initialize Redis client, handle failure gracefully
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        except redis.RedisError:
            self.redis_client = None
        self.customer_product_data = self.get_customer_product_data_with_cache()

    def get_ttl_from_env(self):
        # Get TTL from environment variable redis_cache_ttl or default to 600
        ttl = int(os.environ.get('redis_cache_ttl', 600))
        return ttl

    def get_customer_product_data_with_cache(self):
        # Get TTL from environment variable redis_cache_ttl or default to 600
        ttl = self.get_ttl_from_env()

        # Check if Redis client is initialized and data is in cache
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(database_aggregator.cache_key)
                if cached_data:
                    df = pd.read_json(cached_data)
                    return df
            except redis.RedisError:
                # If Redis operation fails, proceed to fetch data from the database
                pass

        # Fetch data from the database if not in cache or Redis is not available
        return self.fetch_data_from_database(ttl)  # Pass ttl as an argument

    def fetch_data_from_database(self, ttl):
        # Spin up the individual databases
        dbprod = db_base("products")
        prod_info = dbprod.run_query_with_single_df(query_key="get_product_info")
        dbfin = db_base("finance", svr_type='postsql')
        fin_account_activity = dbfin.run_query_with_single_df(query_key="get_account_activity")
        dbcust = db_base("customers", svr_type='mysql')
        cust_products = dbcust.run_query_with_single_df(query_key="get_customer_product_history1")
        sql = self.get_data_from_file(os.path.join(self.get_this_dir(), "libraries", "psql_queries", "aggregate_customer_info.psql"))

        # Tie their output together within a dataframe
        df = psql.sqldf(sql)

        # Cache the data if Redis client is available
        if self.redis_client:
            try:
                self.redis_client.setex(database_aggregator.cache_key, ttl, df.to_json(date_format='iso'))
            except redis.RedisError:
                # If Redis operation fails, proceed without caching
                pass

        return df

    def get_customer_product_data(self):
        return self.customer_product_data
    
    def extract_insights(self):

        # Load the dataset
        data = copy.deepcopy(self.customer_product_data)

        data['amt_usd'] = pd.to_numeric(data['amt_usd'], errors='coerce')

        # First Set of Insights
        first_set = {
            'total_transactions': len(data),
            'average_transaction_amount': f"${data['amt_usd'].mean():,.2f}",
            'max_transaction_amount': f"${data['amt_usd'].max():,.2f}",
            'min_transaction_amount': f"${data['amt_usd'].min():,.2f}",
            'std_dev_transaction_amount': f"${data['amt_usd'].std():,.2f}"
        }

        # Second Set of Insights
        total_revenue = data['amt_usd'].sum()
        city_with_most_revenue = data.groupby('location_name')['amt_usd'].sum().idxmax()
        revenue_in_highest_grossing_city = data.groupby('location_name')['amt_usd'].sum().max()

        second_set = {
            'total_revenue': f"${total_revenue:,.2f}",
            'city_with_most_revenue': city_with_most_revenue,
            'revenue_in_highest_grossing_city': f"${revenue_in_highest_grossing_city:,.2f}"
        }

        # Third Set of Insights
        highest_grossing_product = data.groupby('product_name')['amt_usd'].sum().idxmax()
        highest_grossing_channel = data.groupby('channel_desc')['amt_usd'].sum().idxmax()

        third_set = {
            'highest_grossing_product': highest_grossing_product,
            'highest_grossing_channel': highest_grossing_channel
        }

        # Combine all insights
        combined_insights = {**first_set, **second_set, **third_set}
        return combined_insights



    def print_internal_directory(self):
        for k, v in self.__dict__.items():
            print("{} is \"{}\"".format(k, v))
