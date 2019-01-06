''' Common structures to pass data around. '''

import networkx as nx
import click
from copy import deepcopy,copy
from collections import deque 

# FUNCTIONS
# Having some problems with circular imports, which is a problem I tend
# to have with Python. Just logically arranging functions into files doesn't
# work, they have to be hierarchically grouped (usage grouping rather than
# category grouping). This function therefore goes here.
def get_value(label, source, default):
  ''' Quick function to get values with provided defaults) '''
  if label in source:
    return source[label]
  else:
    return default


class AttributeSet():
  ''' Common class to store Required,Excluded,NumRequired sets: i.e. types, dependencies '''
  def __init__(self, to_find, to_exclude, required_num):

    # easy to understand bool value. This could be put in a function, but it
    # works just fine here for now
    self.has_match_requirements = to_find != '*' and to_find != ''
    self.to_find = to_find.split(',')

    self.required_num = int(required_num)

    # if nothing specified, nothing to exclude
    self.to_exclude = to_exclude.split(',')
    self.has_exclusions = to_exclude != ''


class PatternGroup():
  ''' A collection of patterns. Parsed from XML.'''
  def __init__(self, tree):
    self.label = tree.find('label')
    self.version = tree.find('version')
    # pattern object for every child element
    self.patterns = [Pattern(child) for child in tree.getchildren()]

class Pattern():
  ''' Represents a sequence of words that represent a certain pattern. Parsed from XML. '''
  def __init__(self, tree, debug=False):
    # parse the attributes from an XML pattern definitions.
    self.name = tree.get('name')
    self.description = tree.get('description')
    # 'class' is a protected word in python, so the field is 'classname'
    self.classname = tree.get('class')
    self.weight = int(tree.get('weight'))
    self.label = tree.get('label')
    self.preprocess = tree.get('preprocess').lower() == 'true'
    # create the correct object for the child elements of the pattern
    self.children = [PatternWord(pword,i) for i,pword in enumerate(tree.getchildren())]

    # create graph for pattern traversal and matching
    decomposed_pattern = self._decompose_pattern(self.children)
    self.graph_entry_points = GraphBuilder.get_entry_points(decomposed_pattern)
    # I think the 'graph_exit_points' variable is no longer used outside of tests.
    self.graph_exit_points = GraphBuilder.get_exit_points(decomposed_pattern)
    self.graph = self._create_graph(decomposed_pattern, debug)


  def _create_graph(self, pattern_items, debug=False):
    ''' Constructs a graph of all possible path combinations. '''
    # instantiate an empty directed graph
    dgraph = nx.DiGraph()

    # For the graph, the entry and exit points need to be saved and marked
    # Optional nodes branch from the previous node and join to the required node
    # that is next in the sequence.

    # this adds all the nodes.
    for (_,item) in pattern_items:
      if debug: click.echo('Add node: {}:{}'.format(item._pos, item.index))
      dgraph.add_node(item)

    # create all the edges of the graph
    # The following method is like a breadth-first edge linking method,
    # but because it is a graph, not a tree (must join up to one node in the end)
    # when a required node is reached, all open nodes are joined up to it
    # Required nodes branch to the first optional, then further optionals form a chain.
    # REQ_1 -> REQ_2 : CLOSE EDGE
    # REQ_1 -> OPT_1 : OPEN CHAIN
    # OPT_1 -> REQ_2 : CLOSE CHAIN
    # OPT_1 -> OPT_2 : OPEN CHAIN
    # OPT_2 -> REQ_2 : CLOSE CHAIN
    if debug: click.echo('Start adding edges.')
    open_nodes = []
    for i,(is_required, item) in enumerate(pattern_items):
      # exception case for the first node
      if i == 0:
        open_nodes.append(item)
        if debug: click.echo('add first node: {}'.format(item.index))
        continue

      # for all new nodes, make connections between the open nodes and the new node
      for node in open_nodes:
        if debug: click.echo('add edge: {} -> {}'.format(node.index, item.index))
        dgraph.add_weighted_edges_from([(node,item,1)])

      # add item 
      open_nodes.append(item)

      # when it gets to a required node
      if is_required:
        # closing point for any open nodes
        # remove all nodes
        open_nodes = []
        if debug: click.echo('reset nodes')
        # add the current required node to the open
        if debug: click.echo('req, adding: {}'.format(item.index))
        open_nodes.append(item)
      if debug: click.echo('loop')
    return dgraph
  
  def _decompose_pattern(self, pattern_items):
    ''' Separate pattern words into optional and required nodes. '''
    decomposed_list = []
    # because words are repeated for the optionals (if max > 1)
    # the items need to be copied and given a unique index which
    # represents the word's position in the pattern
    index = 0
    for item in pattern_items:
      if item.max > item.min:
        for _ in range(0, item.max-item.min):
          copied_item = deepcopy(item)
          copied_item.set_index(index)
          decomposed_list.append((False, copied_item))
          index += 1
      for _ in range(0, item.min):
        copied_item = deepcopy(item)
        copied_item.set_index(index)
        decomposed_list.append((True, copied_item))
        index += 1
    return decomposed_list

  @staticmethod
  def get_correct_class(element):
    if element.tag == 'word':
      return PatternWord(element)
    else:
      raise ValueError('Element is not a word.') 


