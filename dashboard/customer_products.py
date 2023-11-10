from includes import *
from flask import Blueprint
from libraries.database_aggregator import database_aggregator as da
from libraries.altair_rendering import AltairRendering as ar
from libraries.utility import Utility as mutil
import pandas as pd
import os

customer_products = Blueprint('customer_products', __name__)


@customer_products.route('/customer_revenue_start', methods=['POST', 'GET'])
def consume_fastapi_start():
        print("dealio")

        res = make_response(render_template('pages/section_content/placeholder.customer_revenue.html',
        section_number="five"))
        return res

import glob
import os
def clear_json_files():
        mu = mutil()
        pattern = 'altair-data*.json'
        # Get a list of matching files in the directory
        matching_files = glob.glob(os.path.join(mu.get_this_dir(), pattern))

        
        if matching_files:
                for file_path in matching_files:
                        # Loop through the matching files and delete them
                        for file_path in matching_files:
                                os.remove(file_path)

         
@customer_products.route('/render_customer_products', methods=['POST', 'GET'])
def render_customer_data_modal(popout = False):

        chart_json=None
        total_slides = 1
        slide_no=1

        mar = ar()
        mda = da()
        
        chart_json = mar.get_cust_summary_images(mda.get_customer_product_data()).configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()            


        res = jsonify({'htmlresponse':render_template('modal/customer_data.modal.html',titles=[''],
                                                      slide_no=slide_no,total_slides=total_slides,chart_json=chart_json)})

        return res

@customer_products.route('/api/data')
def data():
        mda = da()
        df = mda.get_customer_product_data()
        df['post_date'] = pd.to_datetime(df['post_date'])
        df['post_date'] = df['post_date'].dt.strftime('%Y-%m-%d %H:%M')
        data_list = df.to_dict(orient="records")
        #print(data_list)
        return jsonify({'data': data_list})
