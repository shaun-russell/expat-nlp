# todo
# read xml file
# create pattern, group, and word classes
# populate defaults

import xml.etree.cElementTree as etree
# import lxml

# use this as a placeholder for properties
NULL = None

class Parser():
  @staticmethod
  def parse_patterns(source):
    tree = None
    if isinstance(source, str):
      # source is a string, use string parse
     tree = etree.fromstring(source.strip())
    else:
      # assume file so read from that
      tree = etree.parse(source)
    # build the entire structure through the PatternGroup constructor
    patterns = PatternGroup(tree)
    return patterns

class PatternGroup():
  def __init__(self, tree):
    self.label = tree.find('label')
    self.version = tree.find('version')
    # pattern object for every child element
    self.patterns = [Pattern(child) for child in tree.getchildren()]

class Pattern():
  ''' Represents a pattern of words. '''
  def __init__(self, tree):
    self.name = tree.get('name')
    self.description = tree.get('description')
    # 'class' is a protected word in python, so the field is 'classname'
    self.classname = tree.get('class')
    self.priority = int(tree.get('priority'))
    self.label = tree.get('label')
    # create the correct object for the child elements of the pattern
    self.children = [self._parse_contents(el) for el in tree.getchildren()]

  def _parse_contents(self, element):
    if element.tag == 'word':
      return Word(element)
    elif element.tag == 'wordgroup':
      return WordGroup(element)
    # if it's not a word and word group, throw an exception rather than
    # try to continue quietly.
    else:
      raise ValueError('Element is not a word or wordgroup.') 

class WordGroup():
  def __init__(self, tree):
    self.min = int(tree.get('min'))
    self.max = int(tree.get('max'))
    self.label = tree.get('label')
    self.words = [Word(element) for element in tree.getchildren()]

class Word():
  def __init__(self, tree):
    self.min = int(tree.get('min'))
    self.max = int(tree.get('max'))
    self.is_contextual = bool(tree.get('contextual'))
    self.label = tree.get('label')
    # pos
    self.pos = tree.get('pos')
    self.excluded_pos = tree.get('expos')
    # dependencies
    self.dependencies = tree.get('deps')
    self.excluded_dependencies = tree.get('exdeps')
    self.num_dependencies_needed = tree.get('depnum')
    # types
    self.types = tree.get('type')
    self.excluded_types = tree.get('extype')
    self.num_types_needed = tree.get('typenum')
    # words and lemmas
    self.word = tree.get('word')
    self.lemma = tree.get('lemma')
