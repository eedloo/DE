import numpy as np
import pandas as pd
pd.set_option('mode.chained_assignment', None)
from pandas import DataFrame, read_excel, read_csv, read_html
from dagster import asset
import json
import glob
import re
import pickle
import functions

__author__ = "Mohsen Eedloo"
__email__ = "Mohsen.eedloo@gmail.com"

@asset(group_name='Input_Data')
def restaurants_data() -> DataFrame:
    '''
    Opens, cleans, and output ubereat restaurant data. 
    '''
    ub_clean = functions.ubereat_restaurants()
    return ub_clean

@asset(group_name='Input_Data')
def menus_data() -> DataFrame:
    ''' 
    Opens, cleans, and output ubereat menus data. 
    '''
    menus = functions.ubereat_menus()
    return menus

@asset(group_name='Input_Data')
def countries_name() -> list:
    ''' 
    Uses data from the "www.ef.com" website to create a list of countries adjectivals.
    '''
    countries = functions.nations_list()
    return countries

@asset(group_name='Input_Data')
def census_data() -> DataFrame:
    ''' 
    Opens, cleans, and output US Census zipcodes income data. 
    '''
    census = functions.cunsus()
    return census

@asset(group_name='Intermediate')
def restaurants_feng(restaurants_data: DataFrame, countries_name: list) -> DataFrame:
    ''' 
    Does feature engineering on restaurants data.
    '''
    ub_rest = functions.restaurant_add_features(restaurants_data, countries = countries_name)
    return ub_rest

@asset(group_name='Intermediate')
def menus_feng(menus_data: DataFrame) -> DataFrame:
    ''' 
    Does feature engineering on menus data.
    '''
    ub_menu = functions.menus_add_features(menus_data)
    return ub_menu

@asset(group_name='Final')
def make_final_df(restaurants_feng: DataFrame, menus_feng: DataFrame, census_data: DataFrame) -> DataFrame:
    ''' 
    Builds the final dataframe by merging dataframes.
    '''
    return restaurants_feng.merge(menus_feng).merge(census_data)

