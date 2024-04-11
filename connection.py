import sqlalchemy as sa 
from sqlalchemy import create_engine
from urllib.parse import quote_plus 

"""
import pyodbc 

cnxn = pyodbc.connect('Driver={SQL Server};'
                      "Server=arcsqlrpt03;"
                      "Database=ARC_DW;"
                      "Trusted_Connection=yes;")

cursor = cnxn.cursor()
cursor.execute("SELECT COUNT(*) FROM [dbo].[Patient_Satisfaction_Survey] WHERE Comments != ''")
"""

# DEFINE THE DATABASE CREDENTIALS
domain = 'addomain1'
user = 'martina.radoslavov'
password = 'Mir001896019!'
host = 'arcsqlrpt03'
database = 'ARC_DW'
driver = 'driver=SQL+Server'

connection_url = sa.engine.URL.create(
    drivername="mssql+pyodbc",
    username="addomain1\martina.radoslavov",
    password="Mir001896019!",
    host="arcsqlrpt03",
    database="ARC_DW"
)

connectionString = f'mssql+pyodbc://@{host}/{database}?{driver}' ## cant get the backslash to come out right domain\username

engine = create_engine(
    # "mssql+pyodbc://%s:Mir001896019!@arcsqlrpt03/ARC_DW?driver=SQL+Server" % quote_plus("addomain1\martina.radoslavov")
    connectionString
    )

engine.begin()