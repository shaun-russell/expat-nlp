''' Annotator objects. '''
from nltk.tokenize import word_tokenize
from core.structures import AnnotatedSentence,AnnotatedWord
from nltk import pos_tag

# core nlp annotator
from pycorenlp import StanfordCoreNLP


class BaseAnnotator():
  def annotate(self, sentence):
    return None


class StanfordCoreNlpAnnotator(BaseAnnotator):
  def __init__(self, server_url, props=None):
    self.url = server_url
    self.nlp = StanfordCoreNLP(server_url)
    if props == None:
      active_annos = "tokenize,ssplit,pos,lemma,ner,truecase,parse,depparse,relation"
      properties = {'annotators':active_annos, 'pipelineLanguage': 'en', 'outputFormat': 'json'}
      self.props = properties
    else:
      self.props = props

  def annotate(self, sentence):
    annotated_data = self.nlp.annotate(sentence)
    return None


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
    


