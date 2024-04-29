import pandas as pd
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import _stop_words
import connection as conn

# I need to create a training csv with the comments and their neg/pos scores 

sql = """
SELECT * 
FROM [dbo].[Patient_Satisfaction_Survey] 
WHERE Comments != ''
"""
# Query the survey's that do have a commment. 
df = pd.read_sql(sql, conn.engine).set_index('ID').drop_duplicates()