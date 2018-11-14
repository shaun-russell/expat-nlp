''' Tests for the match.py file. '''
import unittest
from core.match import StringMatching, ListMatching,PatternMatcher
from core.structures import AttributeSet,PatternWord,AnnotatedWord,Pattern
from core.annotators import BasicNltkAnnotator
from core.search import GraphSearch,BreadthFirstWithQueue,MatchBuilder
import xml.etree.cElementTree as etree
from collections import deque

pattern_pfx = '''
<!DOCTYPE root [
  <!-- Pattern Element -->
  <!ELEMENT pattern (word)+>
  <!ATTLIST pattern name ID #REQUIRED>
  <!ATTLIST pattern description CDATA "">
  <!ATTLIST pattern class CDATA #REQUIRED>
  <!ATTLIST pattern weight CDATA "1">
  <!ATTLIST pattern label CDATA "">

  <!-- Word element -->
  <!ELEMENT word EMPTY>
  <!ATTLIST word min CDATA "1">
  <!ATTLIST word max CDATA "1">
  <!ATTLIST word contextual CDATA "false">
  <!ATTLIST word label CDATA "">
  <!-- Specific Word Matching -->
  <!ATTLIST word lemma CDATA "*">
  <!ATTLIST word word CDATA "*">
  <!-- Parts of Speech -->
  <!ATTLIST word pos CDATA "*">
  <!ATTLIST word expos CDATA "">
  <!-- Dependencies -->
  <!ATTLIST word deps CDATA "*">
  <!ATTLIST word exdeps CDATA "">
  <!ATTLIST word depnum CDATA "1">
  <!-- Additional Type -->
  <!ATTLIST word type CDATA "*">
  <!ATTLIST word extype CDATA "">
  <!ATTLIST word typenum CDATA "1">
  <!ATTLIST word ner CDATA "O">
]>
'''



