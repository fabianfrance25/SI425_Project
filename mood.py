import sentiment
import pandas as pd
from functions import *
from making_df import *
pd.set_option('display.max_colwidth', None)
#pd.reset_option("display.max_rows")

df = df.drop(['release_date','box_office','run_time','languages','countries','genres'], axis=1)

# made by Gemini AI
GENRE_SENTIMENT_MAP = {
    # HIGHLY POSITIVE (+0.6 to +1.0)
    'Romance': 1.0, 
    'Comedy': 0.8, 
    'Musical': 0.7, 
    'Family': 0.9,
    'Animation': 0.6,
    
    # MODERATE/NEUTRAL (0.0 to +0.5)
    'Drama': 0.0,
    'Biographical film': 0.2,
    'History': 0.1,
    'Documentary': 0.3,
    'Adventure': 0.4,
    'Sports': 0.5,
    'Short Film': 0.1,
    'Western': 0.0,
    'Anime': 0.3, # Depending on content, often neutral
    'Japanese Movies': 0.0, # Neutral category
    
    # NEGATIVE/DARK/THEMATIC (-0.2 to -1.0)
    'Action': -0.2,
    'Science Fiction': -0.3, # Often thematic/dark
    'Crime Fiction': -0.4,
    'Crime Drama': -0.5,
    'Mystery': -0.6,
    'Supernatural': -0.7,
    'Space western': -0.5,
    'Thriller': -1.0, 
    'Horror': -1.0, 
    'War': -0.9,
}

# Gemini AI Code
def get_genre_target_score(movie_genres):
    """Calculates a single sentiment score for a movie based on its genres."""
    score = 0.0
    count = 0
    for genre in movie_genres:
        if genre in GENRE_SENTIMENT_MAP:
            score += GENRE_SENTIMENT_MAP[genre]
            count += 1
    # Return the average genre score (or 0 if no mapped genres are found)
    return score / count if count > 0 else 0.0

def mood_search(query, mov_sums):
    score_list = []

    query_clean = cleanquery(query)
    query_text = " ".join(query_clean)

    MOOD_MAP = {
        'happy': 1.0, 'joy': 0.9, 'funny': 0.8,
        'sad': -0.8, 'dark': -0.9, 'intense': -0.5,
        'exciting': 0.7, 'romantic': 1.0, 'scary': -1.0,
        'action': -0.3,
    }

    v1 = sum([MOOD_MAP.get(w,0) for w in query_clean])
    v1 = v1 / len(query_clean) if query_clean else 0.0

    for i, summary in enumerate(mov_sums):
        text = " ".join(summary)
        v2 = sum([MOOD_MAP.get(w,0) for w in summary])
        v2 = v2 / len(summary) if summary else 0.0

        # text match
        text_match_score = 1.0 - abs(v1 - v2)

        # genre alignment
        try:
            movie_id = plot_summaries.loc[i,'wik_mID']
            movie_genres = final_df[final_df['wik_mID']==movie_id]['genres_names'].unique().tolist()
            target_score = get_genre_target_score(movie_genres)
            genre_alignment_score = 1.0 - abs(v1 - target_score)
        except:
            genre_alignment_score = 0.0

        final_score = (0.4*text_match_score) + (0.6*genre_alignment_score)
        score_list.append(final_score)

    # return as a DataFrame
    mood_df = plot_summaries.copy()
    mood_df['mood_score'] = score_list
    mood_df['wik_mID'] = plot_summaries['wik_mID']

    return mood_df