class PatternWord():
  ''' A structure that represents a single word in a pattern with its match criteria. '''
  def __init__(self, tree, index = -1):
    self.min = int(tree.get('min'))
    self.max = int(tree.get('max'))
    self.is_contextual = bool(tree.get('contextual'))
    self.label = tree.get('label')
    # parts of speech
    self._pos = tree.get('pos')
    self._excluded_pos = tree.get('expos')
    self._num_pos_needed = 1
    self.pos_attributes = AttributeSet(self._pos,
                                       self._excluded_pos,
                                       self._num_pos_needed)
    # dependencies
    self._dependencies = tree.get('deps')
    self._excluded_dependencies = tree.get('exdeps')
    self._num_dependencies_needed = tree.get('depnum')
    self.dep_attributes = AttributeSet(self._dependencies,
                                       self._excluded_dependencies,
                                       self._num_dependencies_needed)
    # types
    self._types = tree.get('type')
    self._excluded_types = tree.get('extype')
    self._num_types_needed = tree.get('typenum')
    self.type_attributes = AttributeSet(self._types,
                                        self._excluded_types,
                                        self._num_types_needed)
    # words and lemmas
    self.word = tree.get('word')
    self.lemma = tree.get('lemma')
    self.ner = tree.get('ner')

    self.index = index

  def set_index(self, id):
    ''' Override the index. '''
    self.index = id
    


class AnnotatedSentence():
  # At this stage, this is just a list. However if if needs to be extended,
  # it's easier to add to an existing class than switch from data structures.
  ''' Container for annotated words. '''
  def __init__(self, annotated_words):
    self.words = annotated_words

  def at(self, index):
    ''' Safe way of getting a word at a specified index.
        Returns None if word doesn't exist.'''
    if index >= len(self.words) or index < 0:
      return None
    return self.words[index]

  def repair_indices(self):
    ''' Re-indexes all words in the sentence from 0 to sentence length. '''
    for i,_ in enumerate(self.words):
      # using words[i] because sometimes the copy is changed, rather than ref
      self.words[i].index = i
  
  def get_queue(self):
    ''' Return the sentence as a queue of words. '''
    q = deque()
    for word in self.words:
      q.append(word)
    # need to reverse because otherwise the sentence is backwards (no matches)
    q.reverse()
    return q

class AnnotatedWord():
  ''' A word that has been given attributes by an annotator. '''
  def __init__(self, **kwargs):
    self.index = get_value('index', kwargs, -1)
    self.word = get_value('word', kwargs, None)
    self.lemma = get_value('lemma', kwargs, None)
    self.pos = get_value('pos', kwargs, None)
    self.dependencies = get_value('dependencies', kwargs, '')
    self.types = get_value('type', kwargs, '')
    self.ner = get_value('ner', kwargs, 'O') # O is none

class GraphBuilder():
  ''' Contains functions to help build graph structures. '''
  @staticmethod
  def get_entry_points(decomposed_pattern):
    ''' Finds all the entry nodes of a pattern.
        If a pattern starts with 1 optional, there are at least 2 entry points
        for a word sequence. '''
    # establish the entry nodes for the pattern
    # until a node is required, every optional node is an entry point
    entry_nodes = []
    for is_required,item in decomposed_pattern:
      # the last entry point is the first required node
      # because patterns fail if they don't have the required nodes, therefore
      # it must enter before or on the first required node
      if is_required:
        entry_nodes.append(item)
        # add the required entry point
        break
      else:
        entry_nodes.append(item)
    return entry_nodes

  @staticmethod
  def get_exit_points(decomposed_pattern):
    ''' Obsolete? '''
    # establish the exit nodes for the pattern
    # same as entry, but with a reversed list
    # could actually refactor this
    exit_nodes = []
    # [::-1] reverses a list
    for is_required,item in decomposed_pattern[::-1]:
      if is_required:
        exit_nodes.append(item)
        # add the required entry point
        break
      else:
        exit_nodes.append(item)
    return exit_nodes


class Selector():
  ''' Selector object base class '''
  def merge_patterns(self, pattern_list):
    return pattern_list

  def apply_patterns_to_sentence(self, pattern_list, sentences):
    return None


# class LengthSelector():
#   ''' A selector that chooses the longest patterns first
#       and ignores subsequent overlapping patterns. '''
#   def __init__(self, longest=True):
#     self.longest_first = longest

#   def merge_patterns(self, pattern_list):
#     # do stuff to patterns
#     merged_patterns = []
#     # for every class name
#     for pattern_class in set([w.classname for w in pattern_list]):
#       # find all patterns of that class
#       patterns_of_class = [w for w in pattern_list if w.classname == pattern_class]
#       # if patterns overlap, select the pattern with the longest length.
#       # if equal length, use priority. If equal priority, let python's sort() choose
#       non_overlapping_patterns = []

#     return merged_patterns

#   def apply_patterns_to_sentence(self, pattern_list, sentences):
#     ''' Incomplete function at this stage. '''
#     patterns = self.merge_patterns
#     # apply patterns to sentence
#     pass
