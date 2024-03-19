from textblob import TextBlob
#from connection import cursor
from connection import engine
import pandas as pd
# importing the modules
from IPython.display import display

# Query the survey's that do have a commment. 
df = pd.read_sql("SELECT top 500 * FROM [dbo].[Patient_Satisfaction_Survey] WHERE Comments != ''", engine)

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
# Input :takes a string 
# returns a list of strings 
def make_sentences(comment):
    comment_blob = TextBlob(comment)
    return comment_blob.sentences 

# Find the polarity btwn (-1,1) -1 being negative and 1 being positive
def find_polarity(comment):
    return comment.sentiment.polarity

# Add the Polarity to the dataframe 
# df["Polarity"] = df['Comments'].map(find_polarity)

# make list of surveys and their sentences -- survey is the df 
def survey_sentences(survey):
    sent = [] # list of tuples 
    for row in survey.index:
        for s in make_sentences(survey['Comments'][row]):
            sent.append((survey['ID'][row] , s))
    return sent

data = survey_sentences(df)
# Create new DF with the ID of the survey and the polarity scores of the sentences 
polarity_df = pd.DataFrame(data , columns = ['ID', 'Sentences'])
polarity_df["Polarity"] = polarity_df['Sentences'].map(find_polarity)

# Determine, based on ratings and polarity scores which surveys are negative and positive
# add a column with the final categorization 

def determine_sentiment(r):
    rating_loc = [
        df.columns.get_loc('Overall, please rate your most recent experience at Advanced Rad')
        , df.columns.get_loc('How would you describe your check-in experience at the office')
        , df.columns.get_loc('How would you describe your experience with the technologist')
        , df.columns.get_loc('How would you describe your scheduling experience')
        , df.columns.get_loc('How likely are you to recommend Advanced Radiology to your friend')]
    ratings = [r[index] for index in rating_loc]

    positive_ratings = all(rating > 2 for rating in ratings)

    polarity_loc = df.columns.get_loc('Polarity')
    if r[polarity_loc] > 0:
        positive = True
    else : positive = False

    if positive_ratings and positive:
        return "Positive"
    elif positive_ratings != positive:
        return "Negative"
    else :
        return "Very Negative"

df['Final_Rating'] = df.apply(determine_sentiment, axis=1)

display(df.groupby('Final_Rating').count())

# df.query('Final_Rating' == 'Very Negative' and 'Polarity' )

df.count()

# df.to_csv("patient_satisfaction.csv")

# can change if_exists to append, and add in a date feature to minimize processing power
# df.to_sql("PatientSatisfactionSurveyScores", engine, if_exists='replace')

# what Names are assoc with negative/positive score
# what are the ratio of scores for each office 

