''' Search algorithms. ''' 
import click
from collections import deque
from copy import copy
from core.match import PatternMatcher
from core.structures import AnnotatedSentence,Pattern

class GraphSearch():
  ''' Base class? Are base classes even needed in python? '''
  @staticmethod
  def find_all_paths(graph, start_node, queue):
    print('default, why is this called?')
    return []


class BreadthFirstWithQueue(GraphSearch):
  @staticmethod
  def find_all_paths(graph, start_node, queue, verbose=False):
    ''' Provide a graph reference, the starting node, and the search queue. '''
    # The debug/verbose statements are useful for debugging, but they could
    # probably be cleaned up and re-worded.
    if verbose:
      q = [x.word for x in queue]
      q.reverse()
      click.echo('SQ: ' + ' '.join(q))

    # if the queue is empty, pop() will make it fail. Also there are no patterns
    # that could be found on an empty list, so we just exit here.
    if not queue:
      if verbose:
        click.echo(click.style('No queue, exiting.', fg='bright_red'))
      return []
    first_word = queue.pop()
    # first word doesn't match the start node, exit because no point continuing
    if verbose:
      click.echo('{}({})[{}] == {}({})[{}] ?'.format(first_word.word, first_word.pos, first_word.types, start_node.word, start_node._pos, start_node._types))
    if not PatternMatcher.word_matches_pattern(first_word, start_node):
      if verbose:
        click.echo(click.style("'{}' doesn't match, exiting.".format(first_word.word), fg='bright_red'))
      return []

    # add the first word back in so we can look at the successors
    # The main search loop evaluates child elements, so we need to insert the
    # starting parent node back into the queue, so it can be treated like a child
    queue.appendleft(first_word)
    if verbose:
      click.echo("Word = {}".format(click.style(first_word.word, fg='cyan')))
    # prep the queue with the first items
    search_queue = deque()
    search_queue.append((start_node,queue,[first_word]))

    saved_paths = []
    # go until the search queue is empty
    while search_queue:
      if verbose:
        click.echo('>  Search queue loop:')
      # each search_queue item is the graph-node, the current queue of words,
      # and the saved path
      node,wordq,path = search_queue.pop()
      if verbose: print('Popped:', node.word, node._pos, [x.pos for x in path])

      if verbose: print('Successors (before end check):', [x._pos for x in graph.successors(node)])
      if len(list(graph.successors(node))) == 0:
        if verbose:
          click.echo(click.style('END GRAPH, SAVING PATTERN', fg='green'))
          click.echo(click.style(' '.join([x.word for x in path]), fg='cyan'))
        # reached a final node, save this path.
        saved_paths.append((path))

      # for every successor, add to the queue
      for i,successor in enumerate(graph.successors(node)):
        queue_copy = copy(wordq)
        # exit if queue is empty, because popping an empty queue throws an error
        if not queue_copy:
          break
        word = queue_copy.pop()
        if verbose:
          click.echo('Checking word: {}'.format(click.style(word.word, fg='bright_cyan')))
          click.echo('Successor -> {} {} {}'.format(i, successor.word, successor._pos))
        # check that the item in the queue matches the starting pattern
        check = False
        if verbose:
          check = True
          click.echo('Checking: {}({}) == {}({})'.format(click.style(word.word, fg='bright_cyan'), word.pos, click.style(successor.word, fg='bright_yellow'), successor._pos))
        if PatternMatcher.word_matches_pattern(word, successor, verbose=verbose):
          if verbose: print('Successor MATCH', word.word, word.pos, successor.word, successor._pos)
          # if this word matches the 
          if word not in path:
            path += [word]
          search_queue.append((successor, queue_copy, path))
        else:
          if verbose and check:
            click.echo(click.style('No match.', fg='bright_yellow'))

    return saved_paths


class MatchBuilder():
  @staticmethod
  def find_all_matches(annotated_sentence, pattern, algorithm, verbose=False):
    sentence_queue = annotated_sentence.get_queue()
    matches = []
    # for every word in the sentence...
    while sentence_queue:
      # get the word that starts the queue
      # make a copy because we can have queues
      # this could be improved, but basically we get the first word to do the
      # initial evaluation, but because we still need this word, we put it back in.\
      # Once the tests work, try just feed every word into the algorithm.find_all_paths(...)
      # and see if the result is the same (should be the proper way)
      queuecopy = copy(sentence_queue)
      # see if the word matches any of the entry points for the pattern
      for entry in pattern.graph_entry_points:
        q = copy(queuecopy)
        word = q.pop()
        q.append(word)
        if verbose:
          click.echo('Entry point: {}({})'.format(entry.word, entry._pos))
          click.echo('Checking: {}({})'.format(word.word, word.pos))
        results = algorithm.find_all_paths(pattern.graph, entry, q, verbose)
        if len(results) > 0:
          matches += results
      sentence_queue.pop()
    return matches

