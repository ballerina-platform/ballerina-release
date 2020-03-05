#This script will scrape the html file content in the webroot
#and generate the search json file

from bs4 import BeautifulSoup
import os
import io
import json
import sys
import re
import shutil
from mkdocs import utils


# The top argument for name in files
if len(sys.argv) > 1:
    topdir = sys.argv[1]
else:
    topdir = '.'

output_dir = os.path.join(topdir,"search")
outputjson = os.path.join(output_dir,"search_index.json")
search_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"search.js")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
print('Copying '+search_js_path+' to ' + output_dir)
shutil.copy2(search_js_path, output_dir)

os.chdir(topdir)

extens = ['html']  # the extensions to search for

found = {x: [] for x in extens}

# Directories to ignore
ignore = ['docs', 'ballerina-fonts','css','fonts','img','js','search','vs']



print('Scraping files in %s for generating the search json' % os.path.realpath(topdir))

# The body of our log file
logbody = ''
index = 0
searchData = { 'docs' :[]}
addedHashes = []

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
            file = io.open(os.path.join(dirpath, name), 'r', encoding='utf8')
            logbody = file.read()

            #parse the html
            soup = BeautifulSoup(logbody,"lxml")

            #get title of the page
            title = soup.title

            page_details = soup.find_all(["p", "pre", "h1", "h2" , "h3", "h4"])
            for detail in page_details:
                text = detail.get_text()
                text = text.replace('\u00a0', ' ')
                text = re.sub(r'[ \t\n\r\f\v]+', ' ', text.strip())
                text = utils.text_type(text.encode('utf-8'), encoding='utf-8')
                if (text and str(os.path.relpath(location))):
                    hashVal = abs(hash((str(os.path.relpath(location)), text, str(title.get_text()))))
                    if hashVal not in addedHashes:
                        currentPage = {
                            'location' : str(os.path.relpath(location)),
                            'text' : text,
                            'title' : str(title.get_text()),
                            'index' : hashVal
                        }
                        addedHashes.append(hashVal)
                        searchData['docs'].append(currentPage)

# Write results to the json file
with open(outputjson, 'w') as logfile:
    json.dump(searchData, logfile)