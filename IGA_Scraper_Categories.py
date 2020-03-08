from colorama import Fore, Back, Style
from bs4 import BeautifulSoup as bs
from operator import itemgetter
import requests
import colorama
import math
import re

# init color console
colorama.init()

# # #   M A K E   C S V   # # #
categoriesText = [
    "All Categories",
    "Beverages",
    "Bulk Foods",
    "Commercial Bakery",
    "Deli and Cheese",
    "Frozen",
    "Grocery",
    "Health and Beauty",
    "Health Care",
    "Meal Replacement",
    "Bakery",
    "Meat",
    "Produce",
    "Refrigerated Grocery",
    "Seafood"
    ]
categoriesUrlsExtensions = [
    r"in-promotion",
    r"Beverages/in-promotion",
    r"Bulk%20Foods/in-promotion",
    r"Commercial%20Bakery/in-promotion",
    r"Deli%20and%20Cheese/in-promotion",
    r"Frozen/in-promotion", 
    r"Grocery/in-promotion",
    r"Health%20%26%20Beauty/in-promotion",
    r"Health%20Care/in-promotion",
    r"Home%20Meal%20Replacement/in-promotion",
    r"Instore%20Bakery/in-promotion",
    r"Meat/in-promotion",
    r"Produce/in-promotion",
    r"Refrigerated%20Grocery/in-promotion",
    r"Seafood/in-promotion"
    ]

print("Please enter desired category number: ")
i = 1
for cat in categoriesText:
    print("{}: {}".format(i, cat))
    i += 1

userCategory = int(input("\n"))
1 if userCategory not in range(1,16) else int(userCategory)
# down one to account for lists
userCategory -= 1

with open("igaSalesExport {}.csv".format(categoriesText[userCategory]), "w") as csv:
    
    csv.write("Item Name,Item Category/Brand,Regular Price,Sale Price,Total Sale Discount,Discount Ratio")

# # #   G E T   P A G E S   # # #

urlDefaultLanding = r"https://www.iga.net/en/online_grocery/browse/{}".format(categoriesUrlsExtensions[userCategory])

pagesScrape = requests.get(urlDefaultLanding)
pagesHtmlDocument = pagesScrape.content
soup = bs(pagesHtmlDocument, "html.parser")
navigationPages = soup.find("ul", "nav nav--block pagination")
regEx = r"page=(.+?)&"

totalItems = int(re.findall(regEx, str(navigationPages))[-1]) * 20
pagesTotal = math.ceil(totalItems / 1000)
print("Roughly total items to scrape: {}".format(totalItems))
print("Pages to scrape: {}".format(pagesTotal))

# # #   C R E A T E   U R L S   # # #

urls = []
for p in range(pagesTotal):
    p += 1
    urls.append("https://www.iga.net/en/online_grocery/browse/{}?pageSize=1000&page={}".format(categoriesUrlsExtensions[userCategory], p))

# # #   P A R S E   U R L S   # # #
print("Working on URL:")
itemCatalog = []

for url in urls:
    
    print("{}...".format(url))
        
    productsScrape = requests.get(url)
    htmlDocument = productsScrape.content
    soup = bs(htmlDocument, "html.parser")

    for productGridItem in soup.find_all("div", "item-product__content push--top"):
        try: 
            productSalePrice = productGridItem.find("span", "price text--strong")
            productSalePrice = productSalePrice.text[1:]
            productPrice = productGridItem.find("span", "price-amount")
            productPrice = productPrice.text[1:]
            productCategory = productGridItem.find("div", "item-product__brand push--top")
            productCategory.text if productCategory.text == None else "Misc"
            if productCategory.text != None:  productCategory = productCategory.text.strip()
            else:
                productCategory = "Misc"
            productName = productGridItem.find("a", "js-ga-productname")
            if productName.text[0] == " ": 
                productName = productName.text[1:]
            else:
                productName = productName.text
            productDiscount = "{:2.2f}".format(float(productPrice) - float(productSalePrice))
            productSaleRatio = float(productDiscount) / float(productPrice)
            productSaleRatio = "{:1.4f}".format(productSaleRatio)
            productMetadataGroup = [
                productName.replace(",","-"),
                productCategory.replace(",","-"),
                productPrice,
                productSalePrice,
                productDiscount,
                productSaleRatio
            ]
            itemCatalog.append(productMetadataGroup)
            
        except AttributeError:
            # item not on sale, IDGAF
            pass
            
itemCatalog = sorted(itemCatalog, key = itemgetter(5), reverse=True)
    
# # #   W R I T E   T O   C S V   # # #

with open("igaSalesExport {}.csv".format(categoriesText[userCategory]), "a") as csv:
                
    for product in itemCatalog:
        csv.write(
        "\n{},{},${},${},${},{}".format(
            product[0],
            product[1],
            product[2],
            product[3],
            product[4],
            product[5]
            )
        )
      
for product in itemCatalog:
    print("{}Item Name: {}{}\n{}Item Category/Brand: {}{}\nRegular Price: ${}\nSale Price: ${}\n{}Total Sale Discount: ${}{}\n".format(
        Fore.CYAN,
        product[0],
        Style.RESET_ALL,
        Fore.GREEN,
        product[1],
        Style.RESET_ALL,
        product[2],
        product[3],
        Fore.RED,
        product[4],
        Style.RESET_ALL
        )
    )

    
print("Finished!")
