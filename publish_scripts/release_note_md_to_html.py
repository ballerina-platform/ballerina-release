import os
import sys
import fnmatch
import jinja2
import markdown
import importlib
import requests
import json

if (len(sys.argv)!=2):
    print ('Please provide required arg <file path of realease note md file>')
    sys.exit()

importlib.reload(sys)
#sys.setdefaultencoding('utf8') //for pyhton 2..
TEMPLATE = """<div class="release_notes">
{{content}}
</div>
"""

filePath = sys.argv[1]
outputFile = 'RELEASE_NOTE.html'
subDir = "/target/output/"


def find():
    print ('Reading releaseNote md file from '+ filePath)
    with open(filePath, 'r') as content_file:
        md = content_file.read()
        extensions = ['extra', 'smarty']
        html = markdown.markdown(md, extensions=extensions, output_format='html5')
        doc = jinja2.Template(TEMPLATE).render(content=html)
        print ('Writing converted html content to .../target/output/'+ outputFile)
        baseDir = os.path.dirname(os.path.realpath(__file__))
        outputFile_loc = baseDir + subDir + outputFile
        os.makedirs(os.path.dirname(outputFile_loc), exist_ok=True)
        with open(outputFile_loc, 'w') as output_content_file:
            output_content_file.write(doc)

find()
