import numpy as np
import pandas as pd
import json
import glob
import re
import pickle

def open_tweets():
    '''
    The function opens all of the Tweets csv files in the Data folder. 
    It concatenate the csv files, filters to select only English tweets,
    and returns the content column. There is only one NaN record on the data,
    and we simply drop that. 

    Input:
            None
    
    Output:
            A cleaned filtered dataframe
    '''
    df = pd.concat([pd.read_csv(file) for file in glob.glob('./Data/*.csv')])
    return df[df['language'] == 'English'][['content']].dropna().reset_index(drop=True)


def open_politifact():
    '''
    The function opens the only Politifact json file in the Data folder.
    Records in the file are seperated, therefore, we open them as a list of dictionaries.
    all dictionaries have same length and keys.
    The function later output a dataframe built from the list of dictionaries.

    Input: 
            None
    
    Output:
            A dataframe built upon the json file

    * Example
    >>> data[1]
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

def freq_words(tweets, common_words = 50, use_dumped = True):
    '''
    The function analyzes the tweets and finds the most common words in that.
    It uses nltk package to lemmatize, find part of speech tags, and number of repeat in the data.
    For tokenization, regex has been used as it was extremely faster than nltk.word_tokenize.
    Two steps of the function is time consuming: lemmatization (~ 5 mins), and finding tags(~ 30 mins).
    The option of using prebuilt lemmatized words and POS tags has been provided via "use_dumped" flag.
    lematized: a list of lemmatized words
    tags: a list of words with corresponding part of speech tag.

    Input:
                Tweets dataframe.
                The number of desired common words. Default value has been set to 50.
                A flag for control of using dumped files. Default value has been set to True.

    Output:     
                A list of desired number of the most common words with their number of repeat in the data.
    
    * Example
    >>> freq_words(tweets, common_words = 20)
    [('http', 1086448),
     ('news', 134138),
     ('sport', 47828),
     ('world', 39678),
     ('year', 36740),
     ('man', 31571),
     ('time', 28523),
     ('woman', 28073),
     ('day', 26096),
     ('life', 22773),
     ('amp', 21832),
     ('workout', 21543),
     ('health', 17127),
     ('business', 16251),
     ('thing', 16034),
     ('realDonaldTrump', 16007),
     ('today', 15690),
     ('way', 14726),
     ('school', 14084),
     ('home', 14015)]
    '''
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    # creating a very long string of all words
    phrase = "\n".join(list(tweets['content']))
    # using regex instead of nltk.word_tokenize
    pattern = re.compile(r'\w+')
    words = pattern.findall(phrase)
    if use_dumped:
        with open("./Data/lematized", "rb") as l:
            lem_words = pickle.load(l)
    else:
        lem_words = [lemmatizer.lemmatize(word) for word in words]
    good_words = [word for word in lem_words if word.casefold() not in stop_words]
    if use_dumped:
        with open("./Data/tags", "rb") as t:
            tags = pickle.load(t)
    else:
        tags = nltk.pos_tag(good_words)
    noun_words = [t[0] for t in tags if t[1] in ('NN','NE') and len(t[0]) > 2]
    distribution = FreqDist(noun_words)
    return distribution.most_common(common_words)