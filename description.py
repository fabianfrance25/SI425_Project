import numpy as np
import pandas as pd
from functions import *
from making_df import *

df = df.drop(['box_office','run_time','languages','countries','genres'], axis=1)

def description_search(query, embeds, mov_sums):

    # clean the initial query
    query_clean = cleanquery(query)
    
    # Build query embedding
    q_vec = np.zeros(300)
    
    count = 0

    # make the user input vector and add a count
    # before averaging it to balance the weight of
    # shorter queries and longer ones
    # prevents vectors that are too big
    for word in query_clean:
        if word in embeds:
            q_vec += embeds[word]
            count += 1
    if count > 0:
        q_vec /= count

    # make a list of description scores
    desc_scores = []

    for summary in mov_sums:

        # make another blank vector
        s_vec = np.zeros(300)

        # initialize the count
        s_count = 0
        for word in summary:
            if word in embeds:

                # make the word vectors from each plot
                s_vec += embeds[word]
                s_count += 1
        
        # get the average to eliminate bias
        if s_count > 0:
            s_vec /= s_count
        
        # calculate cosine distance to get a score
        desc_scores.append(cosine(q_vec, s_vec))

    # return the recommendation
    results = plot_summaries.copy()
    results["desc_sim"] = desc_scores
    return results
