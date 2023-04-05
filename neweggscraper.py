from bs4 import BeautifulSoup
import requests
import re

search = input("What product are you searching for? ")

url = f"https://www.newegg.com/p/pl?d={search}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

pagesText = doc.find(class_="list-tool-pagination-text").strong
numPages = str(pagesText).split("/")[-2]
numPages = "".join(i for i in numPages if i.isalnum()) # Regex to isolate the number from the HTML comments
numPages = int(numPages)

itemsFound = {}

currentPage = 1
for page in range(1, numPages + 1):
    url = f"https://www.newegg.com/p/pl?d={search}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    print(f"Scanning Page {currentPage}/{numPages}")

    itemsDiv = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = itemsDiv.find_all(string = re.compile(search))

    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue
        
        itemName = parent.text

        link = parent['href']
        nextParent = item.find_parent(class_="item-container")

        priceTag = nextParent.find(class_="price-current").text
        priceSplit = priceTag.split("\xa0")
        price = priceSplit[0].replace("$", "")
        price = price.replace(",", "")

        if price == "":
            print("Error collecting price data for item: ", itemName, '\n')
            continue

        #print(itemName)
        #print(price)
        #print('\n')

        itemsFound[item] = {"price": float(price), "link": link}
    currentPage += 1

sortedItems = sorted(itemsFound.items(), key = lambda x: x[1]['price'])

with open("python\encryptiontesting\priceinformation.txt", 'w') as f:
    for item in sortedItems:
        f.write(item[0] + '\n')
        f.write(f"${item[1]['price']}\n")
        f.write(item[1]['link'] + '\n')
        f.write("--------------------------------------------------" + '\n')

#for item in sortedItems:
    #print(item[0])
    #print(f"${item[1]['price']}")
    #print(item[1]['link'])
    #print("--------------------------------------------------", '\n')
