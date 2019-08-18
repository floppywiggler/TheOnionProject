# MappingTheOnion
These scripts serve a simple purpose: To populate a database with as much **live** .onion hosts as possible.
## A warning: 
This script will keep on crawling for as long as you tell it to, and won't discriminate content. **You** are responsible for what sites you end up collecting when running this tool.

## Consists of two main scripts:
    sitechecker.py
    onioncrawler.py
    
 ## onioncrawler.py runs without any arguments.
 It will automatically start scraping for .onion addresses using beautifulsoup, and it will recursively follow these links for more links etc.. The dread forum is for now the start site.
 
 ## sitechecker.py is used to validate onion links. 
 Can be used as a standalone script to validate links. Takes a file containing URLs as argument. Uses regex to extract http***.onion and *.onion strings.* When live host is found, it's added to the "onion.db" database along with the Title of the page, status (OK/other) and status code (200/403/etc) for easy retrieval.
 
 * Usage 
 ` python3 sitechecker.py test.list`
 
 The sitechecker will remove duplicates fed to it to avoid clogging up your pipe.
 
 Remember that TOR is SINGLE THREADED, so you can easily jack your CPU up to a 100% with this script.
 
 ## This code is for educational purposes. I am not responsible for anything you do with this tool. Remember that these are "darkweb" links, and not everything you find is something you want to get near. There's even a good chance it's illegal. 
 
 # Use on own responsibility
