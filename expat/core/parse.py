# todo
# read xml file
# create pattern, group, and word classes
# populate defaults

import xml.etree.cElementTree as etree
import lxml

# use this as a placeholder for properties
NULL = None

class RootElement():
  def __init__(self):
    self.version = NULL
    self.patterngroups = []

class PatternGroup():
  def __init__(self):
    self.label = NULL
    self.patterns = []

class Pattern():
  def __init__(self):
    self.name = NULL
    self.description = NULL
    self.classname = NULL
    self.priority = NULL
    self.label = NULL
    # the child elements of the pattern
    self.children = []

class WordGroup():
  def __init__(self):
    self.min = NULL
    self.max = NULL
    self.label = NULL
    self.words = []

class Word():
  def __init__(self):
    self.min = NULL
    self.max = NULL
    self.is_contextual = NULL
    self.label = NULL
    # pos
    self.pos = NULL
    self.excluded_pos = NULL
    # dependencies
    self.dependencies = NULL
    self.excluded_dependencies = NULL
    self.num_dependencies_needed = NULL
    # types
    self.types = NULL
    self.excluded_types = NULL
    self.num_types_needed = NULL
