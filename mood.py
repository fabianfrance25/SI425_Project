# import the necessary functions and libraries
import sentiment
import pandas as pd
from functions import *
from making_df import *
pd.set_option('display.max_colwidth', None)
#pd.reset_option("display.max_rows")

# initialize the master df
df = df.drop(['release_date','box_office','run_time','languages','countries','genres'], axis=1)

# made by Gemini AI
# We had an idea to use genres as weights, but ran out of time to implement it
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
    # Gemini AI Code end
    
def sentiment_search(query,mov_sums,score_list):
    # make a list of the words for the query
    queryclean = cleanquery(query)

    querywords = " ".join(queryclean)

    # sum all of the vectors in that list
    v1 = sentiment.get_sentiment(querywords)

    # for each cleaned summaries
    for i in range(len(mov_sums)):

        # get the cleaned summary
        summed = mov_sums[i]

            
        # get an average value for the vector
        text = " ".join(summed)

        v2 = sentiment.get_sentiment(text)

        # Gemini AI Code
        text_match_score = 1.0 - abs(v1 - v2)

        try:
            # Assuming plot_summaries and final_df can be linked via wik_mID
            movie_id = plot_summaries.loc[i, 'wik_mID']
            # Get all unique genre names for this movie ID
            movie_genres = final_df[final_df['wik_mID'] == movie_id]['genres_names'].unique().tolist()
            
            target_score = get_genre_target_score(movie_genres)
            
            # Critical alignment calculation: small distance = high score
            genre_alignment_score = 1.0 - abs(v1 - target_score)
        
        except Exception:
            # Safely handle missing ID/data
            genre_alignment_score = 0.0

        final_score = (0.4 * text_match_score) + (0.6 * genre_alignment_score)
        
        score_list.append(final_score)
    
    # Gemini AI Code end
    # make a whole column in the new df for scores to the user's prompt
    plot_summaries['scores'] = score_list

    sorted_summs = pd.merge(df,plot_summaries,on="wik_mID",how="inner")
    sorted_summs = sorted_summs.sort_values(by='scores', ascending=False)
    only_name = sorted_summs[['name','summary','scores']]
    print(only_name.head(10))

    # clear everything
    querywords = ""
    score_list.clear()
