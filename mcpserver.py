from mcp.server.fastmcp.server import FastMCP
from mailbot_functions.db_packages_by_same_user import run as sameUser 
from mailbot_functions.db_total_by_size import run as sameSize 
from mailbot_functions.db_search_by_DateRange import run as sameUserDateRange
from mailbot_functions.db_createpackage import run as createPackage
from mailbot_functions.db_createpackage import NewPackage, PackageSize




from dotenv import load_dotenv

load_dotenv()


mcp = FastMCP("AMailroomServer")

@mcp.tool() 
async def db_packages_by_same_user(recipient_fname,recipient_lname):
    """ show packages from the same user by matching first and last name"""
    """ for example: how many packages does Frank Lin have? Argumemnts: recipient_fname, recipient_lname should be frank, lin
    """
    recipient_fname = recipient_fname.lower()
    recipient_lname = recipient_lname.lower()
    return await sameUser(recipient_fname, recipient_lname)

@mcp.tool()
async def db_total_by_size(size:str, recipient_fname, recipient_lname):
    """ only take sizing keyword {small,medium, big} and user's first and last name from the request, and return all packages for the specific user based on the size request {small,medium,big}
    Example: how many big packages does Frank Lin have? Arguments: size should be big, recipient_fname should be Frank, recipient_lname should be Lin
    """
    recipient_fname = recipient_fname.lower()
    recipient_lname = recipient_lname.lower()

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
    recipient_fname = recipient_fname.lower()
    recipient_lname = recipient_lname.lower()
    return await sameUserDateRange(recipient_fname, recipient_lname, date_range)

@mcp.tool()
async def db_createpackage(newpackage: NewPackage):
    """ create a new package with the given information as the newpackage object
    Example: create a new package for Frank Lin with fragility True, size big, type box, delivery_date 2025-01-01, user_comment "This is a test package"
    Arguments: recipient_fname should be Frank, recipient_lname should be Lin, fragility should be True or False, size should be small, medium or big, type should be box or envelope or wooden crate, delivery_date should be in the format of YYYY-MM-DD
    """

    """
    When a user asks to create, add, or register a package (e.g., "Help me to add a package for Sean Chang, the type is box and the size is big"), extract the following required information:

- recipient_fname: The recipient's first name.
- recipient_lname: The recipient's last name.
- type: The type of the package (e.g., box, envelope, crate, etc.).
- size: The size of the package. Must be one of: "small", "medium", or "big".

Optional fields (if provided by the user):
- fragility: Whether the package is fragile (true/false).
- user_comment: Any additional comment from the user.

**Do not require delivery_date; it will be set automatically to the current time if not provided.**

Always extract and fill in the required fields: recipient_fname, recipient_lname, type, and size.
    """
    newpackage.recipient_fname = newpackage.recipient_fname.lower()
    newpackage.recipient_lname = newpackage.recipient_lname.lower()
   
    return await createPackage(newpackage)




if __name__ == "__main__":
    print(type(mcp))
    mcp.run(transport="stdio")

    