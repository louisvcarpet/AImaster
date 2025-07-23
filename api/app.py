from fastapi import FastAPI #FastAPI is a Python class that provides all the functionality for your API.
from enum import Enum 
from datetime import datetime
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"



app = FastAPI()


#operation HTTP method in api- post: create data / get: read  / put: update / delete , more ecotic method: options/ head / patch / trace

#1
@app.get("/Blake's_AI_Service/{AI_code}")
def root( AI_code: int):
    return {"message",  AI_code}

# 2
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# path parameters
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# query parameteres
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/required_items/")
async def read_item(skip: int = 0, limit: int = 10): #  skip 0 items to skip, limit 10 items to return
    return fake_items_db[skip : skip + limit]


@app.get("/read_items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False): 
    # p here is optional 
    item = {"item_id": item_id} 
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

######################## Request body ########################
#A request body is data sent by the client to your API. A response body is the data your API sends to the client.
from pydantic import BaseModel
class Item(BaseModel):
    recipientName: str
    Package_weight: float
    fragility: bool | None = None
@app.post("/Create_package/")
async def create_package(item: Item): # declare its type as the model you created, Item.
    if item.Package_weight >=1.3:
        return {"Gothca": "This is a heavy package, will route to big room!"}
    else:
        return {"Gotcha": "This is a light package, will rout to small room!"}
    
@app.get("Blake/AI_Service/hello")
async def SayHello(message: str):
    return {"message": message}

# q:  Annotated[str | None, Query(max_length=50)] = None
from typing import Annotated, Optional, Dict, Any
from fastapi import Query
#q: Annotated[str, Query()] = "rick"  
#  Annotated[list[str] | None, Query()] = None  url: ?q=foo&q=bar

# You can define a regular expression pattern that the parameter should match:
#  Query(min_length=3, max_length=50, pattern="^fixedquery$") 
    # ^: starts with the following characters, doesn't have characters before.
    # fixedquery: has the exact value fixedquery.
    # $: ends there, doesn't have any more characters after fixedquery. 
@app.get("/List/")
async def read_items(q: Annotated[list[str] | None, Query(title="Query string", min_length=2)] = ["one", "two"]):
    if q:
        query_items = {"q": q}
        return query_items


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(alias="Yo type sth here")] = None):
    results = {"items": [{"Name" : "Blake", "Age": int(21) }, {"item_id": "Bar"}], "Greeting":"Blake's AI Service"}
    if q:
        results.update({"q": q})
    return results


@app.get("/exclude")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = "Blake's exclusive query"):
    if hidden_query:
        return {"hidden_query": "Not hidden"}
    else:
        return {"hidden_query": "Not found"}
    


from pydantic import AfterValidator 
import random
#There could be cases where you need to do some custom validation that can't be done with the parameters shown above.

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/Customized_ID_Checker/")
async def read_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}

#########################API for MySQL database connection #########################

from mysqlconnector import MySqlConnector
from dotenv import load_dotenv
import pandas as pd
import os
load_dotenv()


connector = MySqlConnector(
    host="localhost",
    database="mailroom",
    userN=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD") 
)



# pandas takecare of mysql database here
df = pd.read_sql("packages", connector.engine)

# print(df)

@app.put("/MYSQL_BLAKE_Get_Packages_From_Name")
async def play_SQL(recipient_fname:Annotated[str, Query(description="First character capitalize")] , recipient_lname: str):
    if recipient_fname and recipient_lname:
        recipient_fname = recipient_fname.capitalize()
        recipient_lname = recipient_lname.capitalize()
        df_new = df[(df['recipient_fname'] == recipient_fname) & (df['recipient_lname'] == recipient_lname)]
    # df_SameUser = df_new.groupby(['recipient_fname', 'recipient_lname']).size().reset_index(name= 'total packages')
    if  df_new.empty:
        return {"message": "No packages found for the given recipient name."}

    return df_new.to_dict(orient='records')
    

class PackageSize(str, Enum):
    small = "small"
    medium = "medium"
    big = "big"

@app.get("/MYSQL_BLAKE_Get_Packages_From_Size")
async def play_SQL(size:PackageSize = Annotated[str, Query(description="Size of the package")]):
    if size:
        df_new = df[df['size'] == size.value]
    return df_new.to_dict(orient='records')

from datetime import datetime, timedelta
@app.get("/MYSQL_BLAKE_Get_Packages_Within_N_Days")
async def play_SQL(start_date: str, days:int):

    df_new = df[ (df['delivery_date'] <= start_date) & (df['delivery_date'] 
            >= pd.to_datetime(start_date) - pd.Timedelta(days=days))][['delivery_date', 'type','recipient_fname']]
    return df_new.to_dict(orient='records')



class NewPackage(BaseModel):
    recipient_fname: str
    recipient_lname: str
    fragility: bool 
    size: PackageSize
    type: str
    delivery_date: datetime
    user_comment: Optional[str] = None
    
@app.put("/MySQL_Blake_Create_Package")
# async def create_package(new_package: Dict[str, Any]):
async def create_package(new_package: NewPackage):
    # return "HI", new_package.model_dump() // model_dump() will copy and paste all input value in the required structure
    df_updated = pd.DataFrame([new_package.model_dump()])
    
    # Insert new row into the "packages" table using to_sql. 
    # if_exists="append" ensures the new row is added to the existing table
    df_updated.to_sql("packages", con=connector.engine, if_exists="append", index=False)
    df_updated = pd.read_sql("packages", connector.engine)
    # Return a success message and the updated DataFrame
    return "Package created successfully", df_updated.to_dict(orient='records')

print(df)





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8060)

# class main():
#     app = FastAPI()
#     app.get("/")


