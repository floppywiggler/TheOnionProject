# TheOnionProject
Using python to bulk check .onion sites and crawl for new ones

## Consists of two main scripts:
    sitechecker.py
    onioncrawler.py
    
 ## onioncrawler.py runs without any arguments.
 It will automatically start scraping for .onion addresses using beautifulsoup, and it will recursively follow these links for more links etc..
 
 ## sitechecker.py is used to validate onion links. 
 Can be used as a standalone script to validate links. Takes a file containing URLs as argument. Uses regex to extract http***.onion and *.onion strings.
 
 * Usage *
 ` python3 sitechecker.py test.list`
 
 The sitechecker will remove duplicates fed to it to avoid clogging up your pipe.
 
 # Remember that TOR is SINGLE THREADED, so you can easily jack your CPU up to a 100% with this script.
 
 
 ## This code is for educational purposes. I am not responsible for anything you do with this tool. Remember that these are "darkweb" links, and not everything you find is something you want to get near. There's even a good chance it's illegal. 
 
 # Use on own responsibility
