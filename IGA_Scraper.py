from colorama import Fore, Back, Style
from bs4 import BeautifulSoup as bs
from operator import itemgetter
from selenium import webdriver
import datetime
import requests
import time
import math
import sys
import re
import os

# set local as dir
os.chdir(sys.path[0])
now = datetime.datetime.now()
time_string = "{}-{}-{}".format(now.year, now.month, now.day)

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

def clean(istr):
    if "\n" in istr:
        istr = istr.replace(r"\n", "")
    if "$" in istr:
        istr = istr.replace("$", "")
    return(istr)

print("Please enter desired category number: ")
for i, cat in enumerate(categoriesText, 1):
    print("{}: {}".format(i, cat))

userCategory = int(input("Choose your category: "))
1 if userCategory not in range(1,16) else int(userCategory)
# down one to account for lists
userCategory -= 1

cv_name = "igaSalesExport {}-{}.csv".format(categoriesText[userCategory], time_string)
with open(cv_name, "w") as csv:

    csv.write("Item Name,Item Category/Brand,Regular Price,Sale Price,Total Sale Discount,Discount Ratio")

# # #   G E T   P A G E S   # # #
# init driver
driver = webdriver.Firefox(executable_path=r"...\geckodriver.exe")

urlDefaultLanding = r"https://www.iga.net/en/online_grocery/browse/{}".format(categoriesUrlsExtensions[userCategory])
pagesScrape = requests.get(urlDefaultLanding)
pagesHtmlDocument = pagesScrape.content
soup = bs(pagesHtmlDocument, "html.parser")

# # #   C R E A T E   U R L S   # # #

urls = []
for p in range(1,20):
  urls.append("https://www.iga.net/en/online_grocery/browse/{}?pageSize=200&page={}".format(categoriesUrlsExtensions[userCategory], p))

# # #   P A R S E   U R L S   # # #

itemCatalog = []

driver.get("https://www.iga.net/en/online_grocery/browse/in-promotion")

for url in urls:

    print(f"Parsing {url}")
    driver.get(url)

    htmlDocument = driver.page_source

    soup = bs(htmlDocument, "html.parser")
    counter = 0
    found = 0
    for productGridItem in soup.find_all("div", "item-product__content push--top"):
        found += 1
        ### P R I C E ###
        try:
            productSalePrice = clean(productGridItem.find("span", {"class": "price text--strong"}).text)
            productPrice = clean(productGridItem.find("span", "price-amount").text)
        except AttributeError:
            continue
        ### D E T A I L S ###
        try: 
            productCategory = productGridItem.find("div", "item-product__brand push--top").text
            productCategory = [re.findall(r'[^\S][A-Za-z]+', productCategory, flags=re.DOTALL)]
            productCategory= productCategory.join("", productCategory)
        except AttributeError:
            productCategory = "Misc"
        productName = productGridItem.find("a", "js-ga-productname")
        if productName.text[0] == " ":
            productName = productName.text[1:]
        else:
            productName = productName.text
        ### M A T H ###
        productDiscount = "{:2.2f}".format(float(productPrice) - float(productSalePrice))
        productSaleRatio = float(productDiscount) / float(productPrice)
        productSaleRatio = "{0:.0%}".format(productSaleRatio)
        productMetadataGroup = [
            productName.replace(",","-"),
            productCategory.replace(",","-"),
            productPrice,
            productSalePrice,
            productDiscount,
            productSaleRatio
        ]
        itemCatalog.append(productMetadataGroup)
        counter += 1
        print(productMetadataGroup)
        print([found, counter])

itemCatalog = sorted(itemCatalog, key = itemgetter(5), reverse=True)

# # #   W R I T E   T O   C S V   # # #

with open(cv_name, "a") as csv:

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

print("Finished!")
