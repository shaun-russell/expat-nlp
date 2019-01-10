''' Helper functions. '''

import click
from core.structures import AnnotatedWord,AnnotatedSentence

# -----------------
# UTILITY FUNCTIONS
# -----------------

def remove_duplicate_lists(messy_list):
  ''' Reduces a list of lists to only the unique lists'''
  result = []
  for item in messy_list:
    if item not in result:
      result.append(item)
  return result

def is_number(string):
  ''' Returns true if the string is a number. '''
  try:
      float(string)
  except ValueError:
      return False
  return True

def clean_line(line):
  ''' Strip trailing and leading whitespace, then trailing and leading quote marks. '''
  return line.strip().strip("'")

def get_reduced_sentence(patterns, annotated_words):
  ''' Replaces preprocessor patterns with a single classname word,
      e.g. "the book" would become "NOUN". '''
  skip_num = 0
  words = []
  index = 0
  for word in annotated_words:
    if skip_num > 0:
      skip_num -= 1
      continue
    found = False
    for ptype,pattern_words in patterns:
      if found:
        break
      for pword in pattern_words:
        if found:
          break
        if pword.index == word.index:
          words.append(AnnotatedWord(word=ptype.classname, index=index, lemma=word.lemma, pos='NULL'))
          skip_num = len(pattern_words) - 1
          found = True
          break
    if not found:
      word.index = index
      words.append(word)
  
  # repair indices
  index = 0
  for word in words:
    word.index = index
    index += 1
  return AnnotatedSentence(words)

def get_content_and_extra(heading, line):
  ''' Splits a line into 'annotating' and 'non-annotating' parts. The function
      expects the sentence first, followed by classification values (with no quote
      marks in classifications. This prevents the classifications being
      annotated as part of the string/sentence. Non-annotating will be None if no
      delimiter found in the heading.'''
  delim_idx = 0
  annotating = ''
  non_annotating = ''

  # find the index of the first delimiter
  if '\t' in heading:
    # First tab character is the end of the first column.
    delim_idx = line.find('\t')
  elif ',' in heading:
    # Last " character is the end of a sentence. Can't look for commas,
    # because the text content could contain a comma.
    delim_idx = line.rfind('"') + 1
  else:
    delim_idx = len(line)

  annotating = line[0:delim_idx].replace('"','').strip('\t').strip(',')
  non_annotating = line[delim_idx:].replace('"','').strip('\t').strip(',')

  # Maybe make this a proper object, rather than a mystery tuple...
  return (annotating, non_annotating)


# -------------------------------
# PRETTY PRINTING DEBUG FUNCTIONS
# -------------------------------
def print_sentence_patterns(patterns, annotated_words):
  ''' Prints a sentence on a line, highlighting pattern words GREEN. '''
  words = []
  # these variable names don't matter that much because they're just for looping.
  for word in annotated_words:
    found = False
    for patt in patterns:
      if found:
        break
      for pw in patt:
        if found:
          break
        if pw.index == word.index:
          words.append(click.style(word.word, fg='green'))
          found = True
          break
    if not found:
      words.append(word.word)
  click.echo(' '.join(words))

def print_sentence_pattern_categories(patterns, annotated_words):
  ''' Prints a sentence, highlighting pattern groups (and their component words). '''
  skip_num = 0
  words = []
  for word in annotated_words:
    # if a pattern is applied, skip all the words that are part of that pattern.
    # This avoids overlapping pattern application, e.g. [The,Cave] and [Cave] 
    # will match on the <The> word, then <Cave>. Since <Cave> is the next word,
    # but we've already matched it, we skip 1 word i.e. len(pattern)
    if skip_num > 0:
      skip_num -= 1
      words.append(click.style(str(word.index) + '.' + word.word, bg='bright_yellow', fg='black'))
      continue

    # these variable names don't matter that much because they're just for looping.
    found = False
    for p,patt in patterns:
      if found:
        break
      for pw in patt:
        if found:
          break
        if pw.index == word.index:
          # If the word matches, insert this pattern category and skip
          # pattern checks for all the words contained in this pattern
          # to prevent overlapping patterns when printing.
          words.append(click.style(p.classname + ':',
                                    fg='white',
                                    bg='cyan'))
          words.append(click.style(str(word.index) + '.' + word.word,
                                    bg='bright_yellow',
                                    fg='black'))
          skip_num = len(patt) - 1
          found = True
          break
    if not found:
      words.append(str(word.index) + '.' + word.word)
  click.echo(' '.join(words))


# individual functions go here
def print_matches(pattern, matches):
  ''' Pretty-print the matches that were found. '''
  click.echo('{}: {} ({})'.format(click.style('PATTERN', fg='bright_yellow'), pattern.name, pattern.classname))
  for i,match in enumerate(matches):
    all_words = ['({}. {})'.format(w.index, w.word) for w in match]
    click.echo('  {}: {}'.format(i+1, " ".join(all_words)))


