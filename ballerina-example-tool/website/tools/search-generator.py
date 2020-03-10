#This script will scrape the html file content in the webroot
#and generate the search json file

from bs4 import BeautifulSoup
import os
import json

# The top argument for name in files
topdir = '.'

extens = ['html']  # the extensions to search for

found = {x: [] for x in extens}

# Directories to ignore
ignore = ['docs', 'ballerina-fonts','css','fonts','img','js','search','vs']

logname = "search_index.json"

print('Scraping files in %s for generating the search json' % os.path.realpath(topdir))

# The body of our log file
logbody = ''

data1 = "{\"docs\": ["

# Walk the tree
for dirpath, dirnames, files in os.walk(topdir):
    # Remove directories in ignore

    for idir in ignore:
        if idir in dirnames:
            dirnames.remove(idir)

    # Loop through the file names for the current step

    for name in files:
        # Split the name by '.' & get the last element
        ext = name.lower().rsplit('.', 1)[-1]

        if ext in extens:

            #Get URL path
            location = os.path.join(dirpath, name)
            found[ext].append(location)
            file = open(os.path.join(dirpath, name), "r")
            logbody = file.read()

            #parse the html
            soup = BeautifulSoup(logbody,"lxml")

            #get title of the page
            title = soup.title

            if title is not None:
                data1 = data1+ "{\"location\":\""+str(location)+"\""
                data1 = data1+",\"text\":\""+str(title.get_text())+"\""
                data1 = data1+ ", \"title\":\"" + str(title.get_text())+"\"},"

data1 = data1[:-1]
data1 = data1+"  ]}";

# Write results to the json file
with open(logname, 'w') as logfile:
    logfile.write(data1)
