#!/bin/bash
# Add the entries of a bib file to a private ADS library
# Later all entries can be downloaded as a bibfile with the ADS format

# Check the number of arguments
if [ "$#" -lt 2 ]; then
    echo "Usage is: main_script.sh <token> <bib_file> [<library#>]"
    exit 1
fi

# Write here your ADS token used for the API
# More info in: https://github.com/adsabs/adsabs-dev-api
token=$1

bibfile=$2

# By default the bibfiles are added to the first library
if [ "$#" -gt 2 ]; then
    library=$3
else
    library=0
fi

# articles in Mendeley generated library
echo "Number of Bib entries in BibTex File:"
read elem <<< $(grep '@' $bibfile | wc -l)
echo $elem

# articles in Mendeley generated library with arxivId
echo "----------------------------------"
echo "Number of Bib entries in BibTex File with arxivId:"
grep 'arxivId' $bibfile | wc -l

# Check if all articles in Mendeley at least have title
echo "----------------------------------"
echo "Number of Bib entries in BibTex File with title:"
grep 'title =' $bibfile | grep -v 'booktitle' | wc -l

# Create a shell script from the Bib file to search in the ADS database 
python3 bib_entries_and_setup_search.py $bibfile $elem || exit 1

# Search in the ADS library and get the ADS Bibcodes
sh shell_ADS_search.sh $token

# Get the id of the ADS library where we want to add the files
curl -H "Authorization: Bearer $token" https://api.adsabs.harvard.edu/v1/biblib/libraries | python3 -m json.tool > library.json

# Create a shell script to add the found Bibcodes to the personal ADS library
python3 setup_add.py $library || exit 1

# Post the files to the personal ADS library 
sh shell_ADS_post.sh $token


if test -f "manually_add.txt"; then
    echo "----------------------------------"
    echo "Number of Bib entries that need manual handling"
    wc -l manually_add.txt
fi
 

# Clean the mess
rm -r jsondir
rm library.json
rm shell_ADS_search.sh
rm shell_ADS_post.sh


