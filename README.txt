# SI425_Project
1. Dataset Status:
    Our data is from https://www.cs.cmu.edu/~ark/personas/. The data is around 75 MB, but currently we are trying to truncate it and then put it into proper 2nd and 3rd Normal form so we can use it better. 
2. Plan going forward:
    As explained in our previous email, we plan to prompt the user to give a description of the movie they'd like to watch. Using that response, we can break it up into a couple of features that we will eventually use in our model. First we will just use the embeddings of the input and compare them to the embeddings of the plot summary to give us a score based on how similar the description is to movies in our dataset. Secondly, we will use sentiment. We will use it to get a sense of the tone of the movie, such as dark or romantic. Then we have characteristics about movies such as year. For example, if they say they want a classic movie we may use an older movie. Additionally, to give back good movies we can use box office revenue as a boost to pick that movie. As of now these are the main features we plan to use in a model to determine which movies to recommend to the user.


3. Group Member Duties:
    Addison-
    Fabian-
    Mike- 