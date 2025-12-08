import nltk
import sentiment
import string as s
import pandas as pd
import gensim.downloader as api
from gensim.models.word2vec import Word2Vec
nltk.download('vader_lexicon')
from making_df import *# import the necessary libraries
import nltk
import sentiment
import string as s
import pandas as pd

# download the basics for the word2vec models
import gensim.downloader as api
from gensim.models.word2vec import Word2Vec
nltk.download('vader_lexicon')

# importing the functions that we wrote
from making_df import *
from mood import *
from description import *
from functions import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
pd.set_option('display.max_colwidth', None)
# pd.reset_option("display.max_rows")

# create a custom model for the embeddings
# https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies?resource=download
movsearch_model = Word2Vec(sentences=Msumcleaned,
                           
                           # keep the vector size at 300 and keep them the same
                           vector_size=300,
                           window=5,
                           min_count=5,
                           workers=4,
                           epochs=10)

# grab the word vectors for each word
embeds = movsearch_model.wv

# add all of the summaries to one list
summaries = plot_summaries['summary'].tolist()

# make a list of plot scores
p_scores = []

# prompt the user on whether or not they want to find a movie based on a description or a mood
# a description means you type in: robots take over earth and humans must fight
# a modd for a similar type of movie would mean: dystopian robot human
description_or_mood = input('Between the two options "description" and "mood" type which one you will use to describe your movie: ')

# make the response uniform by getting rid of grammar or casing / sanitation
response = description_or_mood.lower().strip()

# make a list for the cleaned plots
cleansumms = []

# for each summary, clean it and it to a list for training
for s2 in summaries:
    cleansumms.append(cleanfilm(s2))

if response == "description":
    
    desc_query = input('Please type a brief description of the movie you would like to watch: ')
    while desc_query != 'quit':
        description_search(desc_query,embeds,cleansumms,p_scores)
        desc_query = input('Please type a brief description of the movie you would like to watch: ')

if response == "mood":
    mood_query = input("Please type in some traits that you look for in a movie (happy, sad, intriguing): ")
    
    # Loop until the user types 'quit'.
    while mood_query != "quit":
        sentiment_search(mood_query,cleansumms,p_scores)
        mood_query = input("Please type in some traits that you look for in a movie (happy, sad, intriguing): ")
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
