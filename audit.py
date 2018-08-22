import re

sample_file = "sample_data_ontario.osm"
import xml.etree.cElementTree as ET

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

lower_list = set()
lower_colon_list=set()
problemchars_list=set()
other_list=set()

def key_type(element, keys):
    if element.tag == "tag":    
        if lower.search(element.attrib['k']):
            keys["lower"] +=1
            lower_list.add(element.attrib['k'])
        elif lower_colon.search(element.attrib['k']):
            keys["lower_colon"] +=1
            lower_colon_list.add(element.attrib['k'])
        elif problemchars.search(element.attrib['k']):
            keys["problemchars"] +=1
            problemchars_list.add(element.attrib['k'])
        else:
            keys["other"]+=1
            other_list.add(element.attrib['k'])
        
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        
    return keys

k = process_map(sample_file)
print(k)

