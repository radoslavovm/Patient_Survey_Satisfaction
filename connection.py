from sqlalchemy import create_engine
import urllib
import json

# DEFINE THE DATABASE CREDENTIALS
with open('config.json') as f:
    config = json.load(f)

DB_USERNAME = config['DB_USERNAME']
DB_PASSWORD = config['DB_PASSWORD']
HOST = config["HOST"]
DATABASE = config["DATABASE"]
DRIVER = config["DRIVER"]

quoted = urllib.parse.quote_plus(
                    f"Driver={DRIVER};"
                    f"Server={HOST};"
                    f"Database={DATABASE};"
                    "Trusted_Connection=yes;"
                    f"UID={DB_USERNAME};"
                    f"PWD={DB_PASSWORD}"
                )

engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

engine.begin()