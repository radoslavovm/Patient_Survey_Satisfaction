import pyodbc as odbc
import pandas as pd

cnxn = odbc.connect('Driver={SQL Server};'
                      "Server=arcsqlrpt03;"
                      "Database=ARC_DW;"
                      "Trusted_Connection=yes;"
                      "UID=python_user;"
                      "PWD=2cr1p1ingm@d3e@sy")


# DEFINE THE DATABASE CREDENTIALS
user = 'python_user'
password = '2cr1p1ingm@d3e@sy'
host = 'arcsqlrpt03'
database = 'ARC_DW'
driver = 'driver=SQL+Server'

cursor = cnxn.cursor()

