# Script used to reduce the Dataset from ~130k entries to
# ~19k in order to fit the requirements for Recombee Trial Plan
import csv
from math import floor

inFileBooks = 'books.csv'

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


    elementsCount = len(entries)
    categories = {}

    for itemId, item in entries.items():
        if item["category_name"] in categories.keys():
            categories[item["category_name"]]["count"] += 1
        else:
            categories[item["category_name"]] = {"count": 1}

    for category, stats in categories.items():
        stats["percentage"] = (stats["count"] / elementsCount) * 100
        stats["cutItems"] = floor(stats["percentage"] / 100 * 19000)
        stats["newCount"] = 0

    newEntries = []

    for itemId, item in entries.items():
        currCat = item["category_name"]
        if categories[currCat]["newCount"] <= categories[currCat]["cutItems"]:
            newEntries.append(item)
            categories[currCat]["newCount"] += 1

    with open('books19k.csv', 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
        writer.writeheader() 
        writer.writerows(newEntries)
    

    print(categories)
    print(len(newEntries))




  