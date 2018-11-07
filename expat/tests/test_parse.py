''' Tests for the parse.py file. '''
import unittest
import core.parse as parse
import xml.etree.cElementTree as etree

# the file path to a copy of the xml string below
XML_FILEPATH = 'tests/test-files/test-patterns.xml'
# Rather than reading a file, just use the string for most tests.
XML_SAMPLE = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
  <!-- Root Element -->
  <!ELEMENT root (patterngroup)+>
  <!ATTLIST root version CDATA #REQUIRED>

  <!-- Pattern Group Element -->
  <!ELEMENT patterngroup (pattern)+>
  <!ATTLIST patterngroup label CDATA "">

  <!-- Pattern Element -->
  <!ELEMENT pattern (word)+>
  <!ATTLIST pattern name ID #REQUIRED>
  <!ATTLIST pattern description CDATA "">
  <!ATTLIST pattern class CDATA #REQUIRED>
  <!ATTLIST pattern priority CDATA "1">
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
  <!ATTLIST word ner CDATA "O">
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
]>

<!-- SEE README FOR USAGE AND DOCS -->
<patterngroup label="basic" version="1.0">
  <pattern name="named-pattern" class="examples" description="for example purposes" priority="7"> 
    <!-- Find a word whose PoS begins with NN but isn't a plural, and is of type TXE or HGH -->
    <word pos="NN*" expos="*S" type="TXE,HGH"/>

    <!-- Optional preposition -->
    <word pos="IN" min="0" max="1" label="optional preposition" />
  </pattern>

  <!-- Find up to 3 adjectives that are preceded by a noun, but the noun
        is only for contextual purposes. -->
  <pattern name="JJ3-NN" class="examples">
    <word pos='JJ*' max="3"/>
    <word pos='NN*' contextual='True'/>
  </pattern>

  <!-- Match 'gone' preceded by lemmas of anything starting with 'toast', and 'be' -->
  <pattern name="be-gone" class="word examples">
    <word lemma="toast*" />
    <word lemma="be" />
    <word word="gone" />
  </pattern>
</patterngroup>

'''

# STRING MATCHING
# write tests for the following
class TestParsing(unittest.TestCase):
  def test_parse_loads(self):
    tree = etree.fromstring(XML_SAMPLE.strip())
    for child in tree.getchildren():
      for gchild in child.getchildren():
        for ggchild in gchild.getchildren():
          pass
    # if it passes those loops, then no problems reading tree
    self.assertEqual(True, True)

  def test_parse_tree_parse1(self):
    xmltree = parse.Parser.parse_patterns(XML_SAMPLE)
    expected_tag = xmltree.patterns[0].children[1].pos_attributes.to_find[0]
    self.assertEqual(expected_tag, 'IN')

  def test_parse_tree_parse2(self):
    xmltree = parse.Parser.parse_patterns(XML_SAMPLE)
    expected_tag = xmltree.patterns[1].name
    self.assertEqual(expected_tag, 'JJ3-NN')

  def test_parse_tree_parse3(self):
    xmltree = parse.Parser.parse_patterns(XML_SAMPLE)
    is_contextual = xmltree.patterns[1].children[1].is_contextual
    self.assertEqual(is_contextual, True)

  def test_parse_tree_parse4(self):
    xmltree = parse.Parser.parse_patterns(XML_SAMPLE)
    expected_tag = xmltree.patterns[2].children[2].word
    self.assertEqual(expected_tag, 'gone')

  def test_parse_tree_parse5(self):
    xmltree = parse.Parser.parse_patterns(XML_SAMPLE)
    expected_value = xmltree.patterns[0].children[1].min
    self.assertEqual(expected_value, 0)

  def test_parse_tree_parse6(self):
    xmltree = parse.Parser.parse_patterns(XML_SAMPLE)
    expected_tag = xmltree.patterns[0].children[0]._dependencies
    self.assertEqual(expected_tag, '*')

  def test_parse_tree_filetest1(self):
    xmltree = parse.Parser.parse_patterns(XML_FILEPATH, True)
    expected_tag = xmltree.patterns[0].children[0]._dependencies
    self.assertEqual(expected_tag, '*')