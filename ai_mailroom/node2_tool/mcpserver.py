from mcp.server.fastmcp.server import FastMCP
from mailbot_functions.db_packages_by_same_user import run as sameUser 
from mailbot_functions.db_total_by_size import run as sameSize 
from mysqlconnector import MySqlConnector
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()


mcp = FastMCP("AMailroomServer")

@mcp.tool() 
async def db_packages_by_same_user():
    """ show packages from the same user by matching first and last name"""
    return await sameUser()

@mcp.tool()
async def db_total_by_size(size:str):
    """ only take sizing keyword {small,medium, big} from the request, and return all users' packages based on the size request {small,medium,big
    for example: only show me who has small packages, list them all """

    return await sameSize(size)

# @mcp.resource
# async def show_table(request:str): 
#     df = pd.read_sql("packages", engine) #df is the dataframe of the entire mailroom mysql table about packages and recipient informations 
#     """f read this entire database table for the mailroom informationto answer some general mailroom {request} from user"""
#     return await {request}



if __name__ == "__main__":
    print(type(mcp))
    mcp.run(transport="stdio")

    