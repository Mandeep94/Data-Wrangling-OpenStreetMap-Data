# Data-Wrangling-OpenStreetMap-Data

This project takes the data of ontario city from OSM site. Parses, audits, cleans and saves it in sqlite DB.

The city data used in this project can be found in the below link.
https://download.geofabrik.de/north-america/canada/ontario.html

The data is downloaded in the form of .osm file 
The structure and documentation of this can be found here
https://wiki.openstreetmap.org/wiki/OSM_XML

Since the data is almost over 13GB. I created a sample file from this data 
and ran parse osm to csv functions over this sample file for validation 
After that I passed the full data through these functions 
and stored this in five separate csv files
These files then i loaded into database with the schema found in schema.py file

All the process from creating sample file to converting into csv and then cleaning data 
can be found in jupyter notebook. and the full documentation in the pdf file.

1. Data Wrangling.ipynb:
  step-by-step process from sampling to parse and clean the data

2. sampling.py:
  Samples data from full city osm file of 13GB to 13MB

3. audit.py:
  Audits the tags in sample data

4. audit_street_names.py:
  Audits the street names in data

5. parsing.py:
  Parses the osm data into 5 different csv files

6. schema.py:
  The schema used in parsing the data
  
7. cleanup.py:
  Clean the data for issues found in audit process

8. create_table.sql:
  sql script with create table commands for DB
  
9. Data Wrangling OSM Data.pdf:
  
  
