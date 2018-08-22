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
  - Create sample file
  - Get familiarize with data
  - Audit the data
  - Parse data into csv files
  - Clean the data
  
2. schema.py:
  - The top level schema of Database
  
3. csv files:
  - Data files parsed from osm data into five files to store in db
  
