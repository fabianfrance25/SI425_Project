import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from making_df import *

sid = SentimentIntensityAnalyzer()

def sentiment_search(query, mov_sums):
    q_sent = sid.polarity_scores(query)["compound"]
    sent_scores = []

    for summary in mov_sums:
        text = " ".join(summary)
        s_sent = sid.polarity_scores(text)["compound"]
        diff = 1 - abs(q_sent - s_sent)
        sent_scores.append(diff)

    results = plot_summaries.copy()
    results["sent_sim"] = sent_scores
    return results
