import numpy as np
import pandas as pd
import json
import glob

def open_tweets():
    '''
    The function opens all of the Tweets csv files in the Data folder. 
    It concatenate the csv files, filters to select only English tweets,
    and returns the content column. There is only one NaN record on the data,
    and we simply drop that. 

    Input:
            .CSV files in Data folder
    
    Output:
            A cleaned filtered dataframe
    '''
    df = pd.concat([pd.read_csv(file) for file in glob.glob('./Data/*.csv')])
    return df[df['language'] == 'English'][['content']].dropna().reset_index(drop=True)

# Opens json file in Data folder
# Returns a dataframe
def open_politifact():
    '''
    The function opens the only Politifact json file in the Data folder.
    Records in the file are seperated, therefore, we open them as a list of dictionaries.
    all dictionaries have same length and keys.
    The function later output a dataframe built from the list of dictionaries.

    Input: 
            .JSON file in Data folder
    
    Output:
            A dataframe built upon json file

    * Example
    data[1] would be:

    {'verdict': 'false',
    'statement_originator': 'Matt Gaetz',
    'statement': '"Bennie Thompson actively cheer-led riots in the ’90s."',
    'statement_date': '6/7/2022',
    'statement_source': 'television',
    'factchecker': 'Yacob Reyes',
    'factcheck_date': '6/13/2022',
    'factcheck_analysis_link': 'https://www.politifact.com/factchecks/2022/jun/13/matt-gaetz/gaetz-mischaracterizes-bennie-thompsons-stance-rio/'}

    '''
    data = [json.loads(line) for line in open('./Data/politifact_factcheck_data.json', 'r')]
    return pd.DataFrame(data)
