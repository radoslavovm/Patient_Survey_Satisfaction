import connection as conn
import textBlob as tb
import pandas as pd

def main():
    sql = """
    SELECT TOP 10 * 
    FROM [dbo].[Patient_Satisfaction_Survey] 
    WHERE Comments != ''
    """
    # Query the survey's that do have a commment. 
    df = pd.read_sql(sql, conn.engine)

    # data is a list of the survey sentences and their IDs
    data = tb.survey_sentences(df)
    # Create new DF with the ID of the survey and the polarity scores of the sentences 
    polarity_df = pd.DataFrame(data , columns = ['ID', 'Sentences'])
    polarity_df["Polarity"] = polarity_df['Sentences'].map(tb.find_polarity)

    # polarity_df.to_csv("patient_satisfaction.csv")

    # can change if_exists to append, and add in a date feature to minimize processing power
    polarity_df.to_sql("PatientSatisfactionSurveyScores", conn.engine, if_exists='replace')

    sql_test = """
    SELECT TOP 10 * 
    FROM [dbo].[PatientSatisfactionSurveyScores]
    """
    
    print(pd.read_sql(sql_test, conn.engine))

if __name__ == '__main__':
    main()