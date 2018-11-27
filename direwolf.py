## direwolf.py
## Dean Mock
## Version: 19 Nov 2018


## Archived Backpage.com Escort Ads - Miami, 2014

import requests, json, re
from pprint import pprint
from bs4 import BeautifulSoup


#get user input so that they can initiate program?
#should this accept any user input at all? or just run automatically


# the URI of the page to scrape from
page_link_1 = "http://web.archive.org/web/20140703090808/http://miami.backpage.com:80/FemaleEscorts"
# display text while downloading the page
print("Downloading...")

# query the website and get the HTML
page_response_1 = requests.get(page_link_1, timeout=5)

#ensures the program halts if a bad download occurs
#if needed will print: There was a problem: 404 Client Error: Not Found
try:
	page_link_1.raise_for_status()
except Exception as exc:
	print('There was a problem: %s' % (exc))


# parse the html using Beautiful Soup and store in variable
page_content_1 = BeautifulSoup(page_response_1.content, "html.parser")

# Inspect the page attributes and call on the proper attributes
titles = page_content_1.find_all('div', attrs={'class': 'cat'})


### Archived Backpage.com Adult Jobs Ads - Miami, 2014

# the URI of the page to scrape from
page_link_2 = "http://web.archive.org/web/20140705210941/http://miami.backpage.com:80/AdultJobs"
# display text while downloading the page
print("Downloading...")

# query the website and get the HTML
page_response_2 = requests.get(page_link_2, timeout=5)

#ensures the program halts if a bad download occurs
#if needed will print: There was a problem: 404 Client Error: Not Found
try:
	page_link_2.raise_for_status()
except Exception as exc:
	print('There was a problem: %s' % (exc))


# parse the html using Beautiful Soup and store in variable
page_content_2 = BeautifulSoup(page_response_2.content, "html.parser")

# Inspect the page attributes and call on the proper attributes
titles = titles + page_content_2.find_all('div', attrs={'class': 'cat'})
pprint(titles)