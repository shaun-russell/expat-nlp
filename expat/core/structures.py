''' Common structures to pass data around. '''

from core.helpers import get_value

# Many of these class descriptions aren't very useful. At some point,
# write better definitions.

class ListAttributes():
  def __init__(self, to_find, to_exclude, required_num):

    # easy to understand bool value. This could be put in a function, but it
    # works just fine here for now
    self.has_match_requirements = to_find != '*' and to_find != ''
    self.to_find = to_find.split(',')

    self.required_num = required_num

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

  @staticmethod
  def get_correct_class(element):
    if element.tag == 'word':
      return PatternWord(element)
    elif element.tag == 'wordgroup':
      return WordGroup(element)
    # if it's not a word and word group, throw an exception rather than
    # try to continue quietly.
    else:
      raise ValueError('Element is not a word or wordgroup.') 

class WordGroup():
  ''' A group that contains multiple pattern words. This allows matching of words
      only if N of those words occur. Allows structures like ( word1 word2 ) | (word3). '''
  def __init__(self, tree):
    # min and max are the number of word matches needed for the whole
    # group to match. If only 1 word matches and 2 are required, the 
    # entire group fails to match.
    self.min = int(tree.get('min'))
    self.max = int(tree.get('max'))
    self.label = tree.get('label')
    self.words = [Pattern.get_correct_class(element) for element in tree.getchildren()]

class PatternWord():
  # this description is terrible, change this at some point
  ''' The attributes of a word that is part of a pattern definition. '''
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

