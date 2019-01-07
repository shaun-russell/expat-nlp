''' Search algorithms. ''' 
import click
from collections import deque
from copy import copy
from core.match import PatternMatcher
from core.structures import AnnotatedSentence,Pattern

class GraphSearch():
  ''' Base class for Graph Searching Algorithms.
      Probably not as important in Python since duck-typing... '''
  @staticmethod
  def find_all_paths(graph, start_node, queue):
    print('# Uh oh! If this is called, something has not been properly configured.')
    return []


class BreadthFirstWithQueue(GraphSearch):
  ''' Search the graph using a Breadth-First search,
      with each level popping the search queue. '''
  @staticmethod
  def find_all_paths(graph, start_node, queue, verbose=False):
    ''' Provide a graph reference, the starting node, and the search queue. '''
    # The debug/verbose statements are useful for debugging, but they could
    # probably be cleaned up and re-worded.
    if verbose:
      # This just prints the queue in normal-order rather than reverse-order.
      q = [x.word for x in queue]
      q.reverse()
      click.echo('SearchQ: ' + ' '.join(q))

    # if the queue is empty, pop() will throw an exception. Also there are no patterns
    # that could be found with an empty queue, so we just exit here.
    if not queue:
      if verbose:
        click.echo(click.style('No queue, exiting.', fg='bright_red'))
      return []

    # Python doesn't provide a peek() method on queues, so to look at the first
    # item, it has to be popped and then reinserted to the *front* of the queue.
    first_word = queue.pop()

    # If the head of the queue doesn't match the pattern's start node, stop searching.
    # A queue of words must form a path through the pattern 'maze'. If it fails the
    # entry check, then no complete paths can exist.
    if verbose:
      click.echo('{}({})[{}] == {}({})[{}] ?'.format(first_word.word,
                                                     first_word.pos,
                                                     first_word.types,
                                                     start_node.word,
                                                     start_node._pos,
                                                     start_node._types))
    if not PatternMatcher.word_matches_pattern(first_word, start_node):
      if verbose:
        click.echo(click.style("'{}' doesn't match, stopping search.".format(first_word.word),
                               fg='bright_red'))
      return []

    # Add the first_word back into the queue so we can look at the successor nodes
    # The main search loop evaluates child elements, so we need to insert the
    # starting parent node back into the queue, so it can be treated like a child
    queue.appendleft(first_word)
    if verbose:
      click.echo("Word = {}".format(click.style(first_word.word, fg='cyan')))

    # We have a queue of words (the annotated sentence), but now we need to create
    # a search_queue for the breadth-first-search algorithm implementation.
    search_queue = deque()
    search_queue.append((start_node,queue,[first_word]))

    saved_paths = []
    # go until the search queue is empty
    while search_queue:
      if verbose:
        click.echo('>  Search queue loop:')
      # each search_queue item is the graph-node, the current queue of words,
      # and the path/route taken through the pattern graph so far.
      node,wordq,path = search_queue.pop()
      if verbose:
        click.echo('Popped: {}({}) : {}'.format(node.word,
                                                node._pos,
                                                ','.join([x.pos for x in path])))

      if verbose:
        click.echo('Successors (before end): {}'.format(','.join([x._pos for x in graph.successors(node)])))
      # If end of graph (successfully found a path through the graph), save the
      # route as a matched pattern.
      if len(list(graph.successors(node))) == 0:
        if verbose:
          click.echo(click.style('END GRAPH, SAVING PATTERN', fg='green'))
          click.echo(click.style(' '.join([x.word for x in path]), fg='cyan'))
        # reached a final node, save this path.
        saved_paths.append((path))

      # Breadth-first-search through all the successor nodes to find all paths
      # that match this pattern.
      for i,successor in enumerate(graph.successors(node)):
        # copy the queue rather than reference to avoid feeding a half-chewed
        # queue to the next iteration of the loop.
        queue_copy = copy(wordq)
        # exit if empty queue, because popping an empty queue throws an exception
        if not queue_copy:
          break

        # algorithm is evaluating the head of this queue
        word = queue_copy.pop()
        if verbose:
          click.echo('Checking word: {}'.format(click.style(word.word, fg='bright_cyan')))
          click.echo('Successor -> {} {} {}'.format(i, successor.word, successor._pos))

        if verbose:
          click.echo('Checking: {}({}) == {}({})'.format(click.style(word.word, fg='bright_cyan'),
                                                         word.pos,
                                                         click.style(successor.word, fg='bright_yellow'),
                                                         successor._pos))
        # Compare the word's attributes with the pattern node's attribute requirements
        if PatternMatcher.word_matches_pattern(word, successor, verbose=verbose):
          if verbose:
            click.echo('Successor MATCH: {}({}) = {}({})'.format(word.word,
                                                                  word.pos,
                                                                  successor.word,
                                                                  successor._pos))
          # Avoids rare duplicates in path. Not sure why this happens, but this
          # conditional prevents the effects!
          if word not in path:
            path += [word]
          # Append the successors to the BFS queue
          search_queue.append((successor, queue_copy, path))
        else:
          if verbose:
            click.echo(click.style('No match.', fg='bright_yellow'))

    return saved_paths


class MatchBuilder():
  @staticmethod
  def find_all_matches(annotated_sentence, pattern, algorithm, verbose=False):
    ''' Returns a list of all the paths that can be found in the provided sentence
        using the provided pattern graph. The algorithm used to traverse the graph
        and find patterns is also needed. '''
    sentence_queue = annotated_sentence.get_queue()
    matches = []
    # for every word in the sentence...
    while sentence_queue:
      # get the word that starts the queue
      # make a copy because we can have queues
      # this could be improved, but basically we get the first word to do the
      # initial evaluation, but because we still need this word, we put it back in.
      # Once the tests work, try just feed every word into the algorithm.find_all_paths(...)
      # and see if the result is the same (should be the proper way)
      queuecopy = copy(sentence_queue)
      # see if the word matches any of the entry points for the pattern
      for entry in pattern.graph_entry_points:
        # work with values rather than references, otherwise later patterns
        # would be provided with empty lists (all the data has been popped)
        q = copy(queuecopy)
        word = q.pop()
        q.append(word)

        if verbose:
          click.echo('Entry point: {}({})'.format(entry.word, entry._pos))
          click.echo('Checking: {}({})'.format(word.word, word.pos))

        # get a list of all the paths through the pattern graph
        results = algorithm.find_all_paths(pattern.graph, entry, q, verbose)
        if len(results) > 0:
          matches += results
      sentence_queue.pop()
    return matches

