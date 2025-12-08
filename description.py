from functions import *
from making_df import *

df = df.drop(['release_date','box_office','run_time','languages','countries','genres'], axis=1)

def description_search(query, embeds_list, mov_sums, score_list):
    global q_count

    # clean + tokenize
    queryclean = cleanquery(query)

    # build query embedding
    query_vec = numpy.zeros(300)
    count = 0

    for word in queryclean:
        if word in embeds_list:
            query_vec += embeds_list[word]
            count += 1
    
    if count == 0:
        print("No valid words found in description.")
        return
    
    query_vec /= count

    # compute similarity with each movie
    score_list.clear()

    for summary_words in mov_sums:
        v2 = numpy.zeros(300)
        counter = 0

        for w in summary_words:
            if w in embeds_list:
                v2 += embeds_list[w]
                counter += 1

        if counter > 0:
            v2 /= counter
            sim = cosine(query_vec.flatten(), v2.flatten())
        else:
            sim = 0
        
        score_list.append(sim)

    # save to dataframe
    plot_summaries['scores'] = score_list

    sorted_summs = pd.merge(df, plot_summaries, on="wik_mID", how="inner")
    sorted_summs = sorted_summs.sort_values(by='scores', ascending=False)
    only_name = sorted_summs[['name','summary','scores']]
    print(only_name.head(10))