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

@asset(group_name='Input_Data')
def tweets_data() -> DataFrame:
    ''' Aggregates and opens tweets csv files, and returns a dataframe '''
    tweets = functions.open_tweets()
    return tweets

@asset(group_name='Input_Data')
def politifact_data() -> DataFrame:
    ''' Opens politifact json files and returns a dataframe '''
    politifact = functions.open_politifact()
    return politifact

@asset(group_name='Intermediate')
def find_freq_words(tweets_data: DataFrame) -> list:
    ''' Runs a NLP model to extract the most frequent words in tweets '''
    common_words = functions.freq_words(tweets_data)
    return common_words

@asset(group_name='Intermediate')
def make_words_list(find_freq_words: list) -> list:
    ''' Creates a list of most frequent words. (pre-defined or actual) '''
    list_of_words = functions.word_selection(find_freq_words)
    return list_of_words

@asset(group_name='Final')
def make_final_df(politifact_data: DataFrame, make_words_list: list) -> DataFrame:
    ''' Builds the final dataframe '''
    final_df = functions.counter_match(politifact_data, make_words_list)
    return final_df

