from mcp.server.fastmcp.server import FastMCP


mcp = FastMCP("TestServer")

@mcp.tool() 
async def getSum(a:int, b:int):
    """ get the sum of two integers a and b"""
    return a+b



if __name__ == "__main__":
    print(type(mcp))
    mcp.run(transport="stdio")

    