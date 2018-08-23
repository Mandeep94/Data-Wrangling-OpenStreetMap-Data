import csv
import codecs
import pprint
import cerberus
import schema
import xml.etree.cElementTree as ET
from collections import defaultdict
sample_file = "sample_data_ontario.osm"
osm_file = "ontario.osm"

def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w', encoding="ISO-8859-1") as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:
        
        codecs.getincrementalencoder("utf-8")()

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])



NODES_PATH = 'nodes.csv'
NODE_TAGS_PATH = 'nodes_tags.csv'
WAYS_PATH = 'ways.csv'
WAY_NODES_PATH = 'ways_nodes.csv'
WAY_TAGS_PATH = 'ways_tags.csv'

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['changeset', 'id',  'timestamp', 'version']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

position = 0

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = validator.errors.items()
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        try:
            super(UnicodeDictWriter, self).writerow({
            k:v for k, v in row.items()
        })
        except:
            pass

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    global position

    for elem in element.iter():
        if elem.tag == 'node': #['id', 'lat', 'lon', 'version', 'timestamp', 'changeset']
            node_attribs = {k:elem.attrib[k] for k in elem.keys()}
            tags=[]
            for sub_elem in elem:
                tag_dict = {}
                tag_dict["id"] = elem.attrib["id"]
                tag_type = sub_elem.attrib['k'].split(':')
                if len(tag_type)>1:
                    tag_dict["key"] = tag_type[1]
                    tag_dict["type"] = tag_type[0]
                else:
                    tag_dict["key"] = sub_elem.attrib['k']
                    tag_dict["type"] = default_tag_type
                tag_dict["value"] = sub_elem.attrib["v"]
                tags.append(tag_dict)
            return {'node': node_attribs, 'node_tags': tags}
        elif elem.tag == 'way':
            way_attribs = {}
            way_attribs["id"] = elem.attrib["id"]
            way_attribs["version"] = elem.attrib["version"]
            way_attribs["changeset"] = elem.attrib["changeset"]
            way_attribs["timestamp"] = elem.attrib["timestamp"]
            tags=[]
            way_nodes=[]
            nd_position = 0
            for sub_elem in elem: 
                if sub_elem.tag == 'tag':
                    tag_dict = {}
                    tag_dict["id"] = elem.attrib["id"]
                    tag_type = sub_elem.attrib['k'].split(':')
                    if len(tag_type) >1:
                        tag_dict["key"] = tag_type[1]
                        tag_dict["type"] = tag_type[0]
                    else:
                        tag_dict["key"] = sub_elem.attrib['k']
                        tag_dict["type"] = default_tag_type
                    tag_dict["value"] = sub_elem.attrib["v"]
                    tags.append(tag_dict)
                elif sub_elem.tag == 'nd':
                    nd_dict = {}
                    nd_dict["id"] = elem.attrib["id"]
                    nd_dict["node_id"] = sub_elem.attrib["ref"]
                    nd_dict["position"] = nd_position
                    nd_position +=1
                    way_nodes.append(nd_dict)
            return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

process_map(osm_file, validate=True)
