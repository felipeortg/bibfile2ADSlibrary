#!/bin/bash
# List the personal libraries in the ADS server

# Check the number of arguments
if [ "$#" -lt 1 ]; then
    echo "Usage is: list_libraries.sh <token>"
    exit 1
fi

curl -H "Authorization: Bearer $1" https://api.adsabs.harvard.edu/v1/biblib/libraries | python3 -m json.tool
