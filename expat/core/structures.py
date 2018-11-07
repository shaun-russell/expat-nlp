''' Common structures to pass data around. '''

from core.helpers import get_value
import networkx as nx

# Many of these class descriptions aren't very useful. At some point,
# write better definitions.

class AttributeSet():
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
  ''' A collection of patterns. '''
  def __init__(self, tree):
    self.label = tree.find('label')
    self.version = tree.find('version')
    # pattern object for every child element
    self.patterns = [Pattern(child) for child in tree.getchildren()]

class Pattern():
  ''' Represents a sequence of words that represent a certain pattern. '''
  def __init__(self, tree):
    self.name = tree.get('name')
    self.description = tree.get('description')
    # 'class' is a protected word in python, so the field is 'classname'
    self.classname = tree.get('class')
    self.priority = int(tree.get('priority'))
    self.label = tree.get('label')
    # create the correct object for the child elements of the pattern
    self.children = [Pattern.get_correct_class(el) for el in tree.getchildren()]

    # graph for pattern traversal and matching
    # self.graph = self._create_graph(self.children)
    # self.graph_entry_nodes = []

  def _create_graph(self, pattern_items):
    dgraph = nx.DiGraph()

    decomposed_pattern = self._decompose_pattern(pattern_items)

    # establish the entry nodes for the pattern
    entry_nodes = []
    for (status,item) in decomposed_pattern:
      pass

    print(decomposed_pattern)
    for item in decomposed_pattern:
      # add a single edge
      if item.min > 0:
        # at least 1 required node
        pass
      else:
        # all nodes are optional
        pass
      pass
    return None
  
  def _decompose_pattern(self, pattern_items):
    ''' Separate pattern words into optional and required nodes. '''
    decomposed_list = []
    for item in pattern_items:
      for i in range(0, item.min):
        decomposed_list.append(('required', item))
      for i in range(item.max-item.min, item.max):
        decomposed_list.append(('optional', item))
    return decomposed_list

  @staticmethod
  def get_correct_class(element):
    if element.tag == 'word':
      return PatternWord(element)
    else:
      raise ValueError('Element is not a word.') 


class PatternWord():
  # this description is terrible, change this at some point
  ''' The attributes of a word that is part of a pattern definition. '''
  def __init__(self, tree):
    self.min = int(tree.get('min'))
    self.max = int(tree.get('max'))
    self.is_contextual = bool(tree.get('contextual'))
    self.label = tree.get('label')
    # pos
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



class AnnotatedSentence():
  # At this stage, this is just a list. However if if needs to be extended,
  # it's easier to add to an existing class than switch from data structures.
  ''' Container for annotated words. '''
  def __init__(self, annotated_words):
    self.words = annotated_words

  def at(self, index):
    if index >= len(self.words) or index < 0:
      return None
    return self.words[index]

  def repair_indices(self):
    for i,_ in enumerate(self.words):
      # using words[i] because sometimes the copy is changed, rather than ref
      words[i].index = i

class AnnotatedWord():
  def __init__(self, **kwargs):
    self.index = get_value('index', kwargs, -1)
    self.word = get_value('word', kwargs, None)
    self.lemma = get_value('lemma', kwargs, None)
    self.pos = get_value('pos', kwargs, None)
    self.dependencies = get_value('dependencies', kwargs, '')
    self.types = get_value('type', kwargs, '')
    self.ner = get_value('ner', kwargs, 'O') # O is none

