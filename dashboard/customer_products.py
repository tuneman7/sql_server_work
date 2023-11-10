from includes import *
from flask import Blueprint
from libraries.database_aggregator import database_aggregator as da
from libraries.altair_rendering import AltairRendering
import os

customer_products = Blueprint('customer_products', __name__)


@customer_products.route('/customer_revenue_start', methods=['POST', 'GET'])
def consume_fastapi_start():
        print("dealio")

        res = make_response(render_template('pages/section_content/placeholder.customer_revenue.html',
        section_number="five"))
        return res

def dataframe_to_dict(dataframe):
    print(jsonify({'data': dataframe.to_dict(orient='records')}))
    return jsonify({'data': dataframe.to_dict(orient='records')})

@customer_products.route('/render_customer_products', methods=['POST', 'GET'])
def render_customer_data_modal(popout = False):

        chart_json=None
        total_slides = 1
        slide_no=1

        res = jsonify({'htmlresponse':render_template('modal/customer_data.modal.html',titles=[''],
                                                      slide_no=slide_no,total_slides=total_slides,chart_json=chart_json)})

        return res

@customer_products.route('/api/data')
def data():
        mda = da()
        df = mda.get_customer_product_data()
        data_list = df.to_dict(orient="records")
        #print(data_list)
        return jsonify({'data': data_list})
