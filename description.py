import numpy as np
import pandas as pd
from functions import *
from making_df import *
from gensim.models import KeyedVectors

df = df.drop(['box_office','run_time','languages','countries','genres'], axis=1)

def description_search(query, embeds, mov_sums):
    query_clean = cleanquery(query)
    
    # Build query embedding
    q_vec = np.zeros(300)
    count = 0
    for word in query_clean:
        if word in embeds:
            q_vec += embeds[word]
            count += 1
    if count > 0:
        q_vec /= count

    desc_scores = []

    for summary in mov_sums:
        s_vec = np.zeros(300)
        s_count = 0
        for word in summary:
            if word in embeds:
                s_vec += embeds[word]
                s_count += 1
        if s_count > 0:
            s_vec /= s_count
        desc_scores.append(cosine(q_vec, s_vec))

    # only change was to make plot_summaries instead of df
    results = plot_summaries.copy()
    results["desc_sim"] = desc_scores
    return results