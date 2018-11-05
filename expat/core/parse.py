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