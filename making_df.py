# need to install in word2vec env
import pandas as pd
import string as s
import ast
import io
from functions import *

# we don't need character meta-data, tvtropes.clusters.txt, or name.clusters.txt
ps_cols = ['wik_mID','summary']
plot_summaries = pd.read_csv('MovieSummaries/plot_summaries.txt', sep="\t", names=ps_cols)

# initialize the column names for movies
mm_cols = ['wik_mID','fbase_mID','name','release_date','box_office','run_time','languages','countries','genres']

# read the df
df = pd.read_csv('MovieSummaries/movie.metadata.tsv', sep='\t', names =mm_cols)

# remove the freebase movieID and use fillna(0) to fill the values to be 0
df = df.drop(['fbase_mID'], axis=1)
df = df.fillna(0)

# Gemini was used to make the DF workable
# BELOW THIS LINE IS ALL GEMINI CODE
# --- 1. Define the parsing function (same as before) ---
def get_values_from_string(cell_str):
    if pd.isna(cell_str):
        return []
    try:
        data_dict = ast.literal_eval(cell_str)
        if isinstance(data_dict, dict):
            return list(data_dict.values())
        else:
            return []
    except (ValueError, SyntaxError, TypeError):
        return []

# --- 2. Apply the function to create new "list" columns ---
# We add these directly to the original DataFrame 'df'
df['countries_names'] = df['countries'].apply(get_values_from_string)
df['languages_names'] = df['languages'].apply(get_values_from_string)
df['genres_names'] = df['genres'].apply(get_values_from_string)

# --- 3. "Explode" each list column sequentially ---
# The other columns (name, release_date, etc.)
# will be automatically duplicated.
df_exploded = df.explode('countries_names')
df_exploded = df_exploded.explode('languages_names')
df_exploded = df_exploded.explode('genres_names')

# --- 4. Clean up the final DataFrame ---
# Drop the original string-based columns, as we don't need them
final_df = df_exploded.drop(columns=['countries', 'languages', 'genres'])

# Reset the index and keep the original index for referenceMovieSummaries/
final_df = final_df.reset_index()
final_df = final_df.rename(columns={'index': 'original_index'})

# END of Gemini Code
