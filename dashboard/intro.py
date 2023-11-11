from includes import *
from flask import Blueprint
from libraries.database_aggregator import database_aggregator as da
from libraries.altair_rendering import AltairRendering as ar
from libraries.utility import Utility as mutil
import pandas as pd
import os

intro = Blueprint('intro', __name__)


@intro.route('/intro', methods=['POST', 'GET'])
def consume_fastapi_start():
        print("dealio")

        res = make_response(render_template('pages/section_content/placeholder.intro.html',
        section_number="five"))
        return res