# STRING MATCHING
# write tests for the following
class TestMatching(unittest.TestCase):
  # 1. Match startswith PASS
  def test_match_starts_pass(self):
    word = 'Apples'
    strings = 'A*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 2. Match startswith FAIL
  def test_match_starts_fail(self):
    word = 'Apples'
    strings = 'Apl*,Apple'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 3. Match endswith PASS
  def test_match_ends_pass(self):
    word = 'Apples'
    strings = '*le,*les'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 4. Match endswith FAIL
  def test_match_ends_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Fruit*'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 5. Match exact PASS
  def test_match_exact_pass(self):
    word = 'Mangoes'
    strings = 'Mangoes'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 6. Match exact FAIL
  def test_match_exact_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Orange Fruit Lemons'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 7. Match contains PASS
  def test_match_contains_pass(self):
    word = 'Orange Fruit Mangoes'
    strings = '*Fruit*,*Mangoe*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 8. Match contains FAIL
  def test_match_contains_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = '*Paper*'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 9. Match surround PASS
  def test_match_surround_pass(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Orange*oes'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 10. Match surround FAIL
  def test_match_surround_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = 'A*Fruit Mangoes'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  def test_match_surround_pass_cased(self):
    word = 'Orange Fruit Mangoes'
    strings = '*FRUIT*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 11. Match mixed PASS 1
  def test_match_mixed_pass1(self):
    word = 'Oranges'
    strings = 'Fruit*,*papers,*ang*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 12. Match mixed PASS 2
  def test_match_mixed_pass2(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Or*eg,Orange Fruit Mango,*ruit*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 13. Match mixed FAIL 1
  def test_match_mixed_fail1(self):
    word = 'Potatoes'
    strings = 'Potatos*,*topato*,POTATO'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 14. Match mixed FAIL 2
  def test_match_mixed_fail2(self):
    word = 'ABCDEFg'
    strings = 'ABCDEF,*BCDEF'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 15. Match no-ignore-case PASS 1
  def test_match_case_pass1(self):
    word = 'ABCdefGEH'
    strings = 'ABCd*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 16. Match no-ignore-case PASS 2
  def test_match_case_pass2(self):
    word = 'AbCdE'
    strings = 'AbCdE'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings), False)

  # 16. Match ignore-case PASS 1
  def test_match_case_pass3(self):
    word = 'AbCdE'
    strings = 'AbCdE'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings), True)

  # 18. Match no-ignore-case FAIL 1
  def test_match_case_fail1(self):
    word = 'AbCdE'
    strings = 'aBcde'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings, False))

  # 19. Match no-ignore-case FAIL 2
  def test_match_case_fail2(self):
    word = 'Orange Fruit Mangoes'
    strings = '*fruit*'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings, False))


  # ATTRIBUTE LIST MATCHING
  def test_attr_list_pass1(self):
    value = 'DEF'
    attributes = AttributeSet('ABC,DEF', 'GHI', 1)
    self.assertEqual(True, ListMatching.is_match(value, attributes))

  def test_attr_list_pass2(self):
    value = 'FHI'
    attributes = AttributeSet('*', 'G*', 1)
    self.assertEqual(True, ListMatching.is_match(value, attributes))

  def test_attr_list_pass3(self):
    value = 'AVG'
    attributes = AttributeSet('A*,*G', 'GHI', 2)
    self.assertEqual(True, ListMatching.is_match(value, attributes))

  def test_attr_list_pass4(self):
    # matches the 2 required
    value = 'PNG,JPG,TIFF'
    attributes = AttributeSet('*G*', '', 1)
    self.assertEqual(True, ListMatching.is_match(value, attributes, required=2))

  def test_attr_list_pass5(self):
    # no restrictions on matching
    value = '123'
    attributes = AttributeSet('', '', 1)
    self.assertEqual(True, ListMatching.is_match(value, attributes))

  def test_attr_list_fail1(self):
    # exact match exclusion
    value = 'GHI'
    attributes = AttributeSet('ABC,DEF', 'GHI', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail2(self):
    # check an exclusion inside
    value = '1234 HI5'
    attributes = AttributeSet('ABC,DEF', '*HI*', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail3(self):
    # check that exclusions take precedence over matches
    value = 'AVG'
    attributes = AttributeSet('A*,*F', '*G', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail4(self):
    # check matching * but having a matching exclusion
    value = 'GBG'
    attributes = AttributeSet('*', 'G*', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail5(self):
    # check list of exclusions
    value = 'GBG'
    attributes = AttributeSet('*', 'A*,B*,G*', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail6(self):
    # doesn't match the 3 required
    value = 'PNG,JPG,TIFF'
    attributes = AttributeSet('*G*', '', 3)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail7(self):
    # match the 3 required
    value = 'PNG,JPG,TIFF'
    attributes = AttributeSet('*G*', '', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes, required=3))

  def test_dependency_matching1(self):
    # match anything starting with cc-conj
    deps = 'cc-conj-d'
    dep_pattern = 'cc-conj*'
    attributes = AttributeSet(dep_pattern, '', 1)
    self.assertEqual(True, ListMatching.is_match(deps, attributes, required=1))

  def test_dependency_matching2(self):
    # Pattern looks for dependent, not governor
    deps = 'cc-conj-g'
    dep_pattern = 'cc-conj-d'
    attributes = AttributeSet(dep_pattern, '', 1)
    self.assertEqual(False, ListMatching.is_match(deps, attributes, required=1))

  def test_dependency_matching3(self):
    # require 2 conj dependencies
    deps = 'cc-conj-d,cc-conj-g'
    dep_pattern = 'cc-conj*'
    attributes = AttributeSet(dep_pattern, '', 1)
    self.assertEqual(True, ListMatching.is_match(deps, attributes, required=2))

  def test_dependency_matching4(self):
    # match the conj, but exclude because it contains an excluded
    deps = 'cc-conj-d,cc-conj-g'
    dep_pattern = 'cc-conj*'
    attributes = AttributeSet(dep_pattern, 'cc-conj-g', 1)
    self.assertEqual(False, ListMatching.is_match(deps, attributes, required=1))




  def test_pattern_to_word_matching1(self):
    anword = AnnotatedWord(index=7,
                           word='bongoes',
                           lemma='bongo',
                           pos='IN',
                           ner='O',
                           dependencies='cc-conj-d')
    pattern = pattern_pfx+'<word pos="IN" lemma="bon*" max="1"/>'
    tree = etree.fromstring(pattern)
    pattern_word = PatternWord(tree)
    self.assertEqual(True,PatternMatcher.word_matches_pattern(anword, pattern_word))

  def test_pattern_to_word_matching2(self):
    anword = AnnotatedWord(index=5,
                           word='baboons',
                           lemma='bongo',
                           pos='NN',
                           ner='O',
                           dependencies='cc-conj-d')
    pattern = pattern_pfx+'<word word="*loon*"/>'
    tree = etree.fromstring(pattern)
    # print('\nPATTERN START\n')
    pattern_word = PatternWord(tree)
    self.assertEqual(False, PatternMatcher.word_matches_pattern(anword, pattern_word))

  def test_pattern_to_word_matching3(self):
    anword = AnnotatedWord(index=5,
                           word='baboons',
                           lemma='bongo',
                           pos='NNS',
                           ner='O',
                           dependencies='cc-conj-d')
    pattern = pattern_pfx+'<word pos="*" deps="cc*"/>'
    tree = etree.fromstring(pattern)
    pattern_word = PatternWord(tree)
    self.assertEqual(True,PatternMatcher.word_matches_pattern(anword, pattern_word, verbose=True))


  def test_pattern_to_word_matching4(self):
    anword = AnnotatedWord(index=5,
                           word='baboon',
                           lemma='bongo',
                           pos='NN',
                           ner='O',
                           dependencies='cc-conj-d')
    pattern = pattern_pfx+'<word expos="*N*" word="baboon"/>'
    tree = etree.fromstring(pattern)
    pattern_word = PatternWord(tree)
    self.assertEqual(False, PatternMatcher.word_matches_pattern(anword, pattern_word))


  def test_pattern_to_word_matching5(self):
    anword = AnnotatedWord(index=5,
                           word='baboons',
                           lemma='bongo',
                           pos='NN',
                           ner='O',
                           dependencies='cc-conj-d')
    pattern = pattern_pfx+'<word deps="cc-con*" exdeps="*-d"/>'
    tree = etree.fromstring(pattern)
    pattern_word = PatternWord(tree)
    self.assertEqual(False, PatternMatcher.word_matches_pattern(anword, pattern_word))

  def test_pattern_to_word_matching6(self):
    anword = AnnotatedWord(index=5,
                           word='baboons',
                           lemma='bongo',
                           pos='NN',
                           ner='O',
                           dependencies='cc-conj-d')
    pattern = pattern_pfx+'<word deps="cc-con*" exdeps="*-d"/>'
    tree = etree.fromstring(pattern)
    pattern_word = PatternWord(tree)
    self.assertEqual(False, PatternMatcher.word_matches_pattern(anword, pattern_word))



  def test_pattern_graph_entry_points1(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="JJ" min="1"/>
      <word pos="NN" min="1"/>
    </pattern>'''
    tree = etree.fromstring(pattern)
    pattern = Pattern(tree)
    is_correct_length = len(pattern.graph_entry_points) == 1
    contains_node = pattern.graph_entry_points[0]._pos == 'JJ'
    self.assertTrue(is_correct_length)
    self.assertTrue(contains_node)

  def test_pattern_graph_entry_points2(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="JJ" min="0"/>
      <word pos="NN" min="1"/>
    </pattern>'''
    tree = etree.fromstring(pattern)
    pattern = Pattern(tree)
    is_correct_length = len(pattern.graph_entry_points) == 2
    contains_node1 = pattern.graph_entry_points[0]._pos == 'JJ'
    contains_node2 = pattern.graph_entry_points[1]._pos == 'NN'
    self.assertTrue(is_correct_length)
    self.assertTrue(contains_node1)
    self.assertTrue(contains_node2)

  def test_pattern_graph_exit_points1(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="JJ" min="1"/>
      <word pos="NN" min="1"/>
    </pattern>'''
    tree = etree.fromstring(pattern)
    pattern = Pattern(tree)
    is_correct_length = len(pattern.graph_exit_points) == 1
    contains_node = pattern.graph_exit_points[0]._pos == 'NN'
    self.assertTrue(is_correct_length)
    self.assertTrue(contains_node)

  def test_pattern_graph_exit_points2(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="JJ" min="1"/>
      <word pos="NN" min="1" max="2"/>
    </pattern>'''
    tree = etree.fromstring(pattern)
    pattern = Pattern(tree)
    is_correct_length = len(pattern.graph_exit_points) == 1
    contains_node1 = pattern.graph_exit_points[0]._pos == 'NN'
    self.assertTrue(is_correct_length)
    self.assertTrue(contains_node1)


  def test_pattern_graph_successors1(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="JJ" min="1"/>
      <word pos="IN" min="0"/>
      <word pos="NN" min="1" max="2"/>
    </pattern>'''
    tree = etree.fromstring(pattern)
    pattern = Pattern(tree)
    self.assertTrue(pattern.graph.is_directed())

    # starting_node = pattern.graph.nodes(data=pattern.graph_entry_points[0])
    starting = pattern.graph_entry_points[0]
    successors = []
    for succ in pattern.graph.successors(starting):
      successors.append(succ._pos)

    self.assertTrue(starting._pos == 'JJ')
    self.assertTrue(successors[0] == 'IN')
    self.assertTrue(successors[1] == 'NN')


  def test_pattern_graph_structure1(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="JJ" min="1"/>
      <word pos="IN" min="0"/>
      <word pos="NN" min="1" max="2"/>
    </pattern>'''
    tree = etree.fromstring(pattern)
    # print('\n') # print debug information
    # pattern = Pattern(tree, True)
    pattern = Pattern(tree)
    self.assertTrue(pattern.graph.is_directed())

    starting = pattern.graph_entry_points[0]
    successor = None
    for x in pattern.graph.successors(starting):
      successor = x
      break
    
    successors2 = []
    for node in pattern.graph.successors(successor):
      successors2.append(node._pos)

    self.assertTrue(successors2[0] == 'NN')
    self.assertTrue(successors2[1] == 'NN')


  def test_pattern_graph_matches1(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="VB*" />
      <word pos="DT" min="0"/>
      <word pos="NN*" />
    </pattern>'''
    tree = etree.fromstring(pattern)
    pattern = Pattern(tree)

    sentence = "He is running the race."
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    bfs_search = BreadthFirstWithQueue()

    matches = MatchBuilder.find_all_matches(annotated_sentence, pattern, bfs_search)
    actual = ' '.join([x.word for x in matches[0]])
    expected = 'running the race'
    self.assertEqual(actual, expected)

  def test_pattern_graph_matches2(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="JJ*" />
      <word pos="NN*" />
    </pattern>'''
    tree = etree.fromstring(pattern)
    pattern = Pattern(tree)

    sentence = "He has a big dog that lives in the green house."
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    bfs_search = BreadthFirstWithQueue()

    matches = MatchBuilder.find_all_matches(annotated_sentence, pattern, bfs_search)
    actual1 = ' '.join([x.word for x in matches[0]])
    expected1 = 'big dog'
    actual2 = ' '.join([x.word for x in matches[1]])
    expected2 = 'green house'
    self.assertEqual(actual1, expected1)
    self.assertEqual(actual2, expected2)

  def test_pattern_graph_matches3(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="DT" min="0"/>
      <word pos="NN*" />
    </pattern>'''
    tree = etree.fromstring(pattern)
    pattern = Pattern(tree)

    sentence = "This is the dog who barks at moons."
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    bfs_search = BreadthFirstWithQueue()

    matches = MatchBuilder.find_all_matches(annotated_sentence, pattern, bfs_search)
    actual1 = ' '.join([x.word for x in matches[0]])
    self.assertEqual(actual1, 'the dog')
    actual2 = ' '.join([x.word for x in matches[1]])
    self.assertEqual(actual2, 'dog')
    actual3 = ' '.join([x.word for x in matches[2]])
    self.assertEqual(actual3, 'moons')


  def test_pattern_graph_matches4(self):
    pattern = pattern_pfx+'''
    <pattern name="ex" class="ex-patterns">
      <word pos="VB*" />
      <word pos="DT" min="2"/>
    </pattern>'''
    tree = etree.fromstring(pattern)
    pattern = Pattern(tree)

    sentence = "He is running the race by eating the the mungo."
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    bfs_search = BreadthFirstWithQueue()

    matches = MatchBuilder.find_all_matches(annotated_sentence, pattern, bfs_search)
    actual = ' '.join([x.word for x in matches[0]])
    expected = 'eating the the'
    self.assertEqual(actual, expected)




