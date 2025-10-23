# SI425_Project
1. Dataset Status:
    Our data is from https://www.cs.cmu.edu/~ark/personas/. The data is around 75 MB, but currently we are trying to truncate it and then put it into proper 2nd and 3rd Normal form so we can use it better. 
2. Plan going forward:
    As explained in our previous email, we plan to prompt the user to give a description of the movie they'd like to watch. Using that response, we can break it up into a couple of features that we will eventually use in our model. First we will just use the embeddings of the input and compare them to the embeddings of the plot summary to give us a score based on how similar the description is to movies in our dataset. Secondly, we will use sentiment. We will use it to get a sense of the tone of the movie, such as dark or romantic. Then we have characteristics about movies such as year. For example, if they say they want a classic movie we may use an older movie. Additionally, to give back good movies we can use box office revenue as a boost to pick that movie. As of now these are the main features we plan to use in a model to determine which movies to recommend to the user.


3. Group Member Duties:
    Addison- Will do the embeddings of plot summaries and the input and find good comparisons. Also find how to use embeddings of count for era of movies such as classics, new, etc.

    Fabian- Will find a source online that labels sentiment similar to lab in which we used lexicons. Then he will label the input lexicon and each of the movies. Then compare scores so they are similar. This won't just label if they are positive or negative but we will judge based on distance from each other. Additionally, look how to give a positive boost in the model to the movies with higher box office revenue.

    Mike- Will handle most of the initial cleaning of the data. He will get it into normal forms in which we can work in. Finally, he will work on the taking the features we worked with and finding good models that might work for this type of problem. 