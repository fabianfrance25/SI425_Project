import sentiment
import pandas as pd
from functions import *
from making_df import *

df = df.drop(['release_date','box_office','run_time','languages','countries','genres'], axis=1)
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

        # add all of the similarity scores to a list
        score_list.append(cosine(v1,v2))

    # make a whole column in the new df for scores to the user's prompt
    plot_summaries['scores'] = score_list

    
    sorted_summs = pd.merge(df,plot_summaries,on="wik_mID",how="inner")
    sorted_summs = sorted_summs.sort_values(by='scores', ascending=False)
    only_name = sorted_summs[['name','summary','scores']]
    print(only_name.head(10))

    # clear everything
    querywords = ""
    score_list.clear()
