''' Classes and functions for parsing data sources (like XML) '''

import xml.etree.cElementTree as etree
from core.structures import PatternGroup

class Parser():
  ''' Parser for Pattern xml files. '''
  @staticmethod
  def parse_patterns(source, is_filepath=False):
    ''' Converts an XML file into a PatternGroup object. '''
    tree = None
    if is_filepath:
      tree = etree.parse(source).getroot()
    else:
     tree = etree.fromstring(source.strip())
    # build the entire structure through the PatternGroup constructor
    patterns = PatternGroup(tree)
    return patterns

class ExtensionParser():
  ''' Reader for extension files (type annotation). '''

  @staticmethod
  def parse(extensionfile):
    ''' Returns a dictionary with type_id and extension item attributes. '''
    # This gets fed into another function.
    # Could be improved by making it return a class object, rather than
    # just a mystery tuple.
    extensions = {}
    for line in extensionfile:
      if not line.startswith('#') and len(line) > 3:
        data = line.strip().split(';')
        print(data[1], data[2], data[3])
        extensions[data[0]] = (data[1], data[2], data[3])
    
    return extensions