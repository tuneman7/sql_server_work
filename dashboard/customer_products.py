from includes import *
from flask import Blueprint
from libraries.database_aggregator import database_aggregator as da
from libraries.altair_rendering import AltairRendering as ar
from libraries.utility import Utility as mutil
import pandas as pd
import os
import redis
import glob


customer_products = Blueprint('customer_products', __name__)

#create one instance of this so it doesn't
#need to be re-used
mda = da()
mu = mutil()

@customer_products.route('/customer_revenue_start', methods=['POST', 'GET'])
def consume_fastapi_start():
        print("dealio")

        res = make_response(render_template('pages/section_content/placeholder.customer_revenue.html',
        section_number="five"))
        return res

def clear_json_files():
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
        total_slides = 3
        slide_no=1
        nav_to_section = False
        event_text = None
        
        if request.method == 'POST':
                event_name = request.form["event_name"]
                slide_no = int(request.form["slide_no"])
                nav_to_section = request.form["nav_to_section"]
                print(slide_no,event_name)

        try:
                file_name = event_name.lower() +"_"+ str(slide_no)+".txt"

                print("file_name={}".format(file_name))

                load_file_name = os.path.join(mu.get_this_dir(),"static","data",event_name,file_name)
                print(load_file_name)
                event_text = mu.get_data_from_file(load_file_name)
        except:
                fido="dido"

        print("nav_to_section",nav_to_section)


        print(slide_no,event_name)

        mar = ar()
        
        if slide_no==1:
                chart_json = mar.get_cust_summary_images(mda.get_customer_product_data()).configure_axis(
                        grid=False
                ).configure_view(
                        strokeWidth=0
                ).to_json()
                    
        if slide_no==2:
                chart_json = mar.get_circle_and_donut_graphs(mda.get_customer_product_data()).configure_axis(
                        grid=False
                ).configure_view(
                        strokeWidth=0
                ).to_json()

        insights = mda.extract_insights()

        res = jsonify({'htmlresponse':render_template('modal/customer_data.modal.html',titles=[''],
                                                      slide_no=slide_no,total_slides=total_slides,
                                                      insights=insights,event_text=event_text,
                                                      chart_json=chart_json,nav_to_section=nav_to_section)})

        return res

@customer_products.route('/api/data')
def data():

        df = mda.get_customer_product_data()
        df['post_date'] = pd.to_datetime(df['post_date'])
        df['post_date'] = df['post_date'].dt.strftime('%Y-%m-%d %H:%M')
        data_list = df.to_dict(orient="records")

        return jsonify({'data': data_list})
