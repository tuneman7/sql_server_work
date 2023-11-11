from includes import *
from flask import Blueprint
from libraries.database_aggregator import database_aggregator as da
from libraries.altair_rendering import AltairRendering as ar
from libraries.utility import Utility as mutil
import pandas as pd
import os

api = Blueprint('api', __name__)


@api.route('/api/customer_transaction_data')
def data():
        mda = da()
        df = mda.get_customer_product_data()
        df['post_date'] = pd.to_datetime(df['post_date'])
        df['post_date'] = df['post_date'].dt.strftime('%Y-%m-%d %H:%M')
        data_list = df.to_dict(orient="records")
        #print(data_list)
        return jsonify({'data': data_list})
