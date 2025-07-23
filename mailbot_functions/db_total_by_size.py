
import pandas as pd
from dotenv import load_dotenv
from mysqlconnector import MySqlConnector
import os

load_dotenv()


async def run(input_size,recipient_fname=None, recipient_lname=None): # input shld be a dictionary cuz user wont just pass one word as their question
    """
    this tool is used for getting the number of packages based on size
    """
    connector = MySqlConnector(
        host="localhost",
        database="mailroom",
        userN=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD") 
    )

    engine = connector.engine
    df = pd.read_sql("packages", engine)
   
    for size in ["big", "medium", "small"]:
        if size in str(input_size).lower():
            size_value = size
            break
    else:
        return"Result: No valid size found in the request."

    # count the number of packages by size
    # print(f"\nTotal number of {input} packages for each resident: ")
    df_size = df[df['size']== size_value].groupby(['recipient_fname', 'recipient_lname']).size().reset_index(name = f'total {size_value} packages')
    df_SameUser = df_size[
    (df_size['recipient_fname'].str.lower() == recipient_fname.lower()) &
    (df_size['recipient_lname'].str.lower() == recipient_lname.lower())
    ]
    
    
    total = df_SameUser[f'total {size_value} packages'].iloc[0] if not df_SameUser.empty else 0
    return  f"{recipient_fname} {recipient_lname} has {total} {size_value} packages."

if __name__ == "__main__":
    import asyncio
    input_data = {"user_input": "medium"}
    result = asyncio.run(run(input_data, recipient_fname="lonzo", recipient_lname="ball"))
    print(result)