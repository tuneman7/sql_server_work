from includes import *
from flask import Blueprint
from libraries.database_aggregator import database_aggregator as da
from libraries.altair_rendering import AltairRendering as ar
from libraries.utility import Utility as mutil
import pandas as pd
import os
import requests

intro = Blueprint('intro', __name__)


@intro.route('/intro', methods=['POST', 'GET'])
def consume_fastapi_start():

        urls = {
        "BIGQUERY_API_URL": os.getenv("BIGQUERY_API_URL", "http://127.0.0.1:8028/docs"),
        "PRODUCTS_API_URL": os.getenv("PRODUCTS_API_URL", "http://127.0.0.1:8023/docs"),
        "CUSTOMERS_API_URL": os.getenv("CUSTOMERS_API_URL", "http://127.0.0.1:8024/docs"),
        "FINANCE_API_URL": os.getenv("FINANCE_API_URL", "http://127.0.0.1:8025/docs"),
        "DASHBOARD_URL": os.getenv("DASHBOARD_URL", "http://127.0.0.1:8026/"),
        "DASHBOARD_JN_URL": os.getenv("DASHBOARD_JN_URL", "http://127.0.0.1:8027/?tree"),
        "PYSPARK_JN_URL": os.getenv("PYSPARK_JN_URL", "http://127.0.0.1:8027/?tree")
        }

        url_status = {}
        for name, url in urls.items():
                try:
                        response = requests.get(url)
                        status = 'up' if response.status_code == 200 else 'down'
                        url_status[name] = {'url': url, 'status': status}                        
                except requests.ConnectionError:
                        status = 'down'
                        url_status[name] = {'url': url, 'status': status}


        res = make_response(render_template('pages/section_content/placeholder.intro.html',
        section_number="five",url_status=url_status))
        return res

