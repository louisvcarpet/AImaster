from mysqlconnector import MySqlConnector
import pandas as pd
from dotenv import load_dotenv
import datetime
import os

load_dotenv()


async def run(recipient_fname=None, recipient_lname=None , date_range:int =None ):
    connector = MySqlConnector(
    host="localhost",
    database="mailroom",
    userN=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD") 
    )

    engine = connector.engine
    df =  pd.read_sql("packages", engine)


    earliest = datetime.datetime.now() - pd.Timedelta(days= date_range)  # 1 year ago
    df['delivery_date'] = pd.to_datetime(df['delivery_date'])
    df = df[df['delivery_date'] > earliest]

    dfSameUser = df[
    (df['recipient_fname'].str.lower() == recipient_fname.lower()) &
    (df['recipient_lname'].str.lower() == recipient_lname.lower())
    ][['type', 'size' ,'delivery_date']].reset_index(drop=True)

    total = dfSameUser.shape[0] if not dfSameUser.empty else 0
    if dfSameUser.empty:
        return f"No packages found for {recipient_fname} {recipient_lname} after {earliest.date()}."

    return f"{recipient_fname} {recipient_lname} has {total} packages delivered after {earliest.date()}:\n{dfSameUser.to_string(index=False)}"
    


if __name__ == "__main__":
    import asyncio
    result = asyncio.run(run("Rachel", "Chang", date_range= 60))
    print(result)
