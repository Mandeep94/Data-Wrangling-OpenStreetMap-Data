# samples the xml file by taking the kth element for sample.

import xml.etree.cElementTree as ET

sample_file = "sample_data_ontario.osm"
osm_file = "ontario-latest.osm"

k=1000
def get_element(osm_file, tags=('node', 'way', 'relation')):
    
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()
            
with open(sample_file, 'wb') as output:
    output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write(b'<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(osm_file)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write(b'</osm>')