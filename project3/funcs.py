import numpy as np
import pandas as pd
import json
import os
import glob

# Opens files in Data folder
# Returns a dataframe per files
def open_asdf():
    for file in glob.glob('./Data/*'):
        if file[-5:] == '.json':
            data = [json.loads(line) for line in open(file, 'r')]
            politifact = pd.DataFrame(data)
        if file[-4:] == '.csv':
            data = pd.read_csv(file)
            tweets = pd.DataFrame(data)
    return politifact, tweets