''' Tests for the match.py file. '''
import unittest

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
  <!ELEMENT pattern (word | wordgroup)+>
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
  <!ATTLIST word lemma CDATA "">
  <!ATTLIST word word CDATA "">
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

  <!ELEMENT wordgroup (word)+>
  <!ATTLIST wordgroup min CDATA "1">
  <!ATTLIST wordgroup max CDATA "1">
  <!ATTLIST wordgroup label CDATA "">
]>

<!-- SEE README FOR USAGE AND DOCS -->
<root version="1.0">
  <patterngroup label="basic">
    <pattern name="named-pattern" class="examples" description="for example purposes" priority="7"> 
      <!-- Find a word whose PoS begins with NN but isn't a plural, and is of type TXE or HGH -->
      <word pos="NN*" expos="*S" type="TXE,HGH"/>

      <!-- Optional preposition -->
      <word pos="IN" min="0" max="1" label="optional preposition" />

      <!-- Find a word that is either (but not both) of the following -->
      <wordgroup min="1" max="1">
        <!-- Verb or adverb, not TFL type and not an amod dependency -->
        <word pos="VB*,RB" extype="TFL" exdeps="amod"/>

        <!-- Any part of speech and either nsubj and/or dobj -->
        <word pos="*" deps="nsubj,dobj" depnum="1"/>
      </wordgroup>
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
</root>

'''

# STRING MATCHING
# write tests for the following
class TestParsing(unittest.TestCase):
  # 1. Match startswith PASS
  def test_parse_loads(self):
    self.fail()
    self.assertEqual(True, True)