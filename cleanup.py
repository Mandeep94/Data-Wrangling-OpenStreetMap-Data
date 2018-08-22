import os
import csv



sample_file = "sample_data_ontario.osm"
osm_file = "ontario-latest.osm"
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Pl": "Place",
            "Dr": "Drive",
            "Ct": "Court",
            "Sq": "Square",
            "Sq.": "Square",
            "Rd": "Road",
            "Rd.": "Road",
            "Pky": "Parkway",
            "Pkwy": "Parkway"
            }

def update_name(name, mapping):
    for n in name.split():
        if n in mapping:
            name=name.replace(n,mapping[n])
            break       
    return name



rd = open("ways_tags.csv", 'r')
wt = open("temp_data.csv", 'w')
main_file = csv.DictReader(rd)
temp = csv.writer(wt)
temp.writerow(['id','key','value','type'])
for r in main_file:
    if r['key'] == 'street' and r['type'] == 'addr':
        r['value'] = update_name(r['value'], mapping)
    temp.writerow([r['id'], r['key'], r['value'], r['type']])

rd.close()
wt.close()
os.replace('temp_data.csv', 'ways_tags.csv')