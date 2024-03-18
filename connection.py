from sqlalchemy import create_engine

"""
import pyodbc 

cnxn = pyodbc.connect('Driver={SQL Server};'
                      "Server=arcsqlrpt03;"
                      "Database=ARC_DW;"
                      "Trusted_Connection=yes;")

cursor = cnxn.cursor()
cursor.execute("SELECT COUNT(*) FROM [dbo].[Patient_Satisfaction_Survey] WHERE Comments != ''")
"""

engine = create_engine(
    'mssql+pyodbc://'
    '@arcsqlrpt03/ARC_DW?' # username:pwd@server:port/database
    'driver=SQL+Server'
    )
