from sqlalchemy import create_engine
import pandas as pd
import urllib
import pyodbc

# DEFINE THE DATABASE CREDENTIALS
user = 'python_user'
password = '2cr1p1ingm@d3e@sy'
host = 'arcsqlrpt03'
database = 'ARC_DW'
driver = 'driver=SQL+Server'

quoted = urllib.parse.quote_plus(
                    "Driver={ODBC Driver 17 for SQL Server};"
                    "Server=arcsqlrpt03;"
                    "Database=ARC_DW;"
                    "Trusted_Connection=yes;"
                    "UID=python_user;"
                    "PWD=2cr1p1ingm@d3e@sy"
                )

engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

engine.begin()


sql = """
SELECT top 10 *
FROM [dbo].[Patient_Satisfaction_Survey] 
WHERE Comments != ''
"""

df = pd.read_sql(sql, engine)