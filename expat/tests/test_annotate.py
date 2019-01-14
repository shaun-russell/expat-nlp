''' Tests for the annotators.py file. '''
import unittest
import core.parse as parse
from core.match import StringMatching, ListMatching
from core.structures import AttributeSet
from core.annotators import BasicNltkAnnotator,StanfordCoreNLPAnnotator, TypeExtensionAnnotator

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
    self.assertEqual(item_at_2.lemma, 'pear')

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

  def test_annotate_nltk_geoextension1(self):
    sentence = 'Houses and rabbits look like badgers, oil rigs, and gas stations.'
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    geo_categories = {
      'GNN' : ('NN*', 'tests/test-files/gnns.txt', 'n'),
      'ANIMAL' : ('NN*', 'tests/test-files/animals.txt', 'n'),
    }
    geo_annotator = TypeExtensionAnnotator(geo_categories, stem=True)
    geo_sentence = geo_annotator.extend(annotated_sentence)

    animal_count = len([w for w in geo_sentence.words if 'ANIMAL' in w.types])
    gnn_count = len([w for w in geo_sentence.words if 'GNN' in w.types])
    self.assertEqual(animal_count, 2)
    self.assertEqual(gnn_count, 5)

  def test_annotate_nltk_geoextension2(self):
    sentence = "Musical instruments don't sound like badgers."
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    geo_categories = {
      'GNN' : ('NN*', 'tests/test-files/gnns.txt', 'n'),
      'ANIMAL' : ('NN*', 'tests/test-files/animals.txt', 'n'),
    }
    geo_annotator = TypeExtensionAnnotator(geo_categories, stem=True)
    geo_sentence = geo_annotator.extend(annotated_sentence)

    animal_count = len([w for w in geo_sentence.words if 'ANIMAL' in w.types])
    gnn_count = len([w for w in geo_sentence.words if 'GNN' in w.types])
    self.assertEqual(animal_count, 1)
    self.assertEqual(gnn_count, 0)

  def test_annotate_nltk_geoextension3(self):
    sentence = 'Houses and rabbits look like badgers, oil rigs, and gas stations.'
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)
    geo_categories = {
      'GNN' : ('NN*', 'tests/test-files/gnns.txt', 'n'),
      'ANIMAL' : ('NN*', 'tests/test-files/animals.txt', 'n'),
    }
    geo_annotator = TypeExtensionAnnotator(geo_categories)
    geo_sentence = geo_annotator.extend(annotated_sentence)

    animal_count = len([w for w in geo_sentence.words if 'ANIMAL' in w.types])
    gnn_count = len([w for w in geo_sentence.words if 'GNN' in w.types])
    self.assertEqual(animal_count, 2)
    self.assertEqual(gnn_count, 5)

  def test_annotate_nltk_geoextension_fileload(self):
    sentence = 'Houses and rabbits look like badgers, oil rigs, and gas stations.'
    annotator = BasicNltkAnnotator()
    annotated_sentence = annotator.annotate(sentence)

    exfile = open('tests/test-files/test-extensions.txt', 'r')
    geo_categories = parse.ExtensionParser.parse(exfile)
    exfile.close()

    geo_annotator = TypeExtensionAnnotator(geo_categories)
    geo_sentence = geo_annotator.extend(annotated_sentence)

    animal_count = len([w for w in geo_sentence.words if 'ANIMAL' in w.types])
    gnn_count = len([w for w in geo_sentence.words if 'GNN' in w.types])
    self.assertEqual(animal_count, 2)
    self.assertEqual(gnn_count, 5)





