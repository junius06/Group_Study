import pyupbit
# import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('user', 'root')
password = os.getenv('password', 'p@ssw0rd')
host = os.getenv('host', '127.0.0.1')
database = os.getenv('database', 'blockchain')
    
ticker = 'KRW-BTC'
interval = 'minute1'
to = '2024-04-17 20:00'
count = 200

# Fetch data from Upbit
price_now = pyupbit.get_ohlcv(ticker=ticker, interval=interval, to=to, count=count)

# Create a connection to the MySQL database
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

# Use the connection to write the DataFrame to SQL
price_now.to_sql('BTC', con=engine, if_exists='append', index=False)

# Close the connection
engine.dispose()