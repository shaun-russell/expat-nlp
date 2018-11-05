''' Tests for the annotators.py file. '''
import unittest
from core.match import StringMatching, ListMatching
from core.structures import ListAttributes
from core.annotators import BasicNltkAnnotator

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

