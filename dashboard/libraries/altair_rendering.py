from libraries.database_aggregator import database_aggregator as database_aggregator
from libraries.utility import Utility
import numpy as np

import altair as alt
from vega_datasets import data
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

