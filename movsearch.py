import nltk
import pandas as pd
from description import description_search
from mood import mood_search
from making_df import *
from functions import *
from gensim.models.word2vec import Word2Vec

nltk.download('vader_lexicon')
pd.set_option('display.max_colwidth', None)

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

# lists of all the weights
genrelist = ['Romance', 'Comedy', 'Musical', 'Family', 'Animation', 'Drama', 'Biographical film', 'History', 'Documentary', 'Adventure', 'Sports', 'Short Film', 'Western', 'Anime', 'Japanese Movies', 'Action', 'Science Fiction', 'Crime Fiction', 'Crime Drama', 'Mystery', 'Supernatural', 'Space western', 'Thriller', 'Horror', 'War']
moodlist = ['happy', 'joy', 'funny', 'sad', 'dark', 'intense', 'exciting', 'romantic', 'scary', 'action']

# a grabs all of the plot summaries and cleans them as input for the recommender
summaries = plot_summaries['summary'].tolist()
cleansumms = [cleanfilm(s) for s in summaries]

# ask the user for input given a desired genre, mood, and a current or older movie
print(f'Here are the different genres you can pick from: {genrelist}\n')
desc_query = input("Describe the type of movie you want (genre): ")

print(f'Here are the different moods you can pick from: {moodlist}\n')
tone_query = input("Describe the mood (happy, sad, intense, etc.): ")

year_query = input("Do you prefer NEW movies or OLD movies? ").lower().strip()

# computing the feature scores for each input
desc_df = description_search(desc_query, embeds, cleansumms)  
mood_df = mood_search(tone_query, cleansumms)               

# merging them
merged = desc_df.merge(mood_df[['wik_mID','mood_score']], on='wik_mID')

# Mmerging them to the original metadata
merged = merged.merge(df[['wik_mID','name','release_date']], on='wik_mID', how='left')
merged['year'] = pd.to_datetime(merged['release_date'], errors='coerce').dt.year

# computing the year preferance
merged = compute_year_pref(merged, year_query)  # adds 'year_sim'

# adjustable weights for our own funciton
W_DESC = 0.5
W_SENT = 0.3  
W_YEAR = 0.2

# producing the final score given the weights
merged["final_score"] = (
    W_DESC * merged["desc_sim"] +
    W_SENT * merged["mood_score"] +
    W_YEAR * merged["year_sim"]
)

# sort and display the recommendations
merged = merged.sort_values(by="final_score", ascending=False)
print("\nTop 10 Recommended Movies:\n")
print(merged[['name','summary','final_score']].head(10))
