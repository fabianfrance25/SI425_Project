# need to install in word2vec env
import pandas as pd
import gensim.downloader as api
import string as s
import sentiment
from gensim.models.word2vec import Word2Vec
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# function to get the cosine distance
def cosine(vA, vB):
    ''' Returns the cosine similarity of two numpy ndarray objects. '''
    dot = numpy.dot(vA, vB)
    A = numpy.sqrt(numpy.dot(vA,vA))
    B = numpy.sqrt(numpy.dot(vB,vB))

    # kept getting a runtim error so I coded it this way, the math is fine
    if A * B == 0:
        return 0
    
    else:
        return dot / (A*B)

# the clean function to get rid of the filter words from the query
def cleanquery(summary):
# clean the summary by making it all lowercase
# getting rid of any unnecessary characters before splitting into a list
    cleansum = []
    summary = summary.lower()
    summary = summary.strip()
    summary = summary.split()

    stopwords = ['movie','about','the','at','and','if','but','a','is','film']
 # for each word in the summary if punctuation in the summary, replace it with nothing
    for words in summary:
        for punc in s.punctuation:
            if punc in words:
                words = words.replace(punc,'')
        
        for stop in stopwords:
            if stop == words:
                words = words.replace(stop,'')   
        # add the words to the summary
        cleansum.append(words)

    # return the cleaned summary
    return cleansum

# the normal clean function
def cleanfilm(summary):
# clean the summary by making it all lowercase
# getting rid of any unnecessary characters before splitting into a list
    cleansum = []
    summary = summary.lower()
    summary = summary.strip()
    summary = summary.split()

 # for each word in the summary if punctuation in the summary, replace it with nothing
    for words in summary:
        for punc in s.punctuation:
            if punc in words:
                words = words.replace(punc,'')

        # add the words to the summary
        cleansum.append(words)

    # return the cleaned summary
    return cleansum

# we don't need character meta-data, tvtropes.clusters.txt, or name.clusters.txt
ps_cols = ['wik_mID','summary']
plot_summaries = pd.read_csv('plot_summaries.txt', sep="\t", names=ps_cols)

# initialize the column names for movies
mm_cols = ['wik_mID','fbase_mID','name','release_date','box_office','run_time','languages','countries','genres']

# read the df
df = pd.read_csv('movie.metadata.tsv', sep='\t', names =mm_cols)

# remove the freebase movieID and use fillna(0) to fill the values to be 0
df = df.drop(['fbase_mID'], axis=1)
df = df.fillna(0)

# Gemini was used to make the DF workable
# BELOW THIS LINE IS ALL GEMINI CODE
# --- 1. Define the parsing function (same as before) ---
import ast
import io
import numpy

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

# Reset the index and keep the original index for reference
final_df = final_df.reset_index()
final_df = final_df.rename(columns={'index': 'original_index'})

# END of Gemini Code

# initialize the count
q_count = 0

# loading the embeddings
embeds = api.load("word2vec-google-news-300")
summaries = plot_summaries['summary'].tolist()

# make a list of plot scores
p_scores = []

# make a merged dataframe with the movie name to each ID
plot_summaries = pd.merge(plot_summaries, df[['wik_mID', 'name']], on='wik_mID', how='left')

plot_or_mood = input('Between the two options "description" and "mood" type which one you will use to describe your movie: ')
response = plot_or_mood.lower().strip()

if response == "description":
    # Loop until the user types 'quit'.
    query = input('Please type a brief description of the movie you would like to watch: ')

    # make a list for the cleaned plots
    cleansumms = []

    # for each summary, clean it and it to a list for training
    for s2 in summaries:
        cleansumms.append(cleanfilm(s2))

    # until the user types quit
    while query != 'quit':

        # make a list of the words for the query
        querywords = []
        queryclean = cleanquery(query)
    
        # for each word grab its vector
        for i in range(len(queryclean)):

            # add it to a list
            querywords.append(embeds[[i]])
            q_count += 1

        # sum all of the vectors in that list
        v1 = sum(querywords)
        v1 = v1 / q_count
        # for each cleaned summaries
        for i in range(len(cleansumms)):

            # get the cleaned summary
            summed = cleansumms[i]

            # make the vector of zeros
            v2 = numpy.zeros(300)
            
            # making a counter to get the average value
            counter = 0

            # for each word in the summary
            for words in summed:

                # if it exists, add it to the vector
                if words in embeds:
                    v2 += embeds[words]
                    counter +=1
            
            # get an average value for the vector
            v2 /= counter

            # add all of the similarity scores to a list
            p_scores.append(cosine(v1.flatten(),v2.flatten()))

        # make a whole column in the new df for scores to the user's prompt
        plot_summaries['scores'] = p_scores

        # sort them from highest score to lowest
        sorted_summs = plot_summaries.sort_values(by='scores', ascending=False)

        # print them out
        print(sorted_summs['name'].head(10))

        # clear everything
        querywords.clear()
        p_scores.clear()
        query = input('Please type a brief description of the movie you would like to watch: ')

if response == "mood":
    moods = input("Please type in some traits that you look for in a movie (happy, sad, intriguing): ")

    # make a list for the cleaned plots
    cleansumms = []

    # for each summary, clean it and it to a list for training
    for s2 in summaries:
        cleansumms.append(cleanfilm(s2))

    # until the user types quit
    while moods != 'quit':

        # make a list of the words for the query
        queryclean = cleanquery(moods)

        querywords = " ".join(queryclean)

        # sum all of the vectors in that list
        v1 = sentiment.get_sentiment(querywords)

        # for each cleaned summaries
        for i in range(len(cleansumms)):

            # get the cleaned summary
            summed = cleansumms[i]

            # make the vector of zeros
            sumwords = []

            # for each word in the summary
            for words in summed:
                    sumwords.append(words)
            
            # get an average value for the vector
            text = " ".join(sumwords)

            v2 = sentiment.get_sentiment(text)

            # add all of the similarity scores to a list
            p_scores.append(cosine(v1,v2))

        # make a whole column in the new df for scores to the user's prompt
        plot_summaries['scores'] = p_scores

        # sort them from highest score to lowest
        sorted_summs = plot_summaries.sort_values(by='scores', ascending=False)

        # print them out
        print(sorted_summs['name'].head(10))

        # clear everything
        querywords = ""
        p_scores.clear()
        moods = input("Please type in some traits that you look for in a movie (happy, sad, intriguing)")

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
df['box_norm'] = scaler.fit_transform(df[['box_office']])
sid = SentimentIntensityAnalyzer()

def get_sentiment(summary):
    # takes in movie and returns a number between -1 and 1 representing the sentiment of the text
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(summary)
    compound_score = scores['compound']
    return compound_score

alpha = 0.3  # tweakable
plot_summaries['sentiment_adjusted'] = (
    plot_summaries['sentiment'] + alpha * plot_summaries['box_norm'])
