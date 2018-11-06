''' Annotator objects. '''
from nltk.tokenize import word_tokenize
from core.structures import AnnotatedSentence,AnnotatedWord
from nltk import pos_tag
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
    


