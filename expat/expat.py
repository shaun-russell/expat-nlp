''' Main application for text analysis and processing using patterns. '''

# Better description of thing.
import click
import core.parse as parse
import core.annotators as anno
import core.structures as struct
import core.match as match
import core.search as search
import core.helpers as helpers

from core.main import preprocess_pattern
from colorama import init

# used to tell Click that -h is shorthand for help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])




# START CLI COMMANDS
# This is all Click CLI setup. If wanting actual code, scroll to the cli() function.
@click.command(context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r',encoding='utf8'), required=True)
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
# @click.option('--delimiter', '-d', type=str, default='\t',
#               help='Which delimiter to use IF splitting. Default is TAB.')
@click.option('--export-matrix', '-x', type=click.File('w+', encoding='utf8'),
              help='A filename to export the pattern matrix to.')
@click.option('--debug-pattern', '-g', type=str,
              help='A pattern to run full verbose output on.')
@click.option('--heading', type=str, default='sentence',
              help='The heading to use for the sentence output. Default is "sentence", but override this is there is more than 1 column in the sentences file.')
@click.option('--output-type', '-o', type=click.Choice(['csv', 'tsv', 'arff']), default='csv',
              help='What format the exported matrix should be in.')

# flags
# @click.option('--no-header', '-n', is_flag=True,
#               help='Read the first line as data, rather than as a header')
# @click.option('--ignore-case', '-i', is_flag=True,
              # help='Something about case-sensitivity.')
@click.option('--stepwise', is_flag=True,
              help='Manually cycle through the sentences to scan what is matched.')
@click.option('--verbose', '-v', is_flag=True,
              help='Enables information-dense terminal output.')

# other required arguments
@click.version_option(version='1.0.0')


# main entry point function
def cli(in_file, pattern_file, extension_file, annotator,
        selector, corenlp_url, debug_pattern, output_type,
        export_matrix, heading, verbose, stepwise):
  ''' The main annotation program called from the command line. '''
  # --------------------
  # INIT, CONFIG, AND LOADING
  # --------------------

  # Interface related messages.
  if verbose:
    click.echo('Processing...')
  if not in_file:
    click.echo('Input file not found.')
  if not pattern_file:
    click.echo('Pattern file not found.')

  if not export_matrix:
    click.echo('NOTE: NOT SAVING RESULTS.')
    click.echo('Use the --export-matrix option to save output.')

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
  else:
    # nltk is default because it can be run locally without setup hassle
    click.echo('No annotator specified, using NLTK.')
    selected_annotator = 'nltk'

  # TODO: add more annotators here if needed.
  spatial_annotator = None
  if extension_file:
    # default extension file parser
    extensions = parse.ExtensionParser.parse(extension_file)
    spatial_annotator = anno.TypeExtensionAnnotator(extensions)

  # If new search algorithm needed, create a conditional to pick a search method
  search_method = search.BreadthFirstWithQueue()

  active_selector = None
  if selector == 'containing':
    click.echo('Using: containing selection algorithm')
    active_selector = anno.ContainingSelector()
  else:
    click.echo('No selector specified.')

  # parse the header for column indexes
  # if not no_header:
  #   header_line = in_file.readline()

  # this is what the annotation matrix is saved in
  output_matrix = []
  # any new non-pattern columns need to be added in the header
  # (ideally after 'extracted' and before the patterns)
  delimiter = ','
  if '\t' in heading:
    delimiter = '\t'
  output_matrix.append(heading.split(delimiter) + ['abstracted'] + [p.name for p in all_patterns.patterns if not p.preprocess])

  # init some variables to keep track of progress
  count = 0
  all_lines = in_file.readlines()
  linenum = len(all_lines)

  # --------------------
  # MAIN ANNOTATION LOOP
  # --------------------

  for line in all_lines:
    # blank lines and junk get skipped
    if len(line) < 3:
      continue

    # format the line for pain-free annotation
    cleaned_line,excess = helpers.get_content_and_extra(heading, helpers.clean_line(line))
    if verbose:
      click.echo("{}\n{}\t{}".format(line, cleaned_line, excess))
    # the selected annotator annotates the sentence
    annotated_sentence = selected_annotator.annotate(cleaned_line)
    if spatial_annotator != None:
      annotated_sentence = spatial_annotator.extend(annotated_sentence)

    if verbose:
      # big pretty print of sentence with indices, words, pos, ner, and type
      # annotations from the provided extensions set.
      click.echo('Annotated Sentence:')
      click.echo(' '.join(['{}.{} ({},[{}]:{}) '.format(
          x.index, x.word, click.style(x.pos, fg='cyan'),
          click.style(x.types, fg='bright_magenta'),
          click.style(x.ner, fg='bright_green')) for x in annotated_sentence.words]))

    # ______________________
    # PREPROCESSING PATTERNS
    # Find all matches in the line for every pattern
    matched_patterns = []
    for pattern in [p for p in all_patterns.patterns if p.preprocess]:
      results = preprocess_pattern(pattern, annotated_sentence, active_selector, search_method,
                                  verbose=verbose, debug_pattern=debug_pattern)
      for res in results:
        matched_patterns.append(res)

    # Reduce the patterns to as many that can fit without overlapping, applying longest patterns first
    focus_patterns = []
    if active_selector != None:
      focus_patterns = active_selector.reduce_pattern_collection(matched_patterns, verbose=verbose)
    # PRINT PATTERN RESULTS IN CONTEXT
    if verbose:
      helpers.print_sentence_patterns([x for _,x in focus_patterns], annotated_sentence.words)
      helpers.print_sentence_pattern_categories(focus_patterns, annotated_sentence.words)
    
    # POST-PROCESSING PATTERNS
    reduced_sentence = helpers.get_reduced_sentence(focus_patterns, annotated_sentence.words)
    if verbose:
      # some print formatting thing
      click.echo(' '.join(['{}.{} ({},[{}]:{}) '.format(
        x.index, x.word, click.style(x.pos, 'cyan'),
         click.style(x.types, fg='bright_magenta'),
         click.style(x.ner, fg='bright_green')) for x in reduced_sentence.words]))

    row = ['"{}"'.format(cleaned_line)] + excess.split(delimiter) + ['"' + ' '.join([x.word for x in reduced_sentence.words]) + '"']

    matched_patterns = []
    for pattern in [p for p in all_patterns.patterns if not p.preprocess]:
      results = preprocess_pattern(pattern, reduced_sentence, active_selector, search_method,
                                  verbose=verbose, debug_pattern=debug_pattern)
      new = 0                            
      for res in results:
        new += 1
        matched_patterns.append(res)
      
      # save row
      row.append(str(new))

    focus_patterns = []
    if active_selector != None:
      focus_patterns = active_selector.reduce_pattern_collection(matched_patterns, verbose=False)
    # PRINT PATTERN RESULTS IN CONTEXT
    if verbose:
      helpers.print_sentence_patterns([x for _,x in focus_patterns], reduced_sentence.words)
      helpers.print_sentence_pattern_categories(focus_patterns, reduced_sentence.words)

    # SAVE PATTERNED LINE
    output_matrix.append(row)

    # PRINT PROGRESS (program speed depends on num of patterns and sentences)
    count += 1
    if count % 20 == 0:
      click.echo('\r{} of {}'.format(count, linenum), nl=False)

    # ALLOW MANUAL PROGRESSION FOR DEBUGGING OR VIEWING
    if stepwise:
      input('\rPress <enter> to continue...\n')

   
  if verbose:
    click.echo('Saving...')

  # SAVE ALL TO FILE (if file provided)
  delimiter = ','
  if output_type == 'csv':
    delimiter = ','
  elif output_type == 'tsv':
    delimiter = '\t'

  eol = '\n'

  if output_type != 'arff':
    if export_matrix:
      for row in output_matrix:
        export_matrix.write(delimiter.join(row) + eol)
      export_matrix.close()
    # if verbose:
    click.echo('\nSaved as {} in {}'.format(output_type, export_matrix.name))
  else:
    # might break this out into a separate function...
    # ARFF file generation
    # create the attribute lines for each thing in the header
    attributes = ''
    for i,column in enumerate(output_matrix[0]):
      datatype = 'NUMERIC' if helpers.is_number(output_matrix[1][i]) else 'STRING'
      attributes += ('@ATTRIBUTE "{}" {}{}'.format(column.replace('"',''), datatype, eol))
    
    export_matrix.write('@RELATION expat-generated-output' + eol)
    export_matrix.write(attributes)
    export_matrix.write('@DATA'+ eol)

    export_matrix.write(','.join(row) + '\n')
    export_matrix.write(eol.join([','.join(x) for x in output_matrix[1:]]))
    click.echo('\nSaved as {} in {}'.format(output_type, export_matrix.name))
    export_matrix.close()
