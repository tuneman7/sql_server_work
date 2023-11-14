from includes import *
from flask import Blueprint
from flask import send_file
from libraries.database_aggregator import database_aggregator as da
from libraries.altair_rendering import AltairRendering as ar
from libraries.utility import Utility as mutil
from libraries.custom_excel_output import custom_excel_output as ceo
import pandas as pd
import os

api = Blueprint('api', __name__)


@api.route('/api/customer_transaction_data')
def customer_transaction_data():
        mda = da()
        df = mda.get_customer_product_data()
        df['post_date'] = pd.to_datetime(df['post_date'])
        df['post_date'] = df['post_date'].dt.strftime('%Y-%m-%d %H:%M')
        data_list = df.to_dict(orient="records")
        return jsonify({'data': data_list})

@api.route('/api/customer_transaction_excel')
def customer_transaction_excel():
        mda = da()
        df = mda.get_customer_product_data()
        df['post_date'] = pd.to_datetime(df['post_date'])
        df['post_date'] = df['post_date'].dt.strftime('%Y-%m-%d %H:%M')

        dbcust = ceo(current_database="customers",svr_type='mysql')        

        file_name = os.path.join(dbcust.get_this_dir(),"project_data","tempdir","customer_account_activity.xlsx")

        df["amt_usd"] = df["amt_usd"].replace('[\$,]', '', regex=True).astype(float)

        l_dfs = []
        l_dfs.append(df)
        dbcust.write_excel_from_dfs(list_of_dfs=l_dfs,file_name=file_name,add_subtotal_on_top=True)



        #print(data_list)
        return send_file(file_name, as_attachment=True)
