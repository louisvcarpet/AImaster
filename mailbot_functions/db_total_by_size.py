
import pandas as pd
from dotenv import load_dotenv
from mysqlconnector import MySqlConnector
import os

load_dotenv()


async def run(input): # input shld be a dictionary cuz user wont just pass one word as their question
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
        if size in str(input).lower():
            size_value = size
            break
    else:
        return"Result: No valid size found in the request."

    # count the number of packages by size
    # print(f"\nTotal number of {input} packages for each resident: ")
    df_size_count = df[df['size']== size_value].groupby(['recipient_fname', 'recipient_lname']).size().reset_index(name = f'total {size_value} packages')
    result_str = df_size_count.to_string(index=False)
    return result_str

if __name__ == "__main__":
    import asyncio
    input_data = {"user_input": "How many big packages does the mailroom have?"}
    result = asyncio.run(run(input_data))
    print(result)