# Main part of the project - The Books Recommendation App
import random
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import *
from recombee_api_client.exceptions import ResponseException

categories = [
    {"category_id": 1, "category_name": "Arts & Photography"},
    {"category_id": 2, "category_name": "Comics"},
    {"category_id": 3, "category_name": "Education & Teaching"},
    {"category_id": 4, "category_name": "History"},
    {"category_id": 5, "category_name": "Literature & Fiction"},
    {"category_id": 6, "category_name": "Parenting & Relationships"},
    {"category_id": 7, "category_name": "Romance"},
    {"category_id": 8, "category_name": "Sports & Outdoors"},
    {"category_id": 9, "category_name": "Biographies & Memoirs"},
    {"category_id": 10, "category_name": "Computers & Technology"},
    {"category_id": 11, "category_name": "Engineering & Transportation"},
    {"category_id": 12, "category_name": "Humor & Entertainment"},
    {"category_id": 13, "category_name": "Medical"},
    {"category_id": 14, "category_name": "Politics & Social Sciences"},
    {"category_id": 15, "category_name": "Science & Math"},
    {"category_id": 16, "category_name": "Teen & Young Adult"},
    {"category_id": 17, "category_name": "Business & Money"},
    {"category_id": 18, "category_name": "Cookbooks, Food & Wine"},
    {"category_id": 19, "category_name": "Foreign Language"},
    {"category_id": 20, "category_name": "Law"},
    {"category_id": 21, "category_name": "Mystery, Thriller & Suspense"},
    {"category_id": 22, "category_name": "Reference"},
    {"category_id": 23, "category_name": "Science Fiction & Fantasy"},
    {"category_id": 24, "category_name": "Travel"},
    {"category_id": 25, "category_name": "Children's eBooks"},
    {"category_id": 26, "category_name": "Crafts, Hobbies & Home"},
    {"category_id": 27, "category_name": "Health, Fitness & Dieting"},
    # {"category_id": 28, "category_name": "LGBTQ+ eBooks"},
    {"category_id": 29, "category_name": "Nonfiction"},
    {"category_id": 30, "category_name": "Religion & Spirituality"},
    {"category_id": 31, "category_name": "Self-Help"},
]

client = RecombeeClient(
  'proiect-sac-upb-dev', 
  'dc0CKTIOpCCP3awXAaocJpBLPP0qx57ZRABTmVI26cuUp3F7G4hr9TRFapWsXtre', 
  region=Region.EU_WEST
)
inFileBooks = 'books19k.csv'
inFileUsers = 'users.csv'
selectedUid = ""
selectedUser = {}
lastBookId = ""
lastBook = {}
lastRecommId = ""

commandsText = '''Pick one of the following commands:

    users\t\t - show all users
    select <user_id>\t - select user_id for operations
    deselect\t\t - logout from current user
    recommend <n>\t - see n recommandations for following user
    view <book_title>\t - view details about specific book
    read\t\t - set last viewed book as read
    simillar <n>\t - see n simillar books to the last book seen
    search <word>\t - search for items containing a specific word
    shuffle\t\t - start a quiz to recommend new titles based on categories
    help\t\t - print this message
    exit\t\t - quit the script
'''
    # categories\t\t - see book categories
 
def printUsers(result):
    for u in result:
        print(u["userId"] + " - " + u["userName"] + "\t - Initialized: " + str(u["initialized"]))
    print("==============================\n")

def printUser(uid, result):
    print("==============================")
    print("Selected user: " + uid)
    print("Username: " + result["userName"])
    print("Initialized: " + str(result["initialized"]))
    print("==============================\n")

def printTitles(result):
    print("==============================")
    for b in result["recomms"]:

        print("[" + b["id"] + "] - " + b["values"]["title"] + " - Category : " + b["values"]["category_name"])
    print("==============================\n")
    
def printBook(bid, result):
    print("==============================")
    print("Book ID(ASIN): " + bid)
    print("Title: " + result["title"])
    print("Author: " + result["author"])
    print("Category: " + result["category_name"])
    print("Bestseller: " + str(result["isBestSeller"]))
    print("Price: $" + str(result["price"]))
    print("Rating: $" + str(result["stars"]))
    print("==============================\n")


