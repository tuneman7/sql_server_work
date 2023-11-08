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
#from  libraries.utility import Utility
#from  libraries.db_base import db_base
from  libraries.excel_output import excel_output
import pickle
import sympy
from pprint import pprint
import time
import datetime
import glob
import re
import vl_convert as vlc
import io
import shutil


class custom_excel_output(excel_output):
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
        
    def get_list_of_contracts(self,query_key=None,excel_file_name=None,excel_output_dir=None,sheet_name=None,sub_dir=None,top_row_filter=True):
        if query_key is None:
            return
        if excel_file_name is None:
            excel_file_name = query_key + ".xlsx"
        if excel_output_dir is None:
            excel_output_dir = self.excel_output_directory
        if sheet_name is None:
            sheet_name = "Sheet 1"
        
        if sub_dir is not None:
            excel_output_dir = os.path.join(excel_output_dir,sub_dir)        
        df = self.run_query_with_single_df(query_key)
        list_of_dicts = []
        for series_name, season_name, episode_name, version_name, guild_name,contract_version_id,product_id,season_product_id,episode_mpm in zip(df["series_name"],df["season_name"],df["episode_name"],df["version_name"],df["guild_name"],df["contract_version_id"],df["product_id"],df["season_product_id"],df["episode_mpm"]):
            this_dict = dict()
            file_path = os.path.join(excel_output_dir,self.slugify(series_name))

            with self.suppress_stdout():
                this_dict["series_dir"] = file_path
                self.mkdir(file_path)
                dir_name = "{}_{}".format(self.slugify(season_name),self.slugify(str(season_product_id)))
                file_path = os.path.join(file_path,dir_name)
                this_dict["season_dir"] = file_path
                self.nukepath(file_path)
                self.mkdir(file_path)

            file_name = "{}_{}_{}_{}_{}".format(self.slugify(episode_name),self.slugify(version_name),self.slugify(guild_name),self.slugify(contract_version_id),self.slugify(product_id))
            this_dict["product_id"] = product_id
            this_dict["contract_version_id"] = contract_version_id
            this_dict["file_path"] = file_path
            this_dict["file_name"] = file_name + ".xlsx"
            this_dict["episode_mpm"] = episode_mpm
            dfs_dict = dict()
            df_dict = dict()
            df_dict["df"] = df.loc[(df["product_id"] == product_id) & (df["contract_version_id"] == contract_version_id)  ]#.to_json(orient="records")
            dfs_dict["contract_df"] = df_dict
            this_dict["dfs"] = dfs_dict
            list_of_dicts.append(this_dict)
        return list_of_dicts, df

    def  export_residuals_contracts(self,query_key=None,excel_file_name=None,excel_output_dir=None,sheet_name=None,sub_dir=None,top_row_filter=True):

        start_time_total = time.time()

        #get the contracts -- defauled passed in: get_list_of_residuals_contracts
        start_time_first = time.time()
        list_of_contract_objects, contract_df = self.get_list_of_contracts(query_key=query_key,sub_dir=sub_dir)
        print("--- contract extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        
        #get the cast list        
        start_time_first = time.time()
        list_of_contract_objects, cast_df = self.add_cast_list(list_of_contract_objects=list_of_contract_objects)
        print("--- cast extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))

        # #get the cast payment history
        start_time_first = time.time()        
        list_of_contract_objects, payment_df = self.add_payment_history(list_of_contract_objects=list_of_contract_objects)
        print("--- tr_obligation_talent_calc extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        #payment_df = pd.DataFrame()

        #get stuff out of tc_pymt_tran
        #get_contract_cast_payment_history_summary
        start_time_first = time.time()
        list_of_contract_objects, payment_history_df = self.add_payment_history_summary(list_of_contract_objects=list_of_contract_objects)
        print("--- tc_pymt_tran extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))

        start_time_first = time.time()
        list_of_contract_objects, payment_by_max_day_id_df = self.get_payment_by_max_day_id(list_of_contract_objects=list_of_contract_objects)
        print("--- get_payment_by_max_day_id extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        

        #get stuff out of tc_pymt_tran
        #get_contract_cast_payment_history_summary
        start_time_first = time.time()
        list_of_contract_objects, streaming_dates_df = self.add_streaming_dates(list_of_contract_objects=list_of_contract_objects)
        print("--- add_streaming_dates extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))

        #get_contract_cast_payment_history_summary
        start_time_first = time.time()
        print("--- Starting the Excel Document Printing")
        self.write_contract_excel_documents(list_of_contract_objects=list_of_contract_objects,limiter=None)
        print("--- total write time: %s seconds ---" % (float(time.time()) - float(start_time_first)))

        start_time_first = time.time()
        # print(contract_df.info())
        # print(cast_df.info())
        # print(payment_df.info())
        # print(payment_history_df.info())
        df_dict = dict()
        df_dict["contract_df"] = contract_df
        df_dict["cast_df"] =cast_df
        df_dict["payment_df"] =payment_df
        df_dict["payment_history_df"] =payment_history_df
        df_dict["streaming_dates_df"] = streaming_dates_df
        df_dict["payment_by_max_day_id_df"] = payment_by_max_day_id_df
        
        return_dict = self.dump_dfs_to_files(df_dict)
        print("--- csv dump time: %s seconds ---" % (float(time.time()) - float(start_time_first)))

        #create excel output.
        start_time_first = time.time()
        zip_file_name = self.excel_output_directory
        shutil.make_archive(zip_file_name,'zip',self.excel_output_directory)
        print("--- zip file creation time: %s seconds ---" % (float(time.time()) - float(start_time_first)))

        print("--- Total Time: %s seconds ---" % (float(time.time()) - float(start_time_total)))
        return(return_dict)
        #return self.dump_dfs_to_files(payment_history_df)


    def dump_dfs_to_files(self,df_dict,outdir=None):
        dict_out = dict()
        if outdir is None:
            outdir = os.path.join(self.get_this_dir(),"project_data","excel_extracts","csv_dumps")
        self.mkdir(outdir)
        for key in df_dict:
            outfile = os.path.join(outdir,key+".csv")
            print(outfile)
            df = df_dict[key]
            df.to_csv(outfile,header=True,index=False)
            dict_out[key]= outfile


    

    def  get_payment_by_max_day_id(self,query_key=None,excel_file_name=None,excel_output_dir=None,sheet_name=None,sub_dir=None,top_row_filter=True,list_of_contract_objects=None):
        start_time_first = time.time()
        df = self.run_query_with_single_df("get_contract_information_flattened_by_max_day_id")
        print("--- database extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        df["product_id"] = df["product_id"].astype(int)
        df["contract_version_id"] = df["contract_version_id"].astype(int)
        output_list = []
        start_time_first = time.time()
        for contract in list_of_contract_objects:
            product_id = int(contract["product_id"])
            contract_version_id = int(contract["contract_version_id"])
            my_df = df.loc[(df["product_id"] == product_id) & (df["contract_version_id"] == contract_version_id)]
            df_dict = dict()
            df_dict["df"] = my_df
            df_dict["startrow"] = 1
            df_dict["add_subtotal_on_top"] = "True"            
            contract["dfs"]["LastCalculation_df"]=df_dict
            output_list.append(contract)
        print("--- partitioning time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        return output_list, df


    def  add_payment_history_summary(self,query_key=None,excel_file_name=None,excel_output_dir=None,sheet_name=None,sub_dir=None,top_row_filter=True,list_of_contract_objects=None):
        start_time_first = time.time()
        df = self.run_query_with_single_df("get_contract_cast_payment_history_summary")

        excel_file_name = os.path.join(self.get_this_dir(),"project_data","excel_extracts","cast_extract","get_contract_cast_payment_history_summary.xlsx")

        self.write_excel_from_dfs(list_of_dfs=[df],file_name=excel_file_name)

        print("--- database extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        df["product_id"] = df["product_id"].astype(int)
        df["contract_version_id"] = df["contract_version_id"].astype(int)
        output_list = []
        start_time_first = time.time()
        for contract in list_of_contract_objects:
            product_id = int(contract["product_id"])
            contract_version_id = int(contract["contract_version_id"])
            my_df = df.loc[(df["product_id"] == product_id) & (df["contract_version_id"] == contract_version_id)]
            df_dict = dict()
            df_dict["df"] = my_df
            df_dict["startrow"] = 1
            df_dict["add_subtotal_on_top"] = "True"            
            contract["dfs"]["PaymentHistory_df"]=df_dict
            output_list.append(contract)
        print("--- partitioning time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        return output_list, df

    def  add_streaming_dates(self,query_key=None,excel_file_name=None,excel_output_dir=None,sheet_name=None,sub_dir=None,top_row_filter=True,list_of_contract_objects=None):
        start_time_first = time.time()
        df = self.run_query_with_single_df("get_list_of_residuals_contracts_streaming_dates")
 #       print(df.head(200))
        print("--- database extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        df["episode_mpm_number"] = df["episode_mpm_number"].astype(str)
        output_list = []
        start_time_first = time.time()
        for contract in list_of_contract_objects:
            episode_mpm_number = contract["episode_mpm"]
            #print(episode_mpm_number)
            sql = 'select * from df where episode_mpm_number = \'' + str(episode_mpm_number) + '\''
            #print(sql)
            token_replacements=dict()
            #def run_query_with_single_df_tokenify(self,query_key=None,query_text=None,current_database=None,token_replacements=dict()):
            token_replacements["select * from #streaming_date_results"] = "select * from #streaming_date_results where episode_mpm_number = \'{}\'".format(episode_mpm_number)
            my_df = df.loc[(df.episode_mpm_number.str.contains(str(episode_mpm_number)))]
            #my_df = psql.sqldf(sql)
            #print(df.info())
#            print(my_df.head(10))
#            print(episode_mpm_number)
#            print(len(df))
            df_dict = dict()
            df_dict["df"] = my_df
            df_dict["startrow"] = 0
            df_dict["add_subtotal_on_top"] = "False"            
            contract["dfs"]["Airdates_df"]=df_dict
            output_list.append(contract)
        print("--- partitioning time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        return output_list, df



    def  add_payment_history(self,query_key=None,excel_file_name=None,excel_output_dir=None,sheet_name=None,sub_dir=None,top_row_filter=True,list_of_contract_objects=None):
        start_time_first = time.time()
        df = self.run_query_with_single_df("get_contract_cast_payment_history")

        excel_file_name = os.path.join(self.get_this_dir(),"project_data","excel_extracts","cast_extract","get_contract_cast_payment_history.xlsx")

        self.write_excel_from_dfs(list_of_dfs=[df],file_name=excel_file_name)

        print("--- database extract time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        df["product_id"] = df["product_id"].astype(int)
        df["contract_version_id"] = df["contract_version_id"].astype(int)
        output_list = []
        start_time_first = time.time()
        for contract in list_of_contract_objects:
            product_id = int(contract["product_id"])
            contract_version_id = int(contract["contract_version_id"])
            my_df = df.loc[(df["product_id"] == product_id) & (df["contract_version_id"] == contract_version_id)]
            df_dict = dict()
            df_dict["df"] = my_df  
            df_dict["startrow"] = 1         
            df_dict["add_subtotal_on_top"] = "True"
            contract["dfs"]["payments_df"]= df_dict
            output_list.append(contract)
        print("--- partitioning time: %s seconds ---" % (float(time.time()) - float(start_time_first)))
        return output_list, df



    def  add_cast_list(self,query_key=None,excel_file_name=None,excel_output_dir=None,sheet_name=None,sub_dir=None,top_row_filter=True,list_of_contract_objects=None):

        df = self.run_query_with_single_df("get_contract_cast_list_all")

        excel_file_name = os.path.join(self.get_this_dir(),"project_data","excel_extracts","cast_extract","get_contract_cast_list_all.xlsx")

        self.write_excel_from_dfs(list_of_dfs=[df],file_name=excel_file_name)

        df["product_id"] = df["product_id"].astype(int)
        df["contract_version_id"] = df["contract_version_id"].astype(int)
        output_list = []
        for contract in list_of_contract_objects:
            product_id = int(contract["product_id"])
            contract_version_id = int(contract["contract_version_id"])
            my_df = df.loc[(df["product_id"] == product_id) & (df["contract_version_id"] == contract_version_id)]
            df_dict = dict()
            df_dict["df"] = my_df
            contract["dfs"]["cast_df"]=df_dict
            output_list.append(contract)

        return output_list, df
    
    def write_contract_excel_documents(self,list_of_contract_objects=None,limiter=None,start_row=0):
        for contract in list_of_contract_objects:
            if limiter is not None:
                limiter = limiter -1
                #print("Limiter : {}".format(limiter))
                if limiter==0:
                    print("Reached limiter")
                    return            
            file_name = os.path.join(contract["file_path"],contract["file_name"])
            with pd.ExcelWriter(file_name,engine='xlsxwriter',engine_kwargs={'options': {'strings_to_numbers': True}}) as writer:
                for key in contract["dfs"].keys():
                    sheet_name = key.split('_')[0]
                    df = contract["dfs"][key]["df"]
                    startrow = int(contract["dfs"][key]["startrow"]) if "startrow" in contract["dfs"][key] else 0
                    add_subtotal_on_top = bool(contract["dfs"][key]["add_subtotal_on_top"]) if "add_subtotal_on_top" in contract["dfs"][key] else False
                    df.to_excel(writer,sheet_name=sheet_name,freeze_panes=(1+startrow,0),index=False,startrow=startrow)
                    self.format_worksheet(writer=writer,worksheet=writer.sheets[sheet_name],sheet_name=sheet_name,df=df,top_row_filter=True,startrow=startrow,add_subtotal_on_top=add_subtotal_on_top)

            
            # with pd.ExcelWriter(outfile,engine='xlsxwriter') as writer:
            #     df.to_excel(writer,sheet_name=sheet_name,freeze_panes=(1,0),index=False)
            #     self.format_worksheet(writer=writer,worksheet=writer.sheets[sheet_name],sheet_name=sheet_name,df=df,top_row_filter=top_row_filter)  # format worksheet

    def write_excel_from_dfs(self,list_of_dfs=None,limiter=None,start_row=0,file_name=None,add_subtotal_on_top=False,list_of_sheet_names=None):
        if file_name is None or list_of_dfs is None:
            return
        
        self.nukefile(file_name)

        self.mkdir(os.path.dirname(file_name))

        with pd.ExcelWriter(file_name,engine='xlsxwriter',engine_kwargs={'options': {'strings_to_numbers': True}}) as writer:
            use_sn_list = True if list_of_sheet_names is not None and (len(list_of_dfs)==len(list_of_sheet_names)) else False
            sn = 1
            for df in list_of_dfs:

                # Define a lambda function to remove trailing whitespaces
                remove_trailing_whitespace = lambda x: x.strip() if isinstance(x, str) else x

                # Apply the lambda function to all columns in the DataFrame
                df = df.applymap(remove_trailing_whitespace)


                #print(len(df))
                sheet_name = list_of_sheet_names[sn-1] if use_sn_list else "Sheet_" + str(sn)
                startrow = start_row + 1 if (add_subtotal_on_top == True and start_row==0) else start_row
                df.to_excel(writer,sheet_name=sheet_name,freeze_panes=(1+startrow,0),index=False,startrow=startrow)
                self.format_worksheet(writer=writer,worksheet=writer.sheets[sheet_name],sheet_name=sheet_name,df=df,top_row_filter=True,startrow=startrow,add_subtotal_on_top=add_subtotal_on_top)

        return

            
        




