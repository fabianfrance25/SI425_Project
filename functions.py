import numpy
import string as s

# function to get the cosine distance
def cosine(vA, vB):
    ''' Returns the cosine similarity of two numpy ndarray objects. '''
    dot = numpy.dot(vA, vB)
    A = numpy.sqrt(numpy.dot(vA,vA))
    B = numpy.sqrt(numpy.dot(vB,vB))

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

def compute_year_pref(df, preference):
    target_year = 2025 if preference == "new" else 1950

    df["year_sim"] = 1 - abs(df["year"] - target_year) / 40
    df["year_sim"] = df["year_sim"].clip(0, 1)
    return df
