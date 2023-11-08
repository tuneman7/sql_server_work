from codecs import iterdecode
from copyreg import pickle
from itertools import count
import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp
#from tkinter import S
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandasql as psql
from  libraries.utility import Utility
from  libraries.db_base import db_base
import pickle
import sympy
from pprint import pprint
import time
import datetime
import glob
import re
import vl_convert as vlc
import io
import xlsxwriter

class excel_output(db_base):
    '''
    Simulate some data
    '''
    excel_output_directory = None
    def __init__(self,current_database=None,svr_type='mssql',artifact_dir='db_artifacts',excel_output_directory=None):
        super().__init__(current_database=current_database,svr_type=svr_type,artifact_dir=artifact_dir)
        #db_base.__init__(self,current_database=current_database)

        if excel_output_directory is None:
            excel_output_directory = os.path.join(self.get_this_dir(),"project_data","excel_extracts")
            self.mkdir(excel_output_directory)
        self.excel_output_directory = excel_output_directory

    def output_excel_doc_from_query(self,query_key=None,excel_file_name=None,excel_output_dir=None,sheet_name=None,sub_dir=None,top_row_filter=True,startrow=0,add_subtotal_on_top=False):
        if query_key is None:
            return
        else:
            print(query_key)
        if excel_file_name is None:
            excel_file_name = query_key + ".xlsx"
        if excel_output_dir is None:
            excel_output_dir = self.excel_output_directory
        if sheet_name is None:
            sheet_name = "Sheet 1"
        
        if sub_dir is not None:
            excel_output_dir = os.path.join(excel_output_dir,sub_dir)

        self.mkdir(excel_output_dir)

        outfile = os.path.join(excel_output_dir,excel_file_name)
        
        self.nukefile(outfile)

        start_time_first = time.time()
        df = self.run_query_with_single_df(query_key=query_key)
        print("--- database extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))

        start_time_first = time.time()
        with pd.ExcelWriter(outfile,engine='xlsxwriter',engine_kwargs={'options': {'strings_to_numbers': True}}) as writer:
            df.to_excel(writer,sheet_name=sheet_name,freeze_panes=(1+startrow,0),index=False,startrow=startrow)
            self.format_worksheet(writer=writer,worksheet=writer.sheets[sheet_name],sheet_name=sheet_name,df=df,top_row_filter=top_row_filter,startrow=startrow,add_subtotal_on_top=add_subtotal_on_top)  # format worksheet
        print("--- excel creation time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        return outfile,df.head(5)
        

    def format_worksheet(self,writer,worksheet,sheet_name,df,top_row_filter=True,startrow=0,add_subtotal_on_top=False):
        if add_subtotal_on_top and len(df)>1:
            cols_for_sub = dict()
            pos = 0
            #Add subtotals on top if needed.
            for column in df:
                if "amt" in str(column).lower():
                    cols_for_sub[xlsxwriter.utility.xl_col_to_name(pos)] = pos
                pos = pos+1
            for key in cols_for_sub.keys():
                pos = cols_for_sub[key]
                my_range = "{}{}:{}{}".format(key,startrow+1,key,len(df)-startrow) 
                formula = "=SUBTOTAL(9,{}{}:{}{})".format(key,startrow+1,key,len(df)-startrow)
                if not startrow ==0:
                    worksheet.write(startrow-1,pos,formula)
        if top_row_filter:
            worksheet.autofilter(startrow, 0, df.shape[0], df.shape[1])
        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))+6
            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)
        #Format mpm numbers as "other" -- to prevent scientific notation
        pos = 0
        cols_for_mpm = dict()
        for column in df:
            if ("_mpm" in str(column).lower()) or ("mpm_" in str(column).lower()) :
                cols_for_mpm[xlsxwriter.utility.xl_col_to_name(pos)] = pos
            pos = pos+1
        for key in cols_for_mpm.keys():
            try:
                pos = cols_for_mpm[key]
                my_range = "{}{}:{}{}".format(key,startrow+1,key,len(df)+startrow+1) 
                custom_format = writer.book.add_format({'num_format':'0'})
                writer.sheets[sheet_name].conditional_format(my_range, {'type': 'cell',
                                            'criteria' : '>', 
                                            'value' : -99999999999,
                                            'format' : custom_format})
            except Exception as e:
                print("Error: %s : %s" % (sheet_name, str(e)))




