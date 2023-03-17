import pandas as pd
import numpy as np
pd.set_option('display.precision', 10)

__author__ = "Mohsen Eedloo"
__email__ = "Mohsen.eedloo@gmail.com"

valid = pd.read_csv('./data/car_price_prediction_output.valid')
valid = valid.sort_values('ID').reset_index(drop=True)
cs_df = pd.read_excel('./data/car_stocks.xlsx')


# Extracts starting and ending prices of each year, and calculate percent changes for each manufacturer
# Returns a dictionary with company's name as keys and extracted values of each year as values
def extract(dataframe):
    mfrs = list(cs_df.Manufacturer.unique())
    dic={}
    for j in range(len(mfrs)):
        sub_df = dataframe[dataframe['Manufacturer'] == mfrs[j]].sort_values('Date').reset_index(drop=True)
        sub_dic = {}
        for i in range(len(sub_df)):
            if 2*i < len(sub_df):
                starting = sub_df['Closing Price'].iloc[2*i]
                ending = sub_df['Closing Price'].iloc[2*i+1]
                PercentChange = (ending - starting) / starting
                year = sub_df['Date'].loc[2*i].year
                sub_dic[year] = [starting, ending, PercentChange]
        dic[mfrs[j]] = sub_dic
    return dic

# Calculates "Median Percent Changes For Year"
# The extract function's output dictionary is the input here
# Returns a dictionary with years of keys and median percent changes for that year as values
def mchange(data):
    years = list(range(2011, 2016))
    mfrs = list(cs_df.Manufacturer.unique())
    pchfy = {}
    for i in years:
        pch = []
        for j in mfrs:
            pch.append(data[j][i][2])
        pchfy[i] = np.median(pch)
    return pchfy

# Aggregates results from extract and mchange functions
# Returns nested list of required values
# Makes the data ready to build the stocks dataframe
def agg(dic, pchfy):
    years = list(range(2011, 2016))
    mfrs = list(cs_df.Manufacturer.unique())
    data = []
    for i in mfrs:
        for j in years:
            data.append([i, 
                         j, 
                         np.round(dic[i][j][0], 2), 
                         np.round(dic[i][j][1], 2), 
                         np.round(dic[i][j][2], 2), 
                         np.round(dic[i][j][2]-pchfy[j], 2)
                         ])
    return data

# Builds a clean dataframe with extracted and generated values
# Returns stocks dataframe
def make_df(data):
    colnames = [
        'Manufacturer', 
        'Prod. year', 
        'Starting Stock', 
        'Ending Stock', 
        'Stock Price Change', 
        'Percentile'
        ]
    stock_df = pd.DataFrame(columns= colnames, data=data)
    # normalizing -0s
    stock_df.replace(-0, 0, inplace=True)
    stock_df.loc[:, "Stock Price Change"] = stock_df["Stock Price Change"].map('{:.0%}'.format)
    stock_df.loc[:, "Percentile"] = stock_df["Percentile"].map('{:.0%}'.format)
    stock_df.Manufacturer = stock_df['Manufacturer'].apply(lambda x: x.upper())
    return stock_df

# Builds a dataframe of colors based on the URL 
def color():
    data = pd.read_html("https://en.wikipedia.org/wiki/Car_colour_popularity")
    color_df = data[0]
    colnames = ['Color', 'NA PPG', 'NA DP', 'EU PPG', 'EU DP', 'AP PPG', 'AP DP', 'WORLD PPG', 'WORLD DP']
    color_df.columns = colnames
    color_df.loc[0, 'Color'] = 'White'
    # The dataframe consist of one row for color "Others". 
    # Since we do not have such color in our dataset, nor in "valid" file, we simply drop it.
    color_df.dropna(inplace=True)
    # float to int
    color_df[['NA PPG', 'AP PPG']] = color_df[['NA PPG', 'AP PPG']].astype(int)
    return color_df

# "Car Price Prediction"
# Loads and filters data
def cpp():
    cpp = pd.read_csv('./data/car_price_prediction.csv')
    mfrs = ['Hyundai', 'Toyota', 'Ford', 'Chevrolet']
    MFRS = list(map(lambda x: x.upper(), mfrs))
    years = list(range(2011, 2016))
    cpp_df = cpp[(cpp['Manufacturer'].isin(MFRS)) & (cpp['Prod. year'].isin(years))]
    return cpp_df

# Consumer Confidence Index
# It filters and calculate the values of CCI
# Returns a dataframe
def cci():
    cci = pd.read_csv('./data/CCI.csv')
    cci_years = ['2011-01', '2012-01', '2013-01', '2014-01', '2015-01']
    cci_filtered = cci[(cci['LOCATION'] == 'OECD') & cci.TIME.isin(cci_years)][['TIME', 'Value']].reset_index(drop=True)
    cci_filtered.rename(columns={'TIME': 'Prod. year', 'Value': 'CCI'}, inplace=True)
    # character to int
    for i in range(len(cci_years)):
        cci_filtered.loc[i, 'Prod. year'] = int(cci_years[i][:4])
    return cci_filtered

# Merges the 4 created dataframes
# Outputs a dataframe comparable to "Valid"
def merge(cpp_df, stock_df, color_df, cci_df):
    merge1 = cpp_df.merge(stock_df, how='outer', on=['Manufacturer', 'Prod. year'])
    merge2 = merge1.merge(color_df, how='outer', on='Color')
    merge3 = merge2.merge(cci_df, how='outer', on='Prod. year')
    merge3 = merge3.sort_values('ID').reset_index(drop=True)
    return merge3
