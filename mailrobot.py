from MySqlConnector import Mysqlconnector
from dotenv import load_dotenv
import pandas as pd
import os
load_dotenv()



connector = Mysqlconnector(
    host="localhost",
    database="mailroom",
    userN=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD") 
)

connector.connect()
engine = connector.engine

# pandas takecare of mysql database here
df = pd.read_sql("packages", connector.engine)


# filter the user with last name 'Chang' (fixed)
# print(df[df['recipient_lname']=='Kim'])

# # filter the size with big(fixed)
# print(df.query("size=='big'"))

# # count the size of the table(fixed)
# print(df.size)

# print('df shape:', df.shape)
# print('column number:', df.shape[1])

# count the number of type == box
# print(df[df['type']=="box"])

# select the first 5 row
# print(df.head(5))

# select the last 5 row
# print(df.tail(5))
        #tail(int): the last nth element of the dataframe

# select the second to the fifth
# print(df.iloc[2:6]) 
        # iloc: Purely integer-location based indexing for selection by position.

##################################################################################
#IMPORTANT
# 1) select the special user comment
## hint: define what is special
sepcial = 'freeze'
# print(df[df['user_comment'] == sepcial],"\n")

# 2)select the data that size is big and type is box(fixed)
# print(df[(df['size']=="medium") & (df['type']=="box")])
    # and: &  
    #bracket up the conditon (con1) & (con2)

# 3)count the number of packages by same user, exp:Chang 

df_SameUser = df.groupby(['recipient_fname', 'recipient_lname']).size().reset_index(name= 'total packages')
print("\n",df_SameUser)
#### Only show the user that its total package is more than 1

print ("\n", df_SameUser[df_SameUser['total packages']>1])


# 4)count the number of small packages 
print('\nnumber of small packages:', df[df['size'] == 'small'].shape[0])
print(df['size'].value_counts().reset_index(name="total"))



# 5)return the user full name if they had small packages
size = "small"
# for each person, how many package do they hv in each size (fixed)

print(df.groupby(['recipient_lname'])['size'].value_counts().reset_index())

################################################################################
#what if i want the frame to look like: name big small medium, hint: i have to ways to do that ; IMPORTANT

df_SeperateSize = pd.crosstab(
    index=[df['recipient_fname'], df['recipient_lname']],
    columns=df['size']
).reset_index(names=['First Name','Last Name'])
print(df_SeperateSize, "\n\n\nnow only show big packages > 0\n\n")
print(df_SeperateSize[df_SeperateSize['big']>0])

# pivot
# get_dummies

#######################################################################
# count the size == small (use SQL syntax with parameters)
size = "small"

# function to get the total count of packages by users
def get_packages_by_size(size):
    query2 = f"""
    select recipient_fname, recipient_lname
    from packages
    where size = '{size}'
    """
    return pd.read_sql(query2.format({'user':size}), engine)

df_test = get_packages_by_size(size)
# print('\n\n\nQuantity of total small packages: ', df_test.shape[0])
#         #shape[] can be as a counter

   



