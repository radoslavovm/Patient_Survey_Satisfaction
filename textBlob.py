from textblob import TextBlob
from connection import engine
import pandas as pd

"""
# fetch all makes a list of rows and rows are pyodbc objects that are tuple like. Can access columns using the colomn name or the index (rows.Comments)
ttest = cursor.execute("SELECT top 100 * FROM [dbo].[Patient_Satisfaction_Survey] WHERE Comments != ''")
rows = ttest.fetchall()
print(rows)

ids = [] , comments = [] , overall = [] ,checkin = [] ,tech = [] ,sched = [] 
#"Overall, please rate your most recent experience at Advanced Rad" 
overall_exp = 2
# 'How would you describe your check-in experience at the office' 
check_in = 3
# 'How would you describe your experience with the technologist' 
tech_exp = 4
# 'How would you describe your scheduling experience' 
sched_exp  = 5

    ids.append(row.ID)
    comments.append(row.Comments)
    overall.append(row[overall_exp])
    checkin.append(row[check_in])
    tech.append(row[tech_exp])
    sched.append(row[sched_exp])

data = {
    'ID' : ids
    ,'overall' : overall
    , 'check-in' : checkin
    , 'technologist' : tech
    , 'scheduling' : sched
    , 'Comment' : comments
    , 'Polarity' : polarity
}

df = pd.DataFrame(data)

comment = TextBlob(row.Comments)
polarity.append(comment.sentiment.polarity)
"""

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
def determine_sentiment(r):
    rating_loc = [
        r.columns.get_loc('Overall, please rate your most recent experience at Advanced Rad')
        , r.columns.get_loc('How would you describe your check-in experience at the office')
        , r.columns.get_loc('How would you describe your experience with the technologist')
        , r.columns.get_loc('How would you describe your scheduling experience')
        , r.columns.get_loc('How likely are you to recommend Advanced Radiology to your friend')]
    ratings = [r[index] for index in rating_loc]

    positive_ratings = all(rating > 2 for rating in ratings)

    polarity_loc = r.columns.get_loc('Polarity')
    if r[polarity_loc] > 0:
        positive = True
    else : positive = False

    if positive_ratings and positive:
        return "Positive"
    elif positive_ratings != positive:
        return "Negative"
    else :
        return "Very Negative"
