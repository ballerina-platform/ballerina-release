import os
import sys
import fnmatch
import jinja2
import markdown


reload(sys)
sys.setdefaultencoding('utf8')
TEMPLATE = """<div class="release_notes">
{{content}}
</div>
"""

baseDir = '/var/www/html/products/downloads'
releaseNoteFile = '*ballerina-release-notes-*.md'
outputFile = 'RELEASE_NOTE.html'

if len(sys.argv) > 1:
    topdir = sys.argv[1]
else:
    topdir = '.'

print 'Base directory : ' +baseDir

def find(pattern, path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                print 'Reading release note md file from '+ os.path.join(root, name)
                with open(os.path.join(root, name), 'r') as content_file:
                    md = content_file.read()
                    extensions = ['extra', 'smarty']
                    html = markdown.markdown(md, extensions=extensions, output_format='html5')
                    doc = jinja2.Template(TEMPLATE).render(content=html)
                    print 'Writing converted html content to '+ os.path.join(root, outputFile)
                    with open(os.path.join(root, outputFile), 'w') as output_content_file:
                        output_content_file.write(doc)

find(releaseNoteFile, baseDir)