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
  click.echo('{}: {} ({})'.format(click.style('PATTERN', fg='bright_yellow'), pattern.name, pattern.classname))
  for i,match in enumerate(matches):
    all_words = ['({}. {})'.format(w.index, w.word) for w in match]
    click.echo('  {}: {}'.format(i+1, " ".join(all_words)))

def remove_duplicate_lists(messy_list):
  result = []
  for item in messy_list:
    if item not in result:
      result.append(item)
  return result

def print_sentence_patterns(patterns, annotated_words):
  # print('Applied Patterns')
  words = []
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
  # print('Preprocessed Patterns')
  skipnum = 0
  # index = 0
  words = []
  for word in annotated_words:
    # word.index = index
    # index += 1
    if skipnum > 0:
      skipnum -= 1
      words.append(click.style(str(word.index) + '.' + word.word, bg='bright_yellow', fg='black'))
      continue
    found = False
    for p,patt in patterns:
      if found:
        break
      for pw in patt:
        if found:
          break
        if pw.index == word.index:
          words.append(click.style(p.classname + ':', fg='white', bg='cyan'))
          words.append(click.style(str(word.index) + '.' + word.word, bg='bright_yellow', fg='black'))
          skipnum = len(patt) - 1
          found = True
          break
    if not found:
      words.append(str(word.index) + '.' + word.word)
  click.echo(' '.join(words))

def get_reduced_sentence(patterns, annotated_words):
  skipnum = 0
  words = []
  index = 0
  for word in annotated_words:
    if skipnum > 0:
      skipnum -= 1
      continue
    found = False
    for p,patt in patterns:
      if found:
        break
      for pw in patt:
        # for pw in px:
        if found:
          break
        if pw.index == word.index:
          words.append(struct.AnnotatedWord(word=p.classname, index=index, lemma=word.lemma, pos='NULL'))
          skipnum = len(patt) - 1
          found = True
          # index += 1
          break
    if not found:
      word.index = index
      words.append(word)
      # index += 1
  
  # repair indices?
  index = 0
  for word in words:
    word.index = index
    index += 1
  return struct.AnnotatedSentence(words)


