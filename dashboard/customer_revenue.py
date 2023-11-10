from includes import *
from flask import Blueprint
from libraries.database_aggregator import database_aggregator as da
import os

customer_revenue = Blueprint('customer_revenue', __name__)


@customer_revenue.route('/customer_revenue_start', methods=['POST', 'GET'])
def consume_fastapi_start():
        print("dealio")
        mda = da()
        mda.get_customer_data()
        res = make_response(render_template('pages/section_content/placeholder.customer_revenue.html',
        section_number="five"))
        return res


@customer_revenue.route('/get_customer_revenue', methods=['POST', 'GET'])
def render_customer_data_modal(popout = False):

        res = jsonify({'htmlresponse':render_template('modal/customer_data.modal.html')})

        return res