def coldStartProcedure(user):
    print("Cold start procedure intiated!")
    # Intreaba de 3 utilizatorul care categorii sunt de interes
    for i in range(3):
        # Pune utilizatorul sa aleaga dintre 3 categorii
        catList = random.choices(categories, k=3)
        print("Which of these 3 categories looks interesting to you?")
        print("1 - " + catList[0]["category_name"])
        print("2 - " + catList[1]["category_name"])
        print("3 - " + catList[2]["category_name"])
        choice = input("Enter your choice(1 - 3): ")
        while choice not in ["1", "2", "3"]:
            print("\n\nERROR: wrong choice!")
            print("Which of these 3 categories looks interesting to you?")
            print("1 - " + catList[0]["category_name"])
            print("2 - " + catList[1]["category_name"])
            print("3 - " + catList[2]["category_name"])
            choice = input("Enter your choice(1 - 3): ")

        result = client.send(RecommendItemsToUser(selectedUid, 5, filter="'category_id' == " + str(catList[int(choice[0]) - 1]["category_id"]), return_properties=True, diversity=0.75, rotation_rate=0.9))
        print("\nWe recommend these 5 titles for you:")
        printTitles(result)
        lastRecommId = result["recommId"]
        # Pune utilizatorul sa aleaga una din cele 5 carti propuse si marcheaz-o ca fiind de interes in SR
        bookId = input("Please choose one title that looks interesting to you[ID]: ")
        client.send(AddDetailView(selectedUid, bookId, recomm_id=lastRecommId))
        client.send(AddPurchase(selectedUid, bookId, recomm_id=lastRecommId))

    # La finalul procedurii marcheaza utlizatorul ca fiind initializat
    user["initialized"] = True
    client.send(SetUserValues(selectedUid, user))
    printUser(selectedUid, user)






print(commandsText)
while (True):
    line = input("Enter a command: ")
    command = line.split()
    if command[0] == "exit":
        break

    if command[0] == "help":
        print(commandsText)

    elif command[0] == "users":
        result = client.send(ListUsers(return_properties=True))
        printUsers(result)

    elif command[0] == "select":
        if len(command) != 2:
            print("Error: command shoud be 'select <user_id>\n\n")
            pass
        try:
            result = client.send(GetUserValues(command[1]))
        except ResponseException as e:
            print("An error occured, check user ID!")
        else:
            printUser(command[1], result)
            selectedUid = command[1]
            selectedUser = result
            lastBookId = ""
            lastBook = {}
            lastRecommId = ""

            # Verificare initialized, pornire procedura de first login 
            if not selectedUser["initialized"]:
                coldStartProcedure(selectedUser)

    elif command[0] == "deselect":
        selectedUid = ""
        selectedUser = {}
        lastBookId = ""
        lastBook = {}
        print("User deselected")

    # elif command[0] == "categories":
    #     result = client.send(ListItems(return_properties=True))
    #     categories = []
    #     requests = []
    #     for e in result:
    #         if e["category_name"] not in categories:
    #             categories.append(e["category_name"])
    #     print(categories)

    elif command[0] == "recommend":
        if len(command) != 2:
            print("Error: command shoud be 'recommend <number>\n\n")
            pass
        if selectedUid == "":
            print("Error: to get a recommandation you first need to select a user!")
        else:
            result = client.send(RecommendItemsToUser(selectedUid, int(command[1]), return_properties=True, diversity=0.9, rotation_rate=0.9))
            printTitles(result)
            lastRecommId = result["recommId"]

    elif command[0] == "view":
        if len(command) != 2:
            print("Error: command shoud be 'view <book_id>\n\n")
            pass
        if selectedUid == "":
            print("Error: select a user first!")
        else:
            try:
                result = client.send(GetItemValues(command[1]))
            except ResponseException as e:
                print("An error occured, check book ID!")
            else:
                printBook(command[1], result)
                client.send(AddDetailView(selectedUid, command[1], recomm_id=lastRecommId))
                lastBookId = command[1]
                lastBook = result

    elif command[0] == "read":
        if lastBookId == "":
            print("Error: to read a book you first need to view a book!")
        else:
            result = client.send(AddPurchase(selectedUid, lastBookId, recomm_id=lastRecommId))
            print("'" + lastBook["title"] + "' has been added to your read books!")

    elif command[0] == "simillar":
        if len(command) != 2:
            print("Error: command shoud be 'simillar <number>\n\n")
            pass
        if lastBookId == "":
            print("Error: to read a book you first need to view a book!")
        else:
            result = client.send(RecommendItemsToItem(lastBookId, selectedUid, command[1], return_properties = True, diversity=0.75, rotation_rate=0.9))
            printTitles(result)
            lastRecommId = result["recommId"]

    elif command[0] == "search":
        if len(command) != 2:
            print("Error: command shoud be 'search <word>\n\n")
            pass
        if selectedUid == "":
            print("Error: to search for an item you first need to select a user!")
        else:
            result = client.send(SearchItems(selectedUid, search_query=command[1], count=10, return_properties=True))
            printTitles(result)
            lastRecommId = result["recommId"]

    elif command[0] == "shuffle":
        if selectedUid == "":
            print("Error: select a user first!")
        else:
            coldStartProcedure(selectedUser)