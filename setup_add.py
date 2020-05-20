#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-19 20:55:45
# @Author  : Felipe G. Ortega-Gama (felipeortegagama@gmail.com)
# @Version : 1.0

import sys
import json
import os

if len(sys.argv) < 2:
    print("Usage is: python3 setup_add.py <library#>")
    sys.exit(0)


library = int(sys.argv[1])


# ------------
# ------------
# ------------
# Extract library id from json file

with open('library.json') as json_file:
        data = json.load(json_file)
        libraryid = data['libraries'][library]['id']
        libraryname = data['libraries'][library]['name']
        librarydescription = data['libraries'][library]['description']

print("----------------------------------")
print("Adding bib entries to library: " + libraryname)
print(librarydescription)

# ------------
# ------------
# ------------
# Create shell script to post the entries to the ADS library

bibcodes = []

for filename in os.listdir('jsondir'):
    with open('jsondir/'+filename) as json_file:
        data = json.load(json_file)   
        bibcodes.append(data['response']['docs'][0]['bibcode'])

# print(bibcodes)

post_commandhead = 'curl -H "Authorization: Bearer $1" -H "Content-Type: application/json" '
post_commandhead += 'https://api.adsabs.harvard.edu/v1/biblib/documents/'
post_commandhead += libraryid
post_commandhead += ' -X POST -d '
post_commandhead += "'{"
post_commandhead += '"bibcode": ["'
post_commandtail = '"], "action": "add"}'
post_commandtail += "'\n"

with open('shell_ADS_post.sh', 'w') as shell_file:
    shell_file.write('#!/bin/bash\n')
    shell_file.write('\n\n\n')

    
    for bibcode in bibcodes:
        
        shell_file.write("echo Bibcode: " + bibcode + "\n" )
        shell_file.write(post_commandhead + bibcode +post_commandtail)
        shell_file.write("echo ----------------------------------\n")

