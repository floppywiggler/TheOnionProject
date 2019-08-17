#!/usr/bin/python3
"""
This script will check a list of onion links if they are online or not.
Then returns a list with the pages that are online. 
"""

import subprocess
import os
from sys import argv, exit
from classes.bcolors import bcolors
from classes.query import checkIPs, checkLink, extrOnionLink


subprocess.call('clear')

linkList = []

print(bcolors.FAIL + "=" * 50 + bcolors.ENDC)
print(bcolors.OKGREEN + "Onion Link validator" + bcolors.ENDC)
print(bcolors.FAIL + "=" * 50 + bcolors.ENDC)

checkIPs()

try:
    filename = argv[1]
except:
    print(bcolors.FAIL + "I need a file with onion Links" + bcolors.ENDC)
    exit(1)


current_path = os.getcwd()
file_path = current_path + "/" + filename


with open(file_path) as f:
    content = f.readlines()

def remove_duplicates(linkLST):
    return list(set(linkLST))

content = [x.strip() for x in content]

for item in content:
    linkList.append(extrOnionLink(item))

clean_list = remove_duplicates(linkList)
with open('fulltext.list', 'a+') as fulltxt:
    fulltxt.writelines(clean_list)


for link in clean_list:
    try:
        checkLink(link)
        print( "-" * 50)
    except KeyboardInterrupt as escape:
        print("Exiting..")
        exit(1)

