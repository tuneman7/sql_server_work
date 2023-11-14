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
        data = df
        data["amt_usd"] = data["amt_usd"].replace('[\$,]', '', regex=True).astype(float)

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
    
    def get_circle_and_donut_graphs(self,df):

        # Assuming df is your DataFrame
        data = df
        
        data = df
        data["amt_usd"] = data["amt_usd"].replace('[\$,]', '', regex=True).astype(float)

        # For the pie chart, visualize the revenue per product type
        pie_data = data.groupby('product_type')['amt_usd'].sum().reset_index()

        # Calculate total revenue by city
        city_revenue = data.groupby('location_name')['amt_usd'].sum().reset_index()
        total_revenue = city_revenue['amt_usd'].sum()
        city_revenue['revenue_percentage'] = (city_revenue['amt_usd'] / total_revenue) * 100

        # Get the transaction count for each city
        city_transactions = data['location_name'].value_counts().reset_index()
        city_transactions.columns = ['location_name', 'transactions']

        # Merge the revenue percentage data with the transaction count data
        top_cities = city_transactions.merge(city_revenue, on='location_name')

        # Take the top 10 cities based on transaction count
        top_cities = top_cities.head(10)

        # Define a more subdued color scheme
        subdued_colors = ['#6baed6', '#bdd7e7', '#fdbe85', '#fdae6b', '#a1d99b', '#e5f5e0', '#bcbddc', '#9e9ac8', '#fcc5c0', '#fc9272']

        # Creating a pie chart with a legend to the right and the subdued color scheme, formatting numbers in USD
        pie_chart = alt.Chart(pie_data).mark_arc().encode(
            theta=alt.Theta(field='amt_usd', type='quantitative'),
            color=alt.Color(field='product_type', type='nominal', legend=alt.Legend(title='Product Type', orient='right'), scale=alt.Scale(range=subdued_colors)),
            tooltip=[alt.Tooltip('product_type:N'), alt.Tooltip('amt_usd:Q', title='Revenue', format='$,.2f')]
        ).properties(title='Revenue per Product Type', width=400)

        # Creating a donut chart for the top 10 cities with a legend to the right and the subdued color scheme
        donut_chart = alt.Chart(top_cities).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field='transactions', type='quantitative'),
            color=alt.Color(field='location_name', type='nominal', legend=alt.Legend(title='Top Cities', orient='right'), scale=alt.Scale(range=subdued_colors)),
            tooltip=[alt.Tooltip('location_name:N'), 
                    alt.Tooltip('transactions:Q', title='Transactions', format=','), 
                    alt.Tooltip('revenue_percentage:Q', title='Revenue %', format='.2f'),
                    alt.Tooltip('amt_usd:Q', title='Revenue', format='$,.2f')]
        ).properties(title='Top 10 Cities by Transaction Count, Revenue Percentage, and Dollar Amount', width=400)

        # Combine the charts
        combined_charts = alt.hconcat(
            pie_chart, donut_chart
        ).resolve_scale(
            color='independent'
        ).configure_view(
            stroke=None
        )

        # To display the charts in the notebook, if you're running Jupyter Notebook or JupyterLab
        return combined_charts
