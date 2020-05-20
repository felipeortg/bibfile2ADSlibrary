# bibfile2ADSlibrary

Add the entries from a BibTeX file .bib to your [ADS](https://ui.adsabs.harvard.edu/) library.

To use execute the bash script from the command line
```bash
main_script.sh <token> <bib_file> [<library#>]
```
where token is your personal ADS API token, more info can be found [here.](https://github.com/adsabs/adsabs-dev-api)
You can choose which library is getting the bib entries with the library# variable.
To list the libraries in your account you can run the bash script
```bash
list_libraries.sh <token>
```
The library numeration begins with 0.