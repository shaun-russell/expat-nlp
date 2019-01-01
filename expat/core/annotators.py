''' Annotator objects. '''
from nltk.tokenize import word_tokenize
from core.match import StringMatching
from core.structures import AnnotatedSentence,AnnotatedWord
from nltk import pos_tag
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import json
import click

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
  def __init__(self, label, pos, filepath, lempos, lemmatiser, stemmer):
    self.label = label
    self.pos = pos
    with open(filepath, 'r', encoding='utf8') as wordfile:
      lines = wordfile.readlines()
      self.words = [stemmer.stem(lemmatiser.lemmatize(w.strip().lower(),pos=lempos)) for w in lines]
        # self.words = [w.strip() for w in lines]
    print(label, 'pos:', pos, 'word count:', len(self.words))

class ExtensionAnnotatorBase():
  def extend(self, annotated_sentence):
    return annotated_sentence

class TypeExtensionAnnotator(ExtensionAnnotatorBase):
  def __init__(self, categories, stem=True):
    ''' Initialise the annotator with { label: (pos,filepath) }. '''
    self.wordsets = []
    self.stemming = stem
    self.stemmer = PorterStemmer()
    self.lemmatiser = WordNetLemmatizer()
    for label,(pos,fpath,lempos) in categories.items():
     self.wordsets.append(ExtensionWordSet(label, pos, fpath, lempos, self.lemmatiser, self.stemmer))

  def extend(self, annotated_sentence):
    ''' Extend an existing annotated sentence with types (from wordlists). '''
    extended_sentence = []
    for word in annotated_sentence.words:
      # wordnet lemmatiser only accepts these 4 chars as pos-tags
      lemma = self.stemmer.stem(word.lemma.lower())
      if word.lemma == None or len(word.lemma) < 1:
        postag = word.pos[0].lower()
        postag = postag if postag in ['a','r','n','v'] else 'n'
        lemma = self.stemmer.stem(self.lemmatiser.lemmatize(word.word.lower(), pos=postag))

      # convert the current word types to a list
      word_types = word.types.split(',') if word.types != '' else []
      # for all the wordsets whose part of speech tags match the current word
      for wordset in [s for s in self.wordsets if StringMatching.is_match(word.pos, s.pos)]:
        if lemma in wordset.words:
          word_types.append(wordset.label)

      word.types = ','.join(word_types)
      extended_sentence.append(word)
    return AnnotatedSentence(extended_sentence)


class Selector():
  def select_patterns(self, patterns):
    return patterns
    

class ContainingSelector(Selector):
  def __init__(self):
    pass

  def _is_contained_in(self, parts, whole):
    # if there is a part that is not in the whole, then not contained
    whole_indices = [w.index for w in whole]
    for part in parts:
      if part.index not in whole_indices:
        return False
    # otherwise, everything was contained
    return True

  def select_patterns(self, pattern, matched, verbose=False):
    selected_patterns = []
    pattern_name = pattern if isinstance(pattern, str) else pattern.classname
    # sorted_patterns = sorted(matched, key=len, reverse=True)
    # do work in here
    if matched == []:
      return []
    if verbose: print('Filtering: ', pattern_name)
    for wordlist in matched:
      # wordlist is a list of AnnotatedWord objects
      found = False
      # if the words in the current matched pattern are already matched by an
      # existing pattern, we won't add it.
      # If [A,B,C] is an existing pattern, [B], [C], and [B,C] will be excluded because
      # [A,B,C] contains these.
      for existing in selected_patterns:
        if self._is_contained_in(wordlist, existing):
          found = True
          if verbose:
            # print('Deleting {}'.format([x.word for x in wordlist]))
            click.echo(click.style('Deleting {}'.format([x.word for x in wordlist]), fg="bright_yellow"))
          break
      if not found:
        selected_patterns.append(wordlist)
        if verbose: click.echo(click.style('Keeping {}'.format([x.word for x in wordlist]), fg="bright_cyan"))

    if verbose and len(selected_patterns) > 0:
      click.echo(click.style('> Reduced {} to the following patterns:'.format(pattern_name), fg="bright_green"))
      for s in selected_patterns:
        click.echo(' '.join([w.word for w in s]))
    return selected_patterns
  
  def plength(self,value):
    x,y = value
    words = [a.word for a in y]
    return len(words)

  def reduce_pattern_collection(self, matched_patterns, verbose=False):
    reduced = []
    if verbose:
      print(['{}:{}'.format(x.classname,[w.word for w in y]) for x,y in matched_patterns])
    things = sorted(matched_patterns, key=self.plength, reverse=True)
    if verbose:
      print(['{}:{}'.format(x.classname,[w.word for w in y]) for x,y in things])
      click.echo('Reducing across patterns...')
    for pattern,words in things:
      # if verbose:
        # print([w.word for w in words])
      for p,existing in reduced:
        if self._is_contained_in(words, existing):
          if verbose:
            click.echo(click.style('Deleting {}'.format([x.word for x in words]), fg="bright_yellow"))
          break
      else:
        if verbose: click.echo(click.style('Keeping {}'.format([x.word for x in words]), fg="bright_cyan"))
        reduced.append((pattern, words))

    if verbose:
      for x,pl in reduced:
        print([p.word for p in pl])
    return reduced