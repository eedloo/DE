import numpy as np
import pandas as pd
pd.set_option('display.precision', 10)

# Load data
df = pd.read_excel(r'D:\SLU\AI MSc\Repos\DE\project2\data\car_stocks.xlsx')

# List of Makers
mfrs = list(df.Manufacturer.unique())

# List of production years
years = list(range(2011, 2016))

# Extract starting and ending prices of each year, and calculate percent changes for each manufacturer
# Return a dictionary with company's name as keys and extracted values of each year as values
def extract(dataframe):
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

# Calculate "Median Percent Changes For Year"
# The extract function's output dictionary is the input
# Returns a dictionary with years of keys and median percent changes for that year as values
def mchange(data):
    pchfy = {}
    for i in years:
        pch = []
        for j in mfrs:
            pch.append(data[j][i][2])
        pchfy[i] = np.median(pch)
    return pchfy

# Aggregate results from extract and mchange functions
# Return nested list of required values
# Make the data ready to build the stocks dataframe
def agg(dic, pchfy):
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

# Build a dataframe with extracted and generated values
# Return stocks dataframe
def make_df(data):
    colnames = [
        'Manufacturer', 
        'Year', 
        'Starting', 
        'Ending', 
        'Pct Change', 
        'Distance from Med'
        ]
    stock_df = pd.DataFrame(columns= colnames, data=data)
    stock_df.replace(-0, 0, inplace=True)
    stock_df.loc[:, "Pct Change"] = stock_df["Pct Change"].map('{:.0%}'.format)
    stock_df.loc[:, "Distance from Med"] = stock_df["Distance from Med"].map('{:.0%}'.format)
    return stock_df

def stock_df():
    dic = extract(df)
    pchfy = mchange(dic)
    data = agg(dic, pchfy)
    make_df(data)