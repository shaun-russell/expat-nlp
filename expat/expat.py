''' Tool for FUNCTION and FUNCTION. '''

# Better description of thing.
import click
import core.parse as parse
import core.annotators as anno
import core.structures as struct
import core.match as match
import core.search as search
from colorama import init

# used to tell Click that -h is shorthand for help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# individual functions go here
def print_matches(pattern, matches):
  ''' Pretty-print the matches that were found. '''
  click.echo('PATTERN: {} ({})'.format(pattern.name, pattern.classname))
  for i,match in enumerate(matches):
    all_words = ['({}. {})'.format(w.index, w.word) for w in match]
    click.echo('  {}: {}'.format(i+1, " ".join(all_words)))

def print_sentence_patterns(patterns, annotated_words):
  for word in annotated_words:
    for patt in patterns:
      for pw in patt:
        if pw.index == word.index:
          word = click.style(word, fg='green')
    click.echo('', nl=False)
  click.echo('')

# START CLI COMMANDS
@click.command(context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r'), required=True)
@click.argument('pattern-file', type=str, required=True)
# @click.argument('out-file', type=click.File('w+', encoding='utf8'), required=True)

@click.option('--extension-file', '-x', type=click.File('r'), default='',
              help='Extension annotators for type annotation.')

# optional arguments
@click.option('--annotator', '-n', type=click.Choice(['nltk', 'corenlp']),
              default='nltk', help='A non-flag option that needs a value.')
@click.option('--corenlp-url', '-u', type=str, default='http://localhost:9000',
              help='The url of the CoreNLP server.')

@click.option('--delimiter', '-d', type=str, default='\t',
              help='Which delimiter to use IF splitting. Default is TAB.')
@click.option('--split-index', '-i', type=int, default=-1,
              help='Which index to split on. Default is -1, which means the line is not split.')

@click.option('--ignore-case', '-i', is_flag=True,
              help='Something about case-sensitivity.')
@click.option('--automated', '-a', is_flag=True,
              help="Don't wait before proceeding to the next sentence.")
@click.option('--verbose', '-v', is_flag=True,
              help='Enables information-dense terminal output.')

# other required arguments
@click.version_option(version='1.0.0')


# main entry point function
def cli(in_file, pattern_file, extension_file,
        annotator, corenlp_url, delimiter, split_index,
        automated, verbose, ignore_case):
  '''
    A description of what this main function does.
  '''

  if verbose:
    click.echo('Processing...')
  
  if not in_file:
    click.echo('Pattern file not found.')
  if not pattern_file:
    click.echo('Pattern file not found.')
  # load all files from patterns
  all_patterns = parse.Parser.parse_patterns(pattern_file, True)

  # Use the correct annotator
  selected_annotator = None
  if annotator == 'nltk':
    selected_annotator = anno.BasicNltkAnnotator()
  elif annotator == 'corenlp':
    selected_annotator = anno.StanfordCoreNLPAnnotator(corenlp_url)

  # TODO: make this flexible
  spatial_annotator = None
  if extension_file != ''
    categories = parse.ExtensionParser.parse(extension_file)
    spatial_annotator = anno.TypeExtensionAnnotator()

  # At some point, implement the search/graph generation algorithm selection here
  search_method = search.BreadthFirstWithQueue()

  # store lines in here
  saved_lines = []
  

  # for tracking progress
  word_index = 0

  # parse the header for column indexes
  header_line = in_file.readline()
  header = header_line.strip()
  for line in in_file:
    # the selected annotator annotates the sentence
    annotated_sentence = selected_annotator.annotate(line)
    click.echo('\nAnnotated Sentence:')
    click.echo(' '.join(['{} ({})'.format(x.word, click.style(x.pos, 'cyan')) for x in annotated_sentence.words]))
    # then find all matches in that sentence for every pattern
    all_patterns = []
    for pattern in all_patterns.patterns:
      pattern_matches = search.MatchBuilder.find_all_matches(annotated_sentence,
                                                             pattern,
                                                             search_method)
      if verbose:
        print_matches(pattern, pattern_matches)

    print_sentence_patterns(all_patterns, annotated_sentence.words)

    # periodic progress updates
    # word_index += 1
    # if verbose and word_index % 10 == 0:
    #   click.echo('\rProcessed {}.'.format(word_index), nl=False)
   
  # TODO: here
  # implement objects that select and merge patterns

  # print sentence, using colours (1 for each pattern class?), to show what is matched


  # if verbose: click.echo('Saving...')

  # use the same line endings as the input
  # eol = '\r\n' if dos_eol else '\n'

  # # write the matched lines to the output file
  # for content in saved_lines:
  #   # replace content with useful stuff
  #   out_file.write('{}{}'.format(content, eol))
  # out_file.close()

  # # finished
  # if verbose: click.echo('Saved')