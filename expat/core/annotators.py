''' Annotator objects. '''
from nltk.tokenize import word_tokenize
from core.structures import AnnotatedSentence,AnnotatedWord
from nltk import pos_tag

class BaseAnnotator():
  def annotate(self, sentence):
    return None


class StanfordCoreNlpAnnotator(BaseAnnotator):
  def __init__(self, server_url):
    self.url = server_url

  def annotate(self, sentence):
    return None


class BasicNltkAnnotator(BaseAnnotator):
  def __init__(self):
    pass

  def annotate(self, sentence):
    tokens = word_tokenize(sentence)
    pos_tagged_tokens = pos_tag(tokens)
    anno_words = []
    for i,(token,pos) in enumerate(pos_tagged_tokens):
      anno_words.append(AnnotatedWord(index=i,word=token,pos=pos))
    return AnnotatedSentence(anno_words)
    


