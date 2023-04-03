import numpy as np
import pandas as pd
import json
import os
import glob

# Opens csv files in Data folder and concatenate them
# Filter on English tweets and select the necessary feature (content)
# Returns a dataframe
def open_tweets():
    df = pd.concat([pd.read_csv(file) for file in glob.glob('./Data/*.csv')])
    return df[df['language'] == 'English'][['content']]

# Opens json file in Data folder
# Returns a dataframe
def open_politifact():
    for file in glob.glob('./Data/*.json'):
        data = [json.loads(line) for line in open(file, 'r')]
        return pd.DataFrame(data)