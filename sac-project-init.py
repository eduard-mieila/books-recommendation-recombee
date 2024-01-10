#  Script used to upload data to Recombee DB 
import csv
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import *

client = RecombeeClient(
  'DATABASE_ID_HERE', 
  'API_TOKEN_HERE', 
  region=Region.EU_WEST
)

inFileBooks = 'books19k.csv'
inFileUsers = 'users.csv'

with open(inFileBooks, 'r') as file:
    reader = csv.reader(file, delimiter=",")
    fields = next(reader)
    entries = {}

    for row in reader:
        currId = 0
        currBook = {}

        for colIndex, propValue in enumerate(row):
            if (colIndex == 0):
                currId = propValue
            currBook[fields[colIndex]] = propValue
        
        entries[currId] = currBook
    print("Read all the data from '" + inFileBooks + "'" )


    # # Upload id-uri/ASIN-uri carti 
    requests = []
    for itemId, item in entries.items():
        r = AddItem(itemId)
        # r = DeleteItem(itemId)
        requests.append(r)
    client.send(Batch(requests))
    print("Sent all ids to Recombee DB")

    # # Trimitere proprietăți produse
    requests = []
    for propName in fields:
        if propName == "imgUrl":
            r = AddItemProperty(propName, 'image')
        elif propName in ["stars", "price"]:
            r = AddItemProperty(propName, 'double')
        elif propName in ["reviews", "category_id"]:
            r = AddItemProperty(propName, 'int')
        elif propName in ["isBestSeller", "isEditorsPick", "isGoodReadsChoice", "isKindleUnlimited"]:
            r = AddItemProperty(propName, 'boolean')
        else:
            r = AddItemProperty(propName, 'string')
        requests.append(r)
    client.send(Batch(requests))
    print("Added all proprieties names to Recombee DB")

    # # Upload valori produse
    requests = []
    for itemId, value in entries.items():
        r = SetItemValues(itemId, value, cascade_create = True)
        requests.append(r)
    client.send(Batch(requests))
    print("Added all proprieties values to Recombee DB")


with open(inFileUsers, 'r',  encoding='utf-8-sig') as file:
    reader = csv.reader(file, delimiter=",")
    userFields = next(reader) # Read the header row
    users = {}

    for row in reader:
        currId = 0
        currUser = {}

        for colIndex, propValue in enumerate(row):
            if (colIndex == 0):
                currId = propValue
            currUser[userFields[colIndex]] = propValue
        
        users[currId] = currUser
    print("Read all the data from '" + inFileUsers + "'" )
    
    # Adauga id-urile userilor
    requests = []
    for userId, _ in users.items():
        r = AddUser(userId)
        # Delete pentru resetare DB
        # r = DeleteUser(userId)
        requests.append(r)
    client.send(Batch(requests))
    print("Sent all user ids to Recombee DB")

    # Adauga proprietatile userilor
    client.send(AddUserProperty("userName", "string"))
    client.send(AddUserProperty("initialized", "boolean"))

    # Adauga valorile proprietatilor userilor
    requests = []
    for userId, user in users.items():
        print(userId)
        print(user)
        currUser = user
        del currUser["userId"]
        r = SetUserValues(userId, currUser, cascade_create = True)
        requests.append(r)
    client.send(Batch(requests))
    print("Sent all user data to Recombee DB")
  