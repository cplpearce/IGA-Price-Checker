from colorama import Fore, Back, Style
from bs4 import BeautifulSoup as bs
from operator import itemgetter
import requests
import colorama
import re

# init color console
colorama.init()

# # #   M A K E   C S V   # # #

with open("igaSalesExport.csv", "w") as csv:
    
    csv.write("Item Name,Item Category/Brand,Regular Price,Sale Price,Total Sale Discount,Discount Ratio")

# # #   G E T   P A G E S   # # #

urlPages = "https://www.iga.net/en/online_grocery/browse/in-promotion"
pagesScrape = requests.get(urlPages)
pagesHtmlDocument = pagesScrape.content
soup = bs(pagesHtmlDocument, "html.parser")
navigationPages = soup.find("ul", "nav nav--block pagination")
regEx = r"page=(.+?)&"
totalItems = int(re.findall(regEx, str(navigationPages))[-1]) * 20
pagesTotal = round(totalItems / 1000)

# # #   C R E A T E   U R L S   # # #

urls = []
for p in range(pagesTotal):
    urls.append("https://www.iga.net/en/online_grocery/browse/in-promotion?page={}&pageSize=1000".format(p))

# # #   P A R S E   U R L S   # # #

itemCatalog = []

for url in urls:
    
    print("Working on URL:\n {}...".format(url))
        
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
            productSaleRatio = "{:2.4f}".format(productSaleRatio)
            productMetadataGroup = [
                productName,
                productCategory,
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
    
with open("igaSalesExport.csv", "a") as csv:
                
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