# START CLI COMMANDS
@click.command(context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r'), required=True)
@click.argument('pattern-file', type=str, required=True)
# @click.argument('out-file', type=click.File('w+', encoding='utf8'), required=True)

@click.argument('extension-file', type=click.File('r'), required=True)

# optional arguments
@click.option('--annotator', '-a', type=click.Choice(['nltk', 'corenlp']),
              default='nltk', help='The annotator to use for tagging.')
@click.option('--selector', '-s', type=click.Choice(['none', 'containing']),
              default='none', help='Which type of selection algorithm to use to focus the patterns.')
@click.option('--corenlp-url', '-u', type=str, default='http://localhost:9000',
              help='The url of the CoreNLP server.')

@click.option('--delimiter', '-d', type=str, default='\t',
              help='Which delimiter to use IF splitting. Default is TAB.')
@click.option('--split-index', '-i', type=int, default=-1,
              help='Which index to split on. Default is -1, which means the line is not split.')
@click.option('--export-matrix', '-x', type=click.File('w+', encoding='utf8'),
              help='A filename to export the pattern matrix to.')
@click.option('--debug-pattern', '-g', type=str,
              help='A pattern to run full verbose output on.')
@click.option('--heading', type=str, default='sentence',
              help='The heading to use for the sentence output. Default is "sentence", but override this is there is more than 1 column in the sentences file.')

@click.option('--no-header', '-n', is_flag=True,
              help='Read the first line as data, rather than as a header')
@click.option('--ignore-case', '-i', is_flag=True,
              help='Something about case-sensitivity.')
@click.option('--stepwise', is_flag=True,
              help='Manually cycle through the sentences to scan what is matched.')
@click.option('--verbose', '-v', is_flag=True,
              help='Enables information-dense terminal output.')

# other required arguments
@click.version_option(version='1.0.0')


# main entry point function
def cli(in_file, pattern_file, extension_file,
        annotator, selector, corenlp_url, delimiter, split_index, debug_pattern, export_matrix, heading,
        no_header, verbose, ignore_case, stepwise):
  '''
    A description of what this main function does.
  '''

  if verbose:
    click.echo('Processing...')
  
  if not in_file:
    click.echo('Input file not found.')
  if not pattern_file:
    click.echo('Pattern file not found.')
  # load all files from patterns
  all_patterns = parse.Parser.parse_patterns(pattern_file, True)
  click.echo('Loaded {} patterns'.format(len(all_patterns.patterns)))
  for pattern in all_patterns.patterns:
    click.echo(pattern.name)

  # Use the correct annotator
  selected_annotator = None
  if annotator == 'nltk':
    click.echo('Using NLTK annotator.')
    selected_annotator = anno.BasicNltkAnnotator()
  elif annotator == 'corenlp':
    click.echo('Using Stanford CoreNLP annotator.')
    selected_annotator = anno.StanfordCoreNLPAnnotator(corenlp_url)

  # TODO: make this flexible
  spatial_annotator = None
  if extension_file:
    categories = parse.ExtensionParser.parse(extension_file)
    spatial_annotator = anno.TypeExtensionAnnotator(categories)

  # At some point, implement the search/graph generation algorithm selection here
  search_method = search.BreadthFirstWithQueue()

  active_selector = None
  if selector == 'containing':
    print('Containing selection algorithm')
    active_selector = anno.ContainingSelector()

  # store lines in here
  saved_lines = []
  

  # for tracking progress
  word_index = 0

  # parse the header for column indexes
  if not no_header:
    header_line = in_file.readline()
    header = header_line.strip()

  output_matrix = []
  output_matrix.append([heading] + ['abstracted'] + [p.name for p in all_patterns.patterns if not p.preprocess])
  count = 0
  all_lines = in_file.readlines()
  linenum = len(all_lines)
  for line in all_lines:
    # the selected annotator annotates the sentence
    # strip trailing and leading whitespace, then trailing and leading quote marks
    cleaned_line = line.strip().strip("'")
    excess = ''
    if ',' in heading:
      last_comma_idx = cleaned_line.rfind('"')
      if last_comma_idx < 1:
        last_comma_idx = len(cleaned_line) - 1
      excess = cleaned_line[last_comma_idx+1:].replace('"','')
      cleaned_line = cleaned_line[0:last_comma_idx+1].replace('"','')
    if '\t' in heading:
      last_delim_idx = cleaned_line.rfind('\t')
      cleaned_line = cleaned_line[0:last_delim_idx].replace('"','')
      excess = cleaned_line[last_delim_idx:].replace('"','')

    # print('CL',cleaned_line, 'EX',excess)
    annotated_sentence = selected_annotator.annotate(cleaned_line)
    if spatial_annotator != None:
      annotated_sentence = spatial_annotator.extend(annotated_sentence)
    if verbose:
      click.echo('\nAnnotated Sentence:')
      click.echo(' '.join(['{}.{} ({},[{}]:{}) '.format(x.index, x.word, click.style(x.pos, 'cyan'), click.style(x.types, fg='bright_magenta'),click.style(x.ner, fg='bright_green')) for x in annotated_sentence.words]))

    # PREPROCESSING PATTERNS

    # then find all matches in that sentence for every pattern
    # make the csv line nicely formatted
    matched_patterns = []
    for pattern in [p for p in all_patterns.patterns if p.preprocess]:
      debug = False
      if pattern.name == debug_pattern:
        click.echo(click.style('Debugging:', fg='white', bg='red'))
        debug = True

      # run pattern search
      pattern_matches = sorted(remove_duplicate_lists(search.MatchBuilder.find_all_matches(annotated_sentence,
                                                             pattern,
                                                             search_method,
                                                             debug)), key=len, reverse=True)

      # use the selector to reduce/focus the matched patterns                                                            
      if active_selector == None:
        matched_patterns.append((pattern,pattern_matches))
      else:
        selected = active_selector.select_patterns(pattern, pattern_matches, verbose=debug)
        for s in selected:
          matched_patterns.append((pattern, s))

      if debug:
        click.echo(click.style('End Debugging.', fg='white', bg='green'))
      if verbose:
        print_matches(pattern, pattern_matches)

    # Reduce the patterns to as many that can fit without overlapping, applying longest patterns first
    focus_patterns = active_selector.reduce_pattern_collection(matched_patterns, verbose=verbose)
    # PRINT PATTERN RESULTS IN CONTEXT
    if verbose:
      print_sentence_patterns([x for _,x in focus_patterns], annotated_sentence.words)
      print_sentence_pattern_categories(focus_patterns, annotated_sentence.words)
    
    # POST-PROCESSING PATTERNS
    reduced_sentence = get_reduced_sentence(focus_patterns, annotated_sentence.words)
    if verbose: click.echo(' '.join(['{}.{} ({},[{}]:{}) '.format(x.index, x.word, click.style(x.pos, 'cyan'), click.style(x.types, fg='bright_magenta'),click.style(x.ner, fg='bright_green')) for x in reduced_sentence.words]))
    matched_patterns = []
    row = ["\"{}\"{},{}".format(cleaned_line, excess, ' '.join([x.word for x in reduced_sentence.words]))]
    for pattern in [p for p in all_patterns.patterns if not p.preprocess]:
      debug = False
      if pattern.name == debug_pattern:
        click.echo(click.style('Debugging:', fg='white', bg='red'))
        debug = True

      # run pattern search
      pattern_matches = sorted(remove_duplicate_lists(search.MatchBuilder.find_all_matches(reduced_sentence,
                                                             pattern,
                                                             search_method,
                                                             debug)),key=len, reverse=True)

      # use the selector to reduce/focus the matched patterns                                                            
      if active_selector == None:
        matched_patterns.append((pattern,pattern_matches))
      else:
        selected = active_selector.select_patterns(pattern, pattern_matches, verbose=debug)
        for s in selected:
          matched_patterns.append((pattern, s))
        # matched_patterns += active_selector.select_patterns((pattern, pattern_matches), verbose=verbose)
        # matched_patterns.append((pattern, active_selector.select_patterns(pattern, pattern_matches, verbose=debug)))


      if debug:
        click.echo(click.style('End Debugging.', fg='white', bg='green'))
      # Print all matches of this pattern
      if verbose:
        print_matches(pattern, pattern_matches)
      
      # save row
      row.append(str(len(pattern_matches)))

    focus_patterns = active_selector.reduce_pattern_collection(matched_patterns, verbose=False)
    # PRINT PATTERN RESULTS IN CONTEXT
    if verbose:
      print_sentence_patterns([x for _,x in focus_patterns], reduced_sentence.words)
      print_sentence_pattern_categories(focus_patterns, reduced_sentence.words)

    # SAVE PATTERNED LINE
    output_matrix.append(row)

    # SHOW PROGRESS
    count += 1
    if count % 20 == 0:
      click.echo('\r{} of {}'.format(count, linenum), nl=False)

    # ALLOW MANUAL PROGRESSION FOR DEBUGGING OR VIEWING
    if stepwise:
      input('\rPress a key to continue...\n')

   
  # SAVE ALL TO FILE
  if export_matrix:
    for row in output_matrix:
      export_matrix.write(','.join(row) + '\n')
  export_matrix.close()
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