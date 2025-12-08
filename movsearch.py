import nltk
import pandas as pd
import gensim.downloader as api
from description import description_search
from mood import mood_search
from year_pref import compute_year_pref
from making_df import *
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

summaries = plot_summaries['summary'].tolist()
cleansumms = [cleanfilm(s) for s in summaries]

# Ask User Queries
desc_query = input("Describe the type of movie you want (genre): ")
tone_query = input("Describe the mood (happy, sad, intense, etc.): ")
year_query = input("Do you prefer NEW movies or OLD movies? ").lower().strip()


# make a list of plot scores
p_scores = []

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
