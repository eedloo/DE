import pandas as pd
pd.set_option('mode.chained_assignment', None)
import numpy as np
import json
import seaborn as sns
import re
import requests

def ubereat_restaurants():
    '''
    The function loads, clean, and outputs a dataframe from the file "Ubereats_restaurants.csv"
    * Cleaning:
        ! dropping unnecessary columns
        ! removing records without address or price range
        ! Puerto Rico territory (PR) is the only state that do not have state 2-letter abreviation. Added on line 35.
    * Transformation and engineering:
        ! the name column in the original data has some level of address data. Removed.
        ! price range was in $ format. Converted to numeric.
        ! full-address column splitted to 4: address, city, state, zip.
    Since the data was not clean, there was some level of differentiation. Therefore, some useful commands like "pd.str.split()"
    could not be used.     

    * Input:
        None
    
    * Output:
        Dataframe
    '''
    ubereat_res = pd.read_csv('./Data/Ubereats_restaurants.csv')
    ub_df = ubereat_res.drop(['lat', 'lng', 'zip_code'], axis = 1)
    ub_clean = ub_df[(ub_df.price_range.notna() & ub_df.full_address.notna())].reset_index(drop = True)
    for i in range(len(ub_clean)):
        name = ub_clean.loc[i, 'name'].split('(')
        if len(name) == 2:
            ub_clean.loc[i, 'name'] = name[0][:-1]
        else:
            ub_clean.loc[i, 'name'] = name[0]
        full_address = ub_clean.loc[i, 'full_address'].rsplit(',', 3)
        ub_clean.loc[i, ['address', 'city', 'state', 'zip']] = \
            [full_address[0], full_address[1][1:], full_address[2][1:], full_address[3][1:]]
    ub_clean.price_range.replace(['$$$$', '$$$', '$$', '$'], [4, 3, 2, 1], inplace = True)
    ub_clean.loc[ub_clean[ub_clean.state == ''].index, 'state'] = 'PR'
    colnames = ['id', 'position', 'name', 'address', 'city', 'state', 
                'zip', 'score', 'ratings', 'price_range', 'category']
    ub_clean = ub_clean[colnames]
    return ub_clean


def ubereat_menus():
    '''
    The function loads, cleans, and aggregates "ubereats_restaurant_menus.csv".

    * Cleaning:
        ! Dropping unnecessary columns
        ! Renaming columns
    * Transformation and engineering:
        ! Transform price value
            Example:
                "12.22 USD" --> 12.22
        ! Data aggregation to find mean of menu price and the food variety of restaurants. 
        The number of selections in each restaurant's menu has been captured, and mapped to 4 level of variaty.
        For levels, quantile of data has been used.

    * Input:
        None
    * Output:
        Dataframe
    '''
    ubereat_men = pd.read_csv('./Data/Ubereats_restaurant_menus.csv')
    ubereat_men.drop(['name', 'description'], axis=1, inplace=True)
    ubereat_men.price.replace(to_replace='\s\w{3}', regex = True, value='', inplace=True)
    ubereat_men.price = pd.to_numeric(ubereat_men.price, downcast='float')
    ubereat_men_agg = ubereat_men[['restaurant_id', 'price']].groupby('restaurant_id').agg(['mean', 'count'])
    ubereat_men_agg.columns = ubereat_men_agg.columns.droplevel()
    ubereat_men_agg.reset_index(inplace=True)
    ubereat_men_agg['variaty_level'] = pd.cut(ubereat_men_agg['count'], 
    bins=list(ubereat_men_agg['count'].quantile([0, .25, .5, .75, 1])), 
    include_lowest = True, 
    labels = [1, 2, 3, 4])
    ubereat_men_agg.drop('count', axis=1, inplace=True)
    ubereat_men_agg.columns = ['restaurant_id', 'menu_avg_price', 'variaty_level']
    return ubereat_men_agg


def nations_list():
    '''
    The function reads a table from "www.ef.com" website to output Adjectivals of countries' name.
    * Example:
        Vietnam --> Vietnamese
        United States --> American
    
    * Input:
        None
    * Output:
        List
    '''

    path = requests.get("https://www.ef.com/wwen/english-resources/english-grammar/nationalities/")
    dfs = pd.read_html(path.text)
    data = dfs[1]
    countries = list(data.Adjective)
    return countries

def add_features(ubereat_res, countries=nations_list()):
    '''
    The function extracts and adds two new features to "ubereat_restaurant" data.
    It checkes category of each restaurant to see:
            ! Does the restaurant have multi-nations food?
                If the restaurant has more that one country name in its menu, it will be considered international.
            ! Is the restaurant Vegetarian-friendly?
    
    * Input:
        ! ubereat_restaurant dataframe
        ! list of countries' adjectivals
    * Output:
        ! Dataframe
    '''

    for i in ubereat_res[ubereat_res.category.notna()].index:
        categories_str = ubereat_res[ubereat_res.category.notna()].loc[i, 'category']
        categories_list = categories_str.split(', ')
        international_level = len(list(np.intersect1d(categories_list, countries)))
        if international_level > 1:
            ubereat_res.at[i, 'international'] = 1
        else:
            ubereat_res.at[i, 'international'] = 0
        if 'Vegetarian' in categories_str:
            ubereat_res.at[i, 'Vegetarian'] = 1
        else:
            ubereat_res.at[i, 'Vegetarian'] = 0
    return ubereat_res
