import pandas as pd
pd.set_option('mode.chained_assignment', None)
import numpy as np
import json
import seaborn as sns
import re
import requests

def ubereat_restaurants():
    '''
    The function loads, clean, and outputs a dataframe from the file "restaurants.csv"
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
    ubereat_res = pd.read_csv('./Data/restaurants.csv')
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
    ub_clean.rename(columns={'id': 'restaurant_id'}, inplace=True)
    return ub_clean


def ubereat_menus():
    '''
    The function loads, cleans, and aggregates "restaurant-menus.csv".

    * Cleaning:
        ! Dropping unnecessary columns
        ! Renaming columns
    * Transformation and engineering:
        ! Transform price value
            Example:
                "12.22 USD" --> 12.22
        ! Data aggregation to find mean of menus' prices.
        
    * Input:
        None
    * Output:
        Dataframe
    '''
    ubereat_men = pd.read_csv('./Data/restaurant-menus.csv')
    ubereat_men.drop(['name', 'description'], axis=1, inplace=True)
    ubereat_men.price.replace(to_replace='\s\w{3}', regex = True, value='', inplace=True)
    ubereat_men.price = pd.to_numeric(ubereat_men.price, downcast='float')
    ubereat_men_agg = ubereat_men[['restaurant_id', 'price']].groupby('restaurant_id').agg(['mean', 'count'])
    ubereat_men_agg.columns = ubereat_men_agg.columns.droplevel()
    ubereat_men_agg.reset_index(inplace=True)
    return ubereat_men_agg


def nations_list():
    '''
    The function reads a webpage from "www.ef.com" to output Adjectivals of countries' name.
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

def cunsus():
    '''
    The function loads US Census Median income per zipcode excel file, turns it to dataframe and output it after some modifications.
    We are only interested in two columns:
        * The second quantile (median)
        * Zipcode
    The cleaned dataframe later can be merged with other data to provide information about US zipcodes median income.

    Input:
        None

    Output:
        Dataframe
    
    '''
    cen = pd.read_excel('./Data/US-Census-data.xlsx', header=1)
    cols = ['Geographic Area Name', 'Estimate!!Quintile Means:!!Second Quintile']
    census = cen[cols]
    census.rename(columns={'Geographic Area Name': 'zip', 'Estimate!!Quintile Means:!!Second Quintile':'zip_median_income'}, inplace=True)
    census.zip.replace(to_replace='\w{5}\s', value='', regex = True, inplace = True)
    return census

def restaurant_add_features(ub_clean, countries=nations_list()):
    '''
    The function extracts and adds new features to "restaurant" data.
    It checkes category of each restaurant to see:
        ! Does the restaurant have international cuisines?
            If the restaurant has more that one country name in its menu, it will be considered international.
        ! Is the restaurant Vegetarian-friendly?
        ! Does the restaurant have bar?
    It also calculate the popularity factor of the restaurants by multiplying number of reviews and ratings and normalizing it.
    
    * Input:
        ! ubereat_restaurant dataframe
        ! ubereat_menus dataframe
        ! list of countries' adjectivals
    * Output:
        ! Dataframe
    '''
    from sklearn.preprocessing import MinMaxScaler
    normalizer = MinMaxScaler()
    for i in ub_clean[ub_clean.category.notna()].index:
        categories_str = ub_clean[ub_clean.category.notna()].loc[i, 'category']
        categories_list = categories_str.split(', ')
        international_level = len(list(np.intersect1d(categories_list, countries)))
        if international_level > 1:
            ub_clean.at[i, 'international'] = 1
        else:
            ub_clean.at[i, 'international'] = 0
        if 'Vegetarian' in categories_str:
            ub_clean.at[i, 'Vegetarian'] = 1
        else:
            ub_clean.at[i, 'Vegetarian'] = 0
        if 'Alcohol' in categories_str:
            ub_clean.at[i, 'bar'] = 1
        else:
            ub_clean.at[i, 'bar'] = 0
    ub_clean['popularity'] = normalizer.fit_transform(np.array(ub_clean.score * ub_clean.ratings).reshape(-1,1))
    return ub_clean

def menus_add_features(ubereat_men_agg):
    '''
    The function engineers a new feature and adds it to the ubereat menu data.
    The number of selections in each restaurant's menu will be captured, and mapped to 4 level of variaty.
    For levels, quantile of data has been used.

    * Input:
        ! ubereat_menus dataframe
    * Output:
        ! Dataframe
    '''

    ubereat_men_agg['variaty_level'] = pd.cut(ubereat_men_agg['count'], 
    bins=list(ubereat_men_agg['count'].quantile([0, .25, .5, .75, 1])), 
    include_lowest = True, 
    labels = [1, 2, 3, 4])
    ubereat_men_agg.drop('count', axis=1, inplace=True)
    ubereat_men_agg.columns = ['restaurant_id', 'menu_avg_price', 'variaty_level']
    return ubereat_men_agg
