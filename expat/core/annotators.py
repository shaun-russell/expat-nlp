''' Annotator objects. '''
from nltk.tokenize import word_tokenize
from core.match import StringMatching
from core.structures import AnnotatedSentence,AnnotatedWord
from nltk import pos_tag
from nltk.stem.porter import PorterStemmer
import json

# core nlp annotator
from pycorenlp import StanfordCoreNLP


class BaseAnnotator():
  def annotate(self, sentence):
    return None


class StanfordCoreNLPAnnotator(BaseAnnotator):
  def __init__(self, server_url, props=None):
    self.url = server_url
    self.nlp = StanfordCoreNLP(server_url)
    if props == None:
      active_annos = "tokenize,ssplit,pos,lemma,ner,truecase,parse,depparse"
      properties = {'annotators':active_annos, 'pipelineLanguage': 'en', 'outputFormat': 'json'}
      self.props = properties
    else:
      self.props = props

  def annotate(self, sentence):
    annotated_data = json.loads(self.nlp.annotate(sentence))
    annotated_sentence = annotated_data['sentences'][0]
    anno_words = []
    for token in annotated_sentence['tokens']:
      dependencies = self._get_dependency_string(token['index'], annotated_sentence['basicDependencies'])
      # print(dependencies)
      # -1 the index because CoreNLP makes them 1-based rather than 0-based, so fix.
      anword = AnnotatedWord(index=token['index']-1,
                             word=token['word'],
                             lemma=token['lemma'],
                             pos=token['pos'],
                             ner=token['ner'],
                             dependencies=dependencies)
      anno_words.append(anword)

    return AnnotatedSentence(anno_words)

  def _has_dependency(self, dependency, idx):
    return dependency['governor'] == idx or dependency['dependent'] == idx

  def _get_dependency_string(self, idx, dependencies):
    corresponding = [dep for dep in dependencies if self._has_dependency(dep, idx)]
    dependency_strings = []
    # join the dependencies with the suffixes
    for dep in corresponding:
      if dep['governor'] == idx:
        dependency_strings.append(dep['dep']+'-g')
      elif dep['dependent'] == idx:
        dependency_strings.append(dep['dep']+'-d')
    return ','.join(dependency_strings)


class BasicNltkAnnotator(BaseAnnotator):
  def __init__(self):
    pass

  def annotate(self, sentence):
    ''' Use the NLTK library to add basic NLP info to sentence.
        Return an AnnotatedSentence. '''
    tokens = word_tokenize(sentence)
    pos_tagged_tokens = pos_tag(tokens)
    anno_words = []
    for i,(token,pos) in enumerate(pos_tagged_tokens):
      anno_words.append(AnnotatedWord(index=i,word=token,pos=pos))

    return AnnotatedSentence(anno_words)
    
class ExtensionWordSet():
  def __init__(self, label, pos, filepath, stem=False):
    self.label = label
    self.pos = pos
    with open(filepath, 'r', encoding='utf8') as wordfile:
      lines = wordfile.readlines()
      if stem:
        stemmer = PorterStemmer()
        self.words = [stemmer.stem(w.strip()) for w in lines]
      else:
        self.words = [w.strip() for w in lines]

class ExtensionAnnotatorBase():
  def extend(self, annotated_sentence):
    return annotated_sentence

class TypeExtensionAnnotator(ExtensionAnnotatorBase):
  def __init__(self, categories, stem=False):
    self.wordsets = []
    self.stemming = stem
    for label,(pos,fpath) in categories.items():
     self.wordsets.append(ExtensionWordSet(label, pos, fpath, self.stemming))

  def extend(self, annotated_sentence):
    stemmer = PorterStemmer()
    extended_sentence = []
    for word in annotated_sentence.words:
      stemmed_word = stemmer.stem(word.word) if self.stemming else word.word
      # convert the current word types to a list
      word_types = word.types.split(',') if word.types != '' else []
      # for all the wordsets whose part of speech tags match the current word
      for wordset in [s for s in self.wordsets if StringMatching.is_match(word.pos, s.pos)]:
        if stemmed_word in wordset.words:
          word_types.append(wordset.label)

      word.types = ','.join(word_types)
      extended_sentence.append(word)
    return AnnotatedSentence(extended_sentence)
