''' Big chungus functions go in here. '''
import click
from core.search import MatchBuilder
import core.helpers as helpers


def preprocess_pattern(pattern, sentence, active_selector, search_method,
                       verbose=False, debug_pattern=''):
  # init debug printing, if applicable
  debug = False
  if pattern.name == debug_pattern:
    click.echo(click.style('Debugging:', fg='white', bg='red'))
    debug = True

  # pattern match search
  found_patterns = MatchBuilder.find_all_matches(sentence,
                                                 pattern,
                                                 search_method,
                                                 debug)
  pattern_matches = sorted(helpers.remove_duplicate_lists(found_patterns),
                                                    key=len,
                                                    reverse=True)

  results = []
  if active_selector == None:
    # no selector, return everything
    results.append((pattern, pattern_matches))
  else:
  # use the selector to reduce/focus the matched patterns to a subset
    selected = active_selector.select_patterns(pattern,
                                                pattern_matches,
                                                verbose=debug)
    # Selector returns a list of pattern lists, so de-list the results.
    for s in selected:
      results.append((pattern, s))
  
  # friendly print/debug section
  if debug:
    click.echo(click.style('End Debugging.', fg='white', bg='green'))
  if verbose:
    helpers.print_matches(pattern, pattern_matches)

  return results
