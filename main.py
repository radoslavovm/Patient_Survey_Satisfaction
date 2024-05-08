import connection as conn
import textBlob as tb
import pandas as pd
import traceback

def main():
    sql = """
    SELECT * 
    FROM [dbo].[Patient_Satisfaction_Survey] 
    WHERE Comments != ''
    """
    # Query the survey's that do have a commment. 
    df = pd.read_sql(sql, conn.engine).set_index('ID').drop_duplicates()

    # data is a list of the survey sentences and their IDs
    data = tb.survey_sentences(df)
    

    # Create new DF with the ID of the survey and the polarity scores of the sentences 
    polarity_df = pd.DataFrame(data , columns = ['ID', 'Sentences'])
    polarity_df["Polarity"] = polarity_df['Sentences'].map(tb.find_polarity)
    
    #result = polarity_df.join(df, on='ID')
    #result["Overall_Sentiment"] = result.map(tb.determine_sentiment(result)) 
    
    #polarity_df.to_csv("patient_satisfaction.csv") ## Output resulting dataframe in a csv

    # can change if_exists to append, and add in a date feature to minimize processing power
    polarity_df.to_sql("PatientSatisfactionSurveyScores", conn.engine, if_exists='replace')

    sql_test = """
    SELECT TOP 10 * 
    FROM [dbo].[PatientSatisfactionSurveyScores]
    """
    
    print(pd.read_sql(sql_test, conn.engine))

if __name__ == '__main__':
    try:
        main()
        print("job complete")
    
    except Exception as e:
        with open("exceptions.txt", 'a') as logfile:
            traceback.print_exc(file=logfile)