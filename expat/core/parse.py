''' Classes and functions for parsing data sources (like XML) '''

import xml.etree.cElementTree as etree
from core.structures import PatternGroup

class Parser():
  @staticmethod
  def parse_patterns(source, is_filepath=False):
    tree = None
    if is_filepath:
      tree = etree.parse(source).getroot()
    else:
     tree = etree.fromstring(source.strip())
    # build the entire structure through the PatternGroup constructor
    patterns = PatternGroup(tree)
    return patterns

class ExtensionParser():
  @staticmethod
  def parse(extensionfile):
    extensions = {}
    for line in extensionfile:
      if not line.startswith('#') and len(line) > 3:
        data = line.strip().split(';')
        extensions[data[0]] = (data[1], data[2])
    
    return extensions