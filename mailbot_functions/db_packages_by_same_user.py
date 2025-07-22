from mysqlconnector import MySqlConnector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


async def run(recipient_fname=None, recipient_lname=None):
    connector = MySqlConnector(
    host="localhost",
    database="mailroom",
    userN=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD") 
    )

    
  
    engine = connector.engine


    # pandas takecare of mysql database here
    df =  pd.read_sql("packages", engine)

   # Filter the DataFrame for the given recipient_fname and recipient_lname
    if recipient_fname is not None:
        df = df[df["recipient_fname"] == recipient_fname.lower()]
    if recipient_lname is not None:
        df = df[df["recipient_lname"] == recipient_lname.lower()]

    # Group by the columns and count
    df_SameUser = df.groupby(["recipient_fname", "recipient_lname"]).size().reset_index(name='total packages')
    total = df_SameUser['total packages'].iloc[0] if not df_SameUser.empty else 0
    return  f"{recipient_fname} {recipient_lname} has {total} packages."


if __name__ == "__main__":
    import asyncio
    result = asyncio.run(run("Frank", "Lin"))
    print(result)

