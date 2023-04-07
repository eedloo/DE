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
    df = pd.concat([pd.read_csv(file, low_memory=False) for file in glob.glob('./Data/*.csv')])
    return df[df['language'] == 'English'][['content']].dropna().reset_index(drop=True)


def open_politifact():
    '''
    The function opens the only Politifact json file in the Data folder.
    Records in the file are seperated, therefore, we open them as a list of dictionaries.
    all dictionaries have same length and keys.
    The function later output a filtered dataframe built from the list of dictionaries.
    The only columns that are interested here are "verdict" and "statement".

    Input: 
            None
    
    Output:
            A filtered dataframe built upon the json file.

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
    df = pd.DataFrame(data)
    df_filtered = df[['verdict', 'statement']]
    # Correcting verdicts name
    df_filtered.verdict.replace(list(df_filtered.verdict.unique()), 
    ['True', 'False', 'Mostly-True', 'Half-True', 'Pants-on-Fire', 'Mostly-False'], 
    inplace = True)
    return df_filtered

def freq_words(tweets, common_words = 20, use_dumped = True):
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
                The number of desired common words. Default value has been set to 20.
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
    import nltk
    from nltk import word_tokenize, FreqDist
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import stopwords
    
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

def word_selection(common_words, custom_words = True):
    '''
    The function creates a list of words from the common words.
    A pre-defined list has been provided based on the most interesting words among the top 50s.
    A flag is provided if the user wants to use the actual top words.

    Input:
            List of common words with their repeat number as a form of tuples.
    
    Output:
            A list of the top 20 most interesting (or actual words).    
    '''

    if custom_words:
        # The words in this list has been chosen from the top 50 common words as they seemed to be more interesting and relevant.
        list_of_words = ['news', 'world', 'health', 'business', 'realDonaldTrump', 
        'death', 'attack', 'work', 'crime', 'country', 
        'vote', 'state', 'officer', 'money', 'fire', 
        'law', 'police', 'president', 'crash', 'election']
    else:
        list_of_words = [word for i, (word, repeat) in enumerate(common_words)]
    return list_of_words

def counter_match(politifact, list_of_words):
    '''
    The function counts the number of occurance of each words in "list_of_words" on the "politifact" dataframe.
    Workflow:
        $ A list will be created of the same length of the "politifact" dataframe with number of occurance of each word in that statement.
            >>>num_of_repeats[2]
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
          This shows the 12th word in the list ("state") occured once in the statement index row 2. None of the other words has been found.
            >>>politifact.loc[2, 'statement']
            'Says\xa0Maggie Hassan was "out of state on 30 days over the last three months."'
        $ The "politifact" dataframe will be updated with "list_of_words" as new columns and "num_of_repeats" as values.
        $ The number of occurance of each word correcponding to every verdict then will be captured.
            >>>occurance_dic['news']
            {'True': 5,
            'Mostly-True': 4,
            'Half-True': 5,
            'Mostly-False': 8,
            'False': 29,
            'Pants-on-Fire': 11}
          This shows the word "news" observed with this distribution in "politifact" statement column.
        $ An empty dataframe with columns equal to "politifact" dataframe (except for "statement") will be created.
        $ The values of each dictionary then will be added to the output dataframe.
    '''
    list_of_verdicts = ['True', 'Mostly-True', 'Half-True', 'Mostly-False', 'False', 'Pants-on-Fire']
    num_of_repeats = []
    for i in range(len(politifact)):
        num_of_repeats.append([politifact.loc[i, 'statement'].count(word) for word in list_of_words])
    politifact[list_of_words] = num_of_repeats
    occurance_dic = {}
    for word in list_of_words:
        dic = {}
        for verdict in list_of_verdicts:
            dic[verdict] = politifact[politifact['verdict'] == verdict][word].sum()
        occurance_dic[word] = dic
    df = pd.DataFrame(columns=politifact.columns).drop('statement', axis=1)
    df['verdict'] = list_of_verdicts
    for word in list_of_words:
        df[word] = list(occurance_dic[word].values())
    return df
    