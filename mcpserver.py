from mcp.server.fastmcp.server import FastMCP
from mailbot_functions.db_packages_by_same_user import run as sameUser 
from mailbot_functions.db_total_by_size import run as sameSize 
from mailbot_functions.db_search_by_DateRange import run as sameUserDateRange
from mysqlconnector import MySqlConnector
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()


mcp = FastMCP("AMailroomServer")

@mcp.tool() 
async def db_packages_by_same_user(recipient_fname,recipient_lname):
    """ show packages from the same user by matching first and last name"""
    """ for example: how many packages does Frank Lin have? Argumemnts: recipient_fname, recipient_lname should be Frank, Lin
    """
    return await sameUser(recipient_fname, recipient_lname)

@mcp.tool()
async def db_total_by_size(size:str, recipient_fname, recipient_lname):
    """ only take sizing keyword {small,medium, big} and user's first and last name from the request, and return all packages for the specific user based on the size request {small,medium,big}
    Example: how many big packages does Frank Lin have? Arguments: size should be big, recipient_fname should be Frank, recipient_lname should be Lin
    """

    return await sameSize(size, recipient_fname, recipient_lname)

@mcp.tool()
async def db_search_by_DateRange(recipient_fname, recipient_lname, date_range:int):
    """ show packages from the same user by matching first and last name, and the date range
    Example A: how many packages does Frank Lin have within 63 days? Arguments: recipient_fname should be Frank, recipient_lname should be Lin, date_range should be 63
    Example B: how many packages does Frank Lin have within 1 year? Arguments: recipient_fname should be Frank, recipient_lname should be Lin, date_range should be 365
    Example C: how many packages does Frank Lin have within 1 month? Arguments: recipient_fname should be Frank, recipient_lname should be Lin, date_range should be 30
    Example D: how many packages does Blake Chang have since 2025-01-01? Arguments: recipient_fname should be Blake, recipient_lname should be Chang, date_range should be the number of days from 2025-01-01 to the current date.(use EST time zone for current date)
    Note: you will caculate the date_range based on the current date and the date you want to search from.
   
    """
    return await sameUserDateRange(recipient_fname, recipient_lname, date_range)




if __name__ == "__main__":
    print(type(mcp))
    mcp.run(transport="stdio")

    