#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-19 20:55:45
# @Author  : Felipe G. Ortega-Gama (felipeortegagama@gmail.com)
# @Version : 1.0


import sys
from urllib.parse import urlencode, quote_plus


if len(sys.argv) < 3:
    print("Usage is: bib_entries_and_setup_search.py <bibfile> <#entries>")
    sys.exit(0)

# Function to extract info of a .bib file
def save_entry(lines):
    dict_var = dict()
    for line in lines:
        equals_pos = line.find('=')
        
        key_pos = equals_pos
        entry_pos = equals_pos
        entry_end = len(line)
        
        for posit in range(1,equals_pos):
            if line[equals_pos-posit] == ' ':
                key_pos-=1
                continue
            else:
                break
        
        for posit in range(1,entry_end-equals_pos):
            char = line[equals_pos+posit]
            if char == ' ' or char == '{':
                entry_pos+=1
                continue
            else:
                break
        for posit in range(1,len(line)):
            char = line[-posit]
            if char == ' ' or char == '}' or char == ',' or char == '\n':
                entry_end-=1
                continue
            else:
                break
 
#         print(key_pos,entry_pos,entry_end) 
        key = line[:key_pos]
        entry = line[entry_pos+1:entry_end]
        
        dict_var[key] = entry
            
    return dict_var



# ------------
# ------------
# ------------

# Extract info of a .bib file
orig_bib_file = str(sys.argv[1])
num_entries = int(sys.argv[2])

# Bib entries
bib = []

with open(orig_bib_file, 'r') as f:
    buffer = []
    bib_entry = dict()
    in_entry = False
    for line in f:
        if line[0] == '@':
            in_entry = True
            continue
        elif line[0] == '}':
            bib.append(save_entry(buffer))
            in_entry = False
            buffer = []
            bib_entry = dict()
            continue
            
        if in_entry:
            buffer.append(line)

print("----------------------------------")
if (len(bib) == num_entries):
    print('Success extracting info of all ' + str(len(bib)) +' bib entries')
else:
    print('Was only able to extract ' + str(len(bib)) +' bib entries out of ' + str(num_entries))


# ------------
# ------------
# ------------
# Create a shell script to search each entry in the ADS data base

search_commandhead = 'curl -H "Authorization: Bearer $1" "https://api.adsabs.harvard.edu/v1/search/query?q=identifier%3A'

failed_titles = []
failed_info = []

with open('shell_ADS_search.sh', 'w') as shell_file:
    shell_file.write('#!/bin/bash\n')
    shell_file.write('rm -r jsondir\n')
    shell_file.write('mkdir jsondir\n')
    
    for ii, entry in enumerate(bib):
        
        search_commandtail = '&fl=bibcode" | python -m json.tool > jsondir/entry' + str(ii) + '.json\n'
        try:
            query = {"":bib[ii]['arxivId']}
            encoded_query = urlencode(query,quote_via=quote_plus)
            shell_file.write(search_commandhead + encoded_query[1:] + search_commandtail)
        except:
            failed_titles.append(bib[ii]['title'])
            failed_info.append([bib[ii]['title'],bib[ii]['author'],bib[ii]['year']])


if len(failed_titles) > 0:
    print("----------------------------------")
    print("----------------------------------")
    print("¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
    print(" ")
    print(" ")
    print('Articles that do not have arXiv Id and have to be added manually:')
    for art in failed_titles:
        print('* ' + art)
    with open('manually_add.txt', 'w') as failed_entries_file:
        for info in failed_info:
            failed_entries_file.write(str(info)+'\n')
    print('Title, author, and year saved into manually_add.txt')
    print(" ")
    print(" ")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("----------------------------------")
    print("----------------------------------")

