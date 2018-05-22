# WHAT DOES THIS PROGRAM DO

# The is based on the TypeATool_Keywords program as it gets the necessary information from there (in the form of a csv) - so it is not possible to use this program by itself,
# except if a csv with urls and keywords is provided beforehand.
# With the ‘site: command search’ we search the website for each keyword and extract the first 10 results from google search.
# This step allows us to verify if the URL the keyword was associated with is among the results. It also tells us which pages are ranking for the given keyword in Google.
# If the URL is not among the results, then it should be optimized for the keyword it was associated with.
# In the next step we extract all the existing links from every google result page, so now we have an x number of URLs per google result URL.
# This step is important to get an insight of the internal linking structure of the page.
# We verify if the URL associated with the keyword is present in any of the links we pulled from the google result pages.
# The pages ranking for identical keywords should be internally linked
# Finally the pages from the google search results are sorted according to the presence of the main URL link on the page.
# The results are stored in 2 final CSVs - one is a detailed version with all the information we got while extracting the data, the other is a simpler

# REQUIREMENTS
# PYTHON 3.6
# INSIDE TERMINAL THE FOLLOWING MODULES MUST BE INSTALLED (see the comments in 'importing all the necessary modules' below)

# IMPORTING ALL THE NECESSARY MODULES

import csv
#pip install beautifulsoup4
# pip install bs4
from bs4 import BeautifulSoup
# pip install google-api-python-client
from googleapiclient.discovery import build
#pip install linkGrabber
import linkGrabber
from linkGrabber import Links
import pprint
#pip install requests
import requests
import unicodedata


# DEFINING THE FUNCTIONS

# Define the GoogleSearh function


def google_search(search_term, api_key, cse_id, **kwargs):
    # Construct a Resource for interacting with an API. Returns A Resource object with methods for interacting with the service
    try:
        service = build("customsearch", "v1", developerKey=api_key)
    # cse() Applying the Returns the cse Resource (cse method).Returns metadata about the search performed,
    # metadata about the custom search engine used for the search, and the search results. (list method)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res['items']
    except Exception:
        return 'no result'

# Define the function to get links


def get_links(url):
    try:
        links = linkGrabber.Links(url)
        l = links.find()
    except Exception:
        l = ''
    return l


# DEFINIGN THE API SETTINGS


# Set up the Search Engine settings
search_engine_id = 'INPUT THE SEARCH ENGINE ID'
api_key = 'INPUT THE GOOGLE SEARCH API'

# DEFINING SOURCE AND DESTINATION CSVs

# define the source csv with URLs
# INPUT SOURCE CSV FILE HERE
source_csv = 'INPUT SOURCE CSV FILE HERE'

csv_reader_file = open(source_csv, encoding='UTF-8')
csv_reader = csv.reader(csv_reader_file, delimiter=';')
# skip first line in the csv
next(csv_reader)

# Define the destination CSV for the detailed report
# INPUT DESTINATION CSV FILE FOR DETAILED REPORT HERE
detailed_report_destination = 'INPUT DESTINATION CSV FILE FOR DETAILED REPORT HERE'

csv_writer_file = open(detailed_report_destination, 'w', newline='')
csv_writer = csv.writer(csv_writer_file, delimiter=';')
# write the column headers for the destination csv
csv_writer.writerow(['URL', 'PROG KEYWORD', 'USER KEYWORD', 'GOOGLE SEARCH RESULTS', 'PAGE RANKING IN GOOGLE FOR SELECTED KEYWORD?', 'NEED TO OPTIMIZE FOR SELECTED KEYWORD?', 'LINKS IN THE GOOGLE SEARCH RESULTS PAGES', 'INTERNAL LINKING?'])

# Define the destination CSV for the quick report
# INPUT DESTINATION CSV FILE FOR SIMPLE REPORT HERE
simple_report_destination = 'INPUT DESTINATION CSV FILE FOR SIMPLE REPORT HERE'

csv_writer_file2 = open(simple_report_destination, 'w', newline='')
csv_writer2 = csv.writer(csv_writer_file2, delimiter=';')
# write the column headers for the destination csv
csv_writer2.writerow(['URL', 'SELECTED KEYWORD', 'PAGE RANKING IN GOOGLE FOR SELECTED KEYWORD?', 'NEED TO OPTIMIZE FOR SELECTED KEYWORD?', 'GOOGLE SEARCH RESULTS'])


# PREPARING OTHER SETTINGS

# define the URL of the website you want to search
# INPUT WEBSITE URL HERE
site = 'INPUT WEBSITE URL HERE'

# Prepare the list that will store all the links from the pagees of the Google Search results
links_all = []


# EXECUTING GOOGLE SITE SEARCH

# Go through all the URLs in the source CSV: - if the keyword was input manually, pick that, else, pick the programmaticaly defined keyword -
# call the Google Search function - create the URL by concatenating the site search, site and keyword and inputing the api key and search engine ID
# limiting the number of results to 10
for item in csv_reader:
    if item[2] == '':
        results = google_search('site:' + site + ' ' + "'" + item[1] + "'", api_key, search_engine_id, num=10)
    else:
        results = google_search('site:' + site + ' ' + "'" + item[2] + "'", api_key, search_engine_id, num=10)

    if results == 'no result':
        print (site)
        continue

    # Prepare a list for storing the results
    r1 = []
    # Go through all the results and choose which result from the google search to store, in this case we chose 'link' as we want to store the urls -
    # store the results into the previously prepared list r1= [], so we can use it later
    for result in results:
        r1.append(result['link'])

    # Go through all the urls in the r1 list - make a dictionary to store all the items we will need later and give them appropriate names for the keys
    for google_res in r1:

        r = {}
        r['url'] = item[0]
        r['prog_keyword'] = item[1]
        r['user_keyword'] = item[2]
        r['googles_results'] = google_res

        # Verify if the original url is among the google search results - create 2 additionnal keys for the dictionary
        # add values according to the presence of the URL in the google search results - if the URL is among the GSR the page is ranking in google for the given keyword
        # and does not need optimizing, else it is not ranking and it does need optimizing
        if r['url'] in r1:
            r['ranking in google'] = 'page ranking for given keyword'
            r['need to optimize for selected keyword'] = 'no'
        else:
            r['ranking in google'] = 'page not ranking for given keyword'
            r['need to optimize for selected keyword'] = 'yes'


# EXTRACTING THE LINKS

        # Now we want to get all the links for each page we got with the Google search function
        # we call the get links function and go through every url we got from the google search
        # We store the links into the previously prepared list so we can easily access them
        # We veruify if the original url is among the extracted links: if it is, then the page is internaly linked, else is not and should be
        links = get_links(r['googles_results'])
        for l in links:
            all_links = l['href']
            links_all.append(all_links)
            if r['url'] in links:
                r['link present'] = 'yes'
            else:
                r['link present'] = 'no'

# WRITING THE DATA TO CSVs

        # Finally we write all the data into a CSV named detailed report, which will have all the data we extracted
        csv_writer.writerow([r['url'], r['prog_keyword'], r['user_keyword'], r['googles_results'], r['ranking in google'], r['need to optimize for selected keyword'], links_all, r['link present']])

    # We write a smaller amount of data to another CSV named quick report, which will sum up all the data
    if r['user_keyword'] != '':
        csv_writer2.writerow([r['url'], r['user_keyword'], r['ranking in google'], r['need to optimize for selected keyword'], r1])
    else:
        csv_writer2.writerow([r['url'], r['prog_keyword'], r['ranking in google'], r['need to optimize for selected keyword'], r1])

csv_reader_file.close()
csv_writer_file.close()
csv_writer_file2.close()
