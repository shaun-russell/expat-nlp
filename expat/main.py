''' Tool for FUNCTION and FUNCTION. '''

# Better description of thing.
import click

# used to tell Click that -h is shorthand for help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# individual functions go here
def functo(parpar):
  ''' this function does XYZ. '''
  pass

# START CLI COMMANDS
@click.command(context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r'), required=True)
@click.argument('out-file', type=click.File('w+', encoding='utf8'), required=True)

# optional arguments
@click.option('--optimungo', '-o', default='ABC',
              help='A non-flag option that needs a value.')

# flags
@click.option('--ignore-case', '-i', is_flag=True,
              help='Something about case-sensitivity.')
@click.option('--verbose', is_flag=True,
              help='Enables information-dense terminal output.')

# other required arguments
@click.version_option(version='1.0.0')


# main entry point function
def cli(in_file, out_file,
        optimungo, verbose, ignore_case):
  '''
    A description of what this main function does.
  '''
  

  
  # parse the header for column indexes
  header_line = in_file.readline()
  header = header_line.strip()
  
    
  # store lines in here
  saved_lines = []
  
  # use the same line endings as the input
  eol = '\r\n' if dos_eol else '\n'

  word_index = 0
  
  # main operation in here
  for line in in_file:
    
    # TODO
    # main processing loop (probably in its own file)





    # periodic progress updates
    word_index += 1
    if verbose and word_index % 10 == 0:
      click.echo('\rProcessed {}.'.format(word_index), nl=False)
   
  if verbose: click.echo('Saving...')

  # write the matched lines to the output file
  for content in saved_lines:
    # replace content with useful stuff
    out_file.write('{}{}'.format(content, eol))
  out_file.close()

  # finished
  if verbose: click.echo('Saved')