from mysqlconnector import MySqlConnector
import pandas as pd
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import Annotated, Optional, Dict, Any
from datetime import datetime
from enum import Enum 
load_dotenv()



class PackageSize(str, Enum):
    small = "small"
    medium = "medium"
    big = "big"

class NewPackage(BaseModel):
    recipient_fname: str
    recipient_lname: str
    fragility: Optional[bool] = None
    size: PackageSize
    type: str
    delivery_date: datetime= Field(default_factory=datetime.now)
    user_comment: Optional[str] = None

async def run(new_package: NewPackage):
    connector = MySqlConnector(
    host="localhost",
    database="mailroom",
    userN=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD") 
    )
  
    engine = connector.engine


    # return "HI", new_package.model_dump() // model_dump() will copy and paste all input value in the required structure
    
    df_updated = pd.DataFrame([new_package.model_dump()])
    
    # Insert new row into the "packages" table using to_sql. 
    # if_exists="append" ensures the new row is added to the existing table
    df_updated.to_sql("packages", con=connector.engine, if_exists="append", index=False)
    df_updated = pd.read_sql("packages", connector.engine)
    # Return a success message and the updated DataFrame
    return "Package created successfully", df_updated.to_dict(orient='records')

