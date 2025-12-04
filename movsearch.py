import nltk
import sentiment
import string as s
import pandas as pd
import gensim.downloader as api
from gensim.models.word2vec import Word2Vec
nltk.download('vader_lexicon')
from making_df import *
from mood import *
from description import *
from functions import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
pd.set_option('display.max_colwidth', None)
#pd.reset_option("display.max_rows")

# initialize the count
q_count = 0

# loading the embeddings
embeds = api.load("word2vec-google-news-300")
summaries = plot_summaries['summary'].tolist()

# make a list of plot scores
p_scores = []

description_or_mood = input('Between the two options "description" and "mood" type which one you will use to describe your movie: ')

response = description_or_mood.lower().strip()


# make a list for the cleaned plots
cleansumms = []

# for each summary, clean it and it to a list for training
for s2 in summaries:
    cleansumms.append(cleanfilm(s2))

if response == "description":
    # Loop until the user types 'quit'.
    desc_query = input('Please type a brief description of the movie you would like to watch: ')
    while desc_query != 'quit':
        description_search(desc_query,embeds,cleansumms,p_scores)
        desc_query = input('Please type a brief description of the movie you would like to watch: ')

if response == "mood":
    mood_query = input("Please type in some traits that you look for in a movie (happy, sad, intriguing): ")
    while mood_query != "quit":
        sentiment_search(mood_query,cleansumms,p_scores)
        mood_query = input("Please type in some traits that you look for in a movie (happy, sad, intriguing): ")
