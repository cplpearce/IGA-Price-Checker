# IGA-Price-Checker
### A simple python script to read all of IGA's online sales and report them by greatest discount!

#### You'll need to have python installed with:
```
  Beautiful Soup 4  : helps with parsing html text      : pip install bs4
  colorama          : colorama colors output!           : pip install colorama
  requests          : pulls apart URLs for juicy html   : pip install requests
```
  
#### Full import block for discrepancies:
    from colorama import Fore, Back, Style
    from bs4 import BeautifulSoup as bs
    from operator import itemgetter
    import requests
    import colorama
    import math
    import re

### Working setup on a remote server
##### https://repl.it/repls/OpulentShockingWorker
