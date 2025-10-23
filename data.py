import pandas as pd
# we don't need character meta-data, tvtropes.clusters.txt, or name.clusters.txt
ps_cols = ['wik_mID','summary']
plot_summaries = pd.read_csv('MovieSummaries/plot_summaries.txt', sep="\t", names=ps_cols)

mm_cols = ['wik_mID','fbase_mID','name','release_date','box_office','run_time','languages','countries','genres']
movie_metadata = pd.read_csv('MovieSummaries/movie.metadata.tsv', sep='\t', names =mm_cols)

# remove the freebase movieID
movie_metadata = movie_metadata.drop(['fbase_mID'], axis=1)

# normalize the data
movie_genres = movie_metadata[['wik_mID','genres']]

# need to split the dicts from the genres column into a separate values
# need to the same thing for languages 

# different tables: movies -> ids, dates, info
# genres -> movie id and genres
# language -> movie id and movie language
