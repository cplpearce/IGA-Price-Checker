# IGA-Price-Checker
### A simple python script to read all of IGA's online sales and report them by greatest discount!
# Update June 2020
#### Well, well, well IGA, it seems you've finally come to terms with anti-scraping measures.  Here's a selenium script to break their bot detection.  This will require a driver (chromedriver (chrome) or geckodriver (firefox)) and understanding of local PATH'ing.  There have also been numerous changes and improvements.  Enjoy!

#### You'll need to have python installed with:
```
  Beautiful Soup 4  : helps with parsing html text      : pip install bs4
  requests          : pulls apart URLs for juicy html   : pip install requests
  Chrome/FF Driver  : pulls the html for bs4 to break apart
```
  
#### Full import block for discrepancies:
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
