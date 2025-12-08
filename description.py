# import the functions from the .py files and df
from functions import *
from making_df import *

# reference the master df
df = df.drop(['release_date','box_office','run_time','languages','countries','genres'], axis=1)

# a function that gets the description of the movie
def description_search(query,embeds_list,mov_sums,score_list):
    # initialize the query count
    q_count = 0

    # make a list of the words for the query
    querywords = []

    # clean the query
    queryclean = cleanquery(query)
    
    # for each word grab its vector
    for i in range(len(queryclean)):

        # add it to a list
        querywords.append(embeds_list[[i]])
        
        # the count of words in the query
        q_count += 1

        # sum all of the vectors in that list
        v1 = sum(querywords)

        # get an average value
        v1 = v1 / q_count

        # for each cleaned summaries
        for i in range(len(mov_sums)):

            # get the cleaned summary
            summed = mov_sums[i]

            # make the vector of zeros
            v2 = numpy.zeros(300)
            
            # making a counter to get the average value
            counter = 0

            # for each word in the summary
            for words in summed:

                # if it exists, add it to the vector
                if words in embeds_list:
                    v2 += embeds_list[words]
                    counter +=1
            
            # get an average value for the vector
            v2 /= counter

            # add all of the similarity scores to a list
            score_list.append(cosine(v1.flatten(),v2.flatten()))

        # make a whole column in the new df for scores to the user's prompt
        plot_summaries['scores'] = score_list

        # making a new df to sort the scores and titles most similar to the query the user typed in
        sorted_summs = pd.merge(df,plot_summaries,on="wik_mID",how="inner")
        sorted_summs = sorted_summs.sort_values(by='scores', ascending=False)

        only_name = sorted_summs[['name','summary','scores']]
        print(only_name.head(10))

        # clear everything
        querywords.clear()
        score_list.clear()
