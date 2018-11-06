''' Tests for the annotators.py file. '''
import unittest
from core.match import StringMatching, ListMatching
from core.structures import ListAttributes
from core.annotators import BasicNltkAnnotator,StanfordCoreNLPAnnotator

corenlp_url = 'http://localhost:9000'

# STRING MATCHING
# write tests for the following
class TestMatching(unittest.TestCase):
  def test_annotate_basicnltk(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    item_at_2 = annotated_sentence.at(2)
    self.assertEqual(item_at_2.pos, 'NNS')
    self.assertEqual(item_at_2.word, 'pears')
    self.assertEqual(item_at_2.lemma, None)

  def test_annotate_outside_range_high(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    self.assertEqual(None, annotated_sentence.at(15))

  def test_annotate_outside_range_low(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    self.assertEqual(None, annotated_sentence.at(-2))

  def test_annotate_stanford1(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = StanfordCoreNLPAnnotator(corenlp_url)
    annotated_sentence = annotator.annotate(sentence)
    item_at_2 = annotated_sentence.at(2)
    self.assertEqual(item_at_2.pos, 'NNS')
    self.assertEqual(item_at_2.word, 'pears')
    self.assertEqual(item_at_2.lemma, 'pear')

  def test_annotate_stanford2(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = StanfordCoreNLPAnnotator(corenlp_url)
    annotated_sentence = annotator.annotate(sentence)
    self.assertEqual(True, 'cc-d' in annotated_sentence.at(1).dependencies)

  def test_annotate_stanford3(self):
    sentence = "Apples and pears are like Barry's bears."
    annotator = StanfordCoreNLPAnnotator(corenlp_url)
    annotated_sentence = annotator.annotate(sentence)
    item_at_5 = annotated_sentence.at(2)
    self.assertEqual(item_at_5.ner, 'O')

  def test_annotate_stanford_lemma(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = StanfordCoreNLPAnnotator(corenlp_url)
    annotated_sentence = annotator.annotate(sentence)
    item = annotated_sentence.at(5)
    self.assertEqual(item.lemma, 'badger')

  def test_annotate_stanford_index(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = StanfordCoreNLPAnnotator(corenlp_url)
    annotated_sentence = annotator.annotate(sentence)
    item = annotated_sentence.at(4)
    self.assertEqual(item.index, 4)

  def test_annotate_stanford_deps3(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = StanfordCoreNLPAnnotator(corenlp_url)
    annotated_sentence = annotator.annotate(sentence)
    item_at_2 = annotated_sentence.at(2)
    self.assertEqual(True, 'cc-d' not in annotated_sentence.at(2).dependencies)

  def test_annotate_outside_range_high_corenlp(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = StanfordCoreNLPAnnotator(corenlp_url)
    annotated_sentence = annotator.annotate(sentence)
    self.assertEqual(None, annotated_sentence.at(15))

  def test_annotate_outside_range_low_corenlp(self):
    sentence = 'Apples and pears are like badgers and bears.'
    annotator = StanfordCoreNLPAnnotator(corenlp_url)
    annotated_sentence = annotator.annotate(sentence)
    self.assertEqual(None, annotated_sentence.at(-2))
