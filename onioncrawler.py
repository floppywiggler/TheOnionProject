#!/usr/bin/env python

print("[*] Starting TORSpider...")

import multiprocessing
import pickle
import requests_html
import argparse
from classes.bcolors import bcolors
import re

global url

def get_titles():
	print("Loaded get_titles function")
	title_link = {}
	with open("short.pickle", 'rb') as s:
		domains = pickle.load(s)

	session = requests_html.HTMLSession()

	while True:
		try:
			url = domains[0]
			domains = domains[1:]
			response = session.get(url, proxies={'http': '127.0.0.1:8118'})
			title = response.html.find("title")[0].text
			title_link[url] = title

		except IndexError:
			break

		except Exception as e:
			print(str(e))
			break

	with open('titles.pickle', 'wb') as t:
		pickle.dump(title_link, t)

	print("Finished titles")


def get_domains():
	"""
	This script helps with a personal project for which the
		hidden-spider was made. This script will take the
		finished queue ('full.pickle') and get the domain names
		of the websites and store them in a new pickle file ('short.pickle')
	"""
	print("Loaded get_domains function!")
	# Open full.pickle
	with open('full.pickle', 'rb') as f:
		finished_list = pickle.load(f)

	# Check if index is in the url, if so, go ahead and add it
	non_domains_homepage = list(filter(lambda x: 'index' in x, finished_list))
	fin = []
	for url in non_domains_homepage:
		if url not in finished_list:
			fin.append(url)

	# Using map, get just the domain names of every link
	domains = map(lambda x: "/".join(x.split('/')[:3]), fin)


	# Take the list from map and turn it into a set (to remove dups)
	domains = str(domains) + str(non_domains_homepage)
	domains = list(set(domains))



	# Change the set back into a list and pickle it into 'short.pickle'
	with open('short.pickle', 'wb') as s:
		pickle.dump(domains, s)



	print(bcolors.OKGREEN + "finished with domains! Moving to titles.." + bcolors.ENDC)
	get_titles()

parser = argparse.ArgumentParser()

parser.add_argument('--domains', help='Get domains')
parser.add_argument('--titles', help='Get titles')

args = parser.parse_args()

if args.domains:
	get_domains()

if args.titles:
	get_titles()


def saveProgramState(queue_list, finished_list):

	# Save the queue as a pickle object to save loading
	# 	time as byte streams load much quicker than
	# 	text, and due to the possible large queue file
	#
	# Another advantage to using pickle is to have the data
	#	already set up as the list python object
	with open('queue.pickle', 'wb') as q:
		pickle.dump(queue_list, q)

	with open('full.pickle', 'wb') as f:
		pickle.dump(finished_list, f)


def parseNewLinks(links):
	# Since this is an .onion crawler, we need to make sure
	#	the sites we add to the queue are actually .onion HTML
	#	websites
	passed = list(filter(lambda x: x.split("/")[0] == 'http:' or x.split("/")[0] == 'https:', links))
	passed = list(filter(lambda x: x.split("/")[2][-6:] == '.onion', passed))

	return set(passed)


def main():

	# check to make sure the program does not need to resume
	# 	from a previous session
	# 	check for the files to run the program in the directory
	# 	if they are not found, create them
	# TODO:
	# 	Hash the data to make sure the data is correct when it
	# 	is loaded again (unless the module does that for us.. not real sure)
	try:
		global q
		global f
		q = open("queue.pickle", 'rb')
		f = open("full.pickle", 'rb')
		# Add a hash check here
		queue_list = pickle.load(q)
		finished_list = pickle.load(f)

	except IOError:
		# If it is a clean start, begin on the front page of the
		# 	Hidden Wiki (link active as of October 2018)
		queue_list = ["http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page"]
		finished_list = []

		q = open("queue.pickle", 'wb')
		f = open("full.pickle", 'wb')

	finally:
		q.close()
		f.close()

	session = requests_html.HTMLSession()
	print(bcolors.OKGREEN + "[*] Starting to crawl..." + bcolors.ENDC)

	while True:
		# Loop until there is nothing left in the queue
		try:
			url = queue_list[0]
			queue_list = queue_list[1:]

			print(bcolors.HEADER + "[*] Crawling website: %s..." % url + bcolors.ENDC)
			response = session.get(url, proxies={'http': '127.0.0.1:8118'})

			# The default object type of absolute_links is
			# 	a non-iterable 'set' object. Turn it into a list
			# 	to be able to iterate over it
			found = list(response.html.absolute_links)

			print(bcolors.OKGREEN + "\t[*] Found %s links" % len(found) + bcolors.ENDC)
			new_to_crawl = parseNewLinks(found)
			finished_list.append(url)
			queue_list = list((set(queue_list).union(new_to_crawl)).difference(set(finished_list)))

			with open('domains.list', 'a+') as domainstxt:
				for line in found:
					domainstxt.write(line)
					domainstxt.write('\n')
					print(bcolors.OKBLUE + 'Wrote ' + str(line) + ' to txt' + bcolors.ENDC)

		except TypeError:
			# this would be the end of the queue
			saveProgramState(finished_list, queue_list)
			break

		except ConnectionError:
			print(bcolors.FAIL + "[*] Could not connect to %s... Continuing..." % url + bcolors.ENDC)
			pass

		except KeyboardInterrupt:
			print(bcolors.WARNING + "[*] Keyboard Interrupt...\n[*] Exiting..." + bcolors.ENDC)
			saveProgramState(queue_list, finished_list)
			break

		except Exception as e:
			print(str(e))
			saveProgramState(queue_list, finished_list)


	print(bcolors.OKGREEN + "[*] Crawling is complete... " + bcolors.ENDC)
	print("[---] Now getting domains for all the URLs!: ")
	get_domains()

def extrOnionLink(file):
	with open(file, 'r+') as of:
		pattern = re.compile(r'(.+.onion)')
		matchObj = re.search(pattern, str(file))
		link = matchObj.group(1)
		return link


if __name__ == '__main__':
	main()

# http://zqkrlwi4fecvo6ri.onion/wiki/index.php/Main_Page













