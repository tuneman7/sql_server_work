from libraries.database_aggregator import database_aggregator as database_aggregator
from libraries.utility import Utility
import numpy as np

import altair as alt
import os
import pandas as pd
import pandasql as psql
import math


class AltairRendering:


    def __init__(self,load_data_from_url=False):
        if load_data_from_url == True:
            self.my_data_object = database_aggregator()
        else:
            self.my_data_object = database_aggregator(load_data_from_url=load_data_from_url)


    def get_cust_summary_images(self,df):
        df["amt_usd"] = df["amt_usd"].replace('[\$,]', '', regex=True).astype(float)
        data = df

        # Assuming 'data' is your DataFrame after cleaning
        data['post_date'] = pd.to_datetime(data['post_date'])
        data['amt_usd'] = pd.to_numeric(data['amt_usd'])

        # Group the data by month and calculate the sum of 'amt_usd' in each month
        monthly_revenue = data.groupby(data['post_date'].dt.to_period("M")).sum()['amt_usd'].reset_index()

        # Convert the Period object to a string for 'post_date' column
        monthly_revenue['post_date'] = monthly_revenue['post_date'].dt.strftime('%Y-%m')


        # Altair Visualizations
        # 1. Monthly Revenue Over Time
        line = alt.Chart(monthly_revenue).mark_line().encode(
            x='post_date:T',
            y='amt_usd:Q'
        )

        points = alt.Chart(monthly_revenue).mark_point(size=150, opacity=0).encode(
            x='post_date:T',
            y='amt_usd:Q',
            tooltip=[alt.Tooltip('post_date:T', title='Date'), alt.Tooltip('amt_usd:Q', title='Revenue', format='$,.2f')]
        )

        monthly_revenue_chart = line + points
        monthly_revenue_chart = monthly_revenue_chart.properties(
            title='Monthly Revenue Over Time',
            width=300,
            height=150
        )
        # 2. Distribution of Transaction Amounts with Sine Wave
        transaction_distribution_chart = alt.Chart(data).mark_bar(color='#bdd7e7').encode(
            alt.X("amt_usd:Q", bin=alt.Bin(maxbins=30), title='Transaction Amount (USD)'),
            y='count()',
            tooltip=[alt.Tooltip('count()', title='Number of Transactions'), alt.Tooltip('amt_usd:Q', title='Amount', format='$,.2f')]
        ).properties(
            title='Distribution of Transaction Amounts',
            width=300,
            height=150
        )  # Combine the sine wave chart with the transaction distribution chart

        # Group the data by 'post_date' and 'product_type' and calculate the sum of 'amt_usd' in each group
        revenue_product_type = data.groupby(['post_date', 'product_type']).sum()['amt_usd'].reset_index()

        # Convert the 'post_date' column to a string for better visualization
        revenue_product_type['post_date'] = revenue_product_type['post_date'].dt.strftime('%Y-%m')


        # 3. Revenue by Product Type
        revenue_product_chart = alt.Chart(revenue_product_type).mark_bar(color='#bdd7e7').encode(
            x='amt_usd:Q',
            y=alt.Y('product_type:N', sort='-x'),
            tooltip=[alt.Tooltip('product_type:N', title='Product Type'), alt.Tooltip('amt_usd:Q', title='Revenue', format='$,.2f')]
        ).properties(
            title='Revenue by Product Type',
            width=300,
            height=150
        )

        # Combine charts into a single visualization
        combined_chart = alt.hconcat(monthly_revenue_chart, transaction_distribution_chart, revenue_product_chart).resolve_scale(
            color='independent'
        )

        #alt.data_transformers.enable('json')
        #alt.data_transformers.enable("vegafusion")
        alt.data_transformers.disable_max_rows()


        # Display the chart
        return combined_chart
