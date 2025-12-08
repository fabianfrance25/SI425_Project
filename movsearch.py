<<<<<<< HEAD
import nltk
import pandas as pd
import gensim.downloader as api
from description import description_search
from mood import mood_search
from year_pref import compute_year_pref
from making_df import df, plot_summaries, cleanfilm

nltk.download('vader_lexicon')
=======
# import the necessary libraries
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
>>>>>>> 83a35124526a365c9291a2a625b9af67be1536aa
pd.set_option('display.max_colwidth', None)

<<<<<<< HEAD
embeds = api.load("word2vec-google-news-300")

summaries = plot_summaries['summary'].tolist()
cleansumms = [cleanfilm(s) for s in summaries]

# Ask User Queries
desc_query = input("Describe the type of movie you want: ")
tone_query = input("Describe the mood (happy, sad, intense, etc.): ")
year_query = input("Do you prefer NEW movies or OLD movies? ").lower().strip()

# Compute Feature Scores
desc_df = description_search(desc_query, embeds, cleansumms)  
mood_df = mood_search(tone_query, cleansumms)               

# Merge Scores
merged = desc_df.merge(mood_df[['wik_mID','mood_score']], on='wik_mID')

# Merge Original Metadata
merged = merged.merge(df[['wik_mID','name','release_date']], on='wik_mID', how='left')
merged['year'] = pd.to_datetime(merged['release_date'], errors='coerce').dt.year

# Year preference
merged = compute_year_pref(merged, year_query)  # adds 'year_sim'

# Weighted Final Ranking
W_DESC = 0.6
W_SENT = 0.3  
W_YEAR = 0.1

merged["final_score"] = (
    W_DESC * merged["desc_sim"] +
    W_SENT * merged["mood_score"] +
    W_YEAR * merged["year_sim"]
)

# Sort and Display 
merged = merged.sort_values(by="final_score", ascending=False)
print("\nTop 10 Recommended Movies:\n")
print(merged[['name','summary','final_score']].head(10))
=======
# create a custom model for the embeddings
# https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies?resource=download
movsearch_model = Word2Vec(sentences=Msumcleaned,
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
# a mood for a similar type of movie would mean: dystopian robot human
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
>>>>>>> 83a35124526a365c9291a2a625b9af67be1536aa
