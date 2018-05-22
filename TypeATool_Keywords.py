# WHAT DOES THIS PROGRAM DO

# The user provides a definite number of the most important pages from a site.
# Using the SemRush API we programmatically extract 1 keyword per page.
# The output is presented in a CSV document
# The user is asked to review/correct/input the keywords that are not suitable or missing.
# The user review/corrects/inputs the keywords in the appropriate column and saves the changes to the CSV
# This provides the starting point: urls are associated with the keywords that they are supposed to rank for in Google
# this should be reviewed by the user to assure the keywords are suitable.

# INSIDE TERMINAL THE FOLLOWING MODULES MUST BE INSTALLED (see the comments in 'importing all the necessary modules' below)


# IMPORTING ALL THE NECESSARY MODULES

# pip install requests
import requests
# pip install bs4
# pip install BeautifulSoup4
from bs4 import BeautifulSoup
import csv


# DEFINING THE FUNCTIONS

# Define the SemRush function which will allow us to get the keywords for each URL


def semrush_keyword(soup):
    text = soup.find('body')
    keyword = 'no keyword'
    keyword = (((text.text).split(';'))[7]).split('\r\n')[1]
    return (keyword)

# DEFINING THE SOURCE AND DESTINATION CSV


# define the source csv with URLs
# INPUT THE SOURCE CSV FILE HERE
source_csv = 'INPUT THE SOURCE CSV FILE'

csv_reader_file = open(source_csv, encoding='UTF-8')
csv_reader = csv.reader(csv_reader_file, delimiter=',')
# skip first line in the csv
next(csv_reader)


# define destination CSV
# INPUT THE DESTINATION CSV FILE HERE
destination_csv = 'INPUT THE DESTINATION CSV FILE'

csv_writer_file = open(destination_csv, 'w', newline='')
csv_writer = csv.writer(csv_writer_file, delimiter=';')
# write the column headers for the destination csv
csv_writer.writerow(['url', 'keyword', 'user_keyword'])


# PREPARING OTHER SETTINGS

# prepare the source list that will store the URLs
source = []

# Prepare the settings for semrush API
# INPUT THE SEMRUSH API KEY HERE
semrush_key = 'INPUT THE SEMRUSH API KEY'

# define the rows in the source CSV
for row in csv_reader:
    # make a temporary dictionary to store current row
    r = {}
    r['url'] = row[0]
    # add temporary dictionary to source list/array
    source.append(r)


# EXTRACTING THE KEYWORDS

# For each URL in the source csv go through these lines of code: define the URL -
# call the semrush function and extract the keyword from the HTML of each URL with BS - append the keyword to the source list
# make sure that the keyword is left blank if Python throws any kind of exception so the user will be able to fill the missing keywords afterwards
for s in source:
    url = s['url']
    try:
        response = requests.get('http://api.semrush.com/?type=url_organic&key=' + semrush_key + '&display_limit=2&url=' + url + '&database=' + '')
        soup = BeautifulSoup(response.text, 'lxml')
        s['keyword'] = semrush_keyword(soup)
    except Exception:
        s['keyword'] = ''


# WRITING THE RESULTS INTO CSV

    csv_writer.writerow([s['url'], s['keyword'], ''])

# Closing the csv files

csv_reader_file.close()
csv_writer_file.close()
