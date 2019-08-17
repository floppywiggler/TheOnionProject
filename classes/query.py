import re
import urllib3
import json
from urllib3.contrib.socks import SOCKSProxyManager
from bs4 import BeautifulSoup
from classes.bcolors import bcolors

## DATABASE HANDLING ##
import sqlite3
conn = sqlite3.connect('onion.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS onionsites (URL, Title , Status, Status_code, last_checked)")
##  END DATABASE HANDLING ##

def checkIPs():
    """
    This funciton checks first the Public IP and then the TOR IP and prints them out.
    """

    proxy = SOCKSProxyManager('socks5h://localhost:9050/')
    http = urllib3.PoolManager()
    myip = http.request('GET', 'http://httpbin.org/ip')

    try:
        global torIP
        torIP = proxy.request('GET', 'http://httpbin.org/ip')
    except NameError:
        print(bcolors.FAIL + "proxy isn't running or address:port is wrong.\nScript will exit." + bcolors.ENDC)
        exit(1)

    jsonIP =json.loads(myip.data.decode('utf-8'))
    jsonTorIP = json.loads(torIP.data.decode('utf-8'))

    print("Your real IP Address is: " + bcolors.OKBLUE + jsonIP["origin"] + bcolors.ENDC)
    print("Your Tor IP Address is: " + bcolors.FAIL + jsonTorIP["origin"] + bcolors.ENDC)
    print(bcolors.FAIL + "="*50 + bcolors.ENDC)

def checkLink(link):
    try:
        proxy = SOCKSProxyManager('socks5h://localhost:9050/')
        websiteObj = proxy.request('GET', link, timeout=3.0)
        response_code = websiteObj.status
        sitedata = websiteObj.data
        soup = BeautifulSoup(sitedata, "html.parser")
        siteTitle = soup.title.string
    except:
        response_code = 500
        pass

    if response_code >= 200 and response_code < 404:
        status = 'OK'
        print("Title:", bcolors.WARNING + siteTitle + bcolors.ENDC)
        print("Link: ", bcolors.OKBLUE + link + bcolors.ENDC, "\nStatus:", bcolors.OKGREEN + status + bcolors.ENDC)
        c.execute("INSERT INTO onionsites VALUES (?, ?, ? , ?, ?)", (link, siteTitle,status,response_code,'datetime')) # Storing all the results
    elif response_code == 500:
        status = 'Failed'
        print("Status code:", response_code)
        print("Link: ", bcolors.FAIL + str(link) + bcolors.ENDC, "\nStatus:", bcolors.FAIL + status + bcolors.ENDC )
        c.execute("INSERT INTO onionsites VALUES (?, ?, ? , ?, ?)", (link, 'N/A',status,response_code,'datetime')) # Storing all the results
    #else:
     #   print("Response code:", response_code)


def extrOnionLink(link):
    try:

        pattern = re.compile(r'(^http...+.onion)')
        matchObj = re.search(pattern, str(link))
        link = matchObj.group()
        return link
    except AttributeError as e:
        pass






"""
#test function work.

def checkLink2(link):
    try:
        http = urllib3.PoolManager()
        websiteObj = http.request('GET', link)
        response_code = websiteObj.status
    except:
        response_code = 500
        pass

    if response_code >= 200 and response_code <= 299:
        status = 'OK'
        print("Link: ", link, "\nStatus:", bcolors.OKGREEN + status + bcolors.ENDC )
    elif response_code >= 500:
        status = 'Failed'
        print("Link: ", link, "\nStatus:", bcolors.FAIL + status + bcolors.ENDC )
"""
