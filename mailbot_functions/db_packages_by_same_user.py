from mysqlconnector import MySqlConnector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


async def run(input=None):
    connector = MySqlConnector(
    host="localhost",
    database="mailroom",
    userN=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD") 
    )

    connector.connect()
  
    engine = connector.engine


    # pandas takecare of mysql database here
    df =  pd.read_sql("packages", engine)
    df_SameUser =  df.groupby(['recipient_fname', 'recipient_lname']).size().reset_index(name= 'total packages')
    return  df_SameUser.to_string(index=False)
    # print("\n",df_SameUser)

