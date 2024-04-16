from textblob import TextBlob
import pandas as pd

# Taking the comment of a survey and seperating the strings out
# Input : takes a string 
# returns a list of strings 
def make_sentences(comment):
    comment_blob = TextBlob(comment)
    return comment_blob.sentences 


# Find the polarity btwn (-1,1) -1 being negative and 1 being positive
# Input : takes a string (a sentence from a comment)
# returns a list of strings 
def find_polarity(sentence):
    return TextBlob(sentence).sentiment.polarity

# for each survey comment, make list of sentences and their survey ID -- survey is the df 
# Input : takes a string (a sentence from a comment)
# returns a tuple of the sentence and the survey ID
def survey_sentences(survey):
    sent = [] # list of tuples 
    for row in survey.index:
        for s in make_sentences(survey['Comments'][row]):
            sent.append((survey['ID'][row] , str(s)))
    return sent

# Determine, based on ratings and polarity scores which surveys are negative and positive add a column with the final categorization 
# Input : a DF of the surveys 
# returns a string that is the overall rating category 
def determine_sentiment(rrow):
    rating_loc = [
        rrow.columns.get_loc('Overall, please rate your most recent experience at Advanced Rad')
        , rrow.columns.get_loc('How would you describe your check-in experience at the office')
        , rrow.columns.get_loc('How would you describe your experience with the technologist')
        , rrow.columns.get_loc('How would you describe your scheduling experience')
        , rrow.columns.get_loc('How likely are you to recommend Advanced Radiology to your friend')]
    ratings = [rrow[index] for index in rating_loc]

    # TRUE if the rating for all 5 questions is above 2
    positive_ratings = all(rating > 2 for rating in ratings)

    polarity_loc = rrow.columns.get_loc('Polarity')
    if rrow[polarity_loc] > 0:
        positive = True
    else : positive = False

    if positive_ratings and positive:
        return "Positive"
    elif positive_ratings != positive:
        return "Negative"
    else :
        return "Very Negative"
