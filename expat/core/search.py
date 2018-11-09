''' Search algorithms. ''' 
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
    if verbose: print('SQ:', [x.word for x in queue])


    # if the queue is empty, pop() will make it fail. Also there are no patterns
    # that could be found on an empty list
    if not queue:
      return []
    first_word = queue.pop()
    # first word doesn't match the start node, exit because no point continuing
    if not PatternMatcher.word_matches_pattern(first_word, start_node):
      return []

    # add the first word back in so we can look at the successors
    queue.appendleft(first_word)
    # prep the queue with the first items
    search_queue = deque()
    search_queue.append((start_node,queue,[first_word]))

    saved_paths = []
    # go until the search queue is empty
    while search_queue:
      if verbose: print('>  Search queue loop:')
      # each search_queue item is the graph-node, the current queue of words,
      # and the saved path
      node,wordq,path = search_queue.pop()
      if verbose: print('Popped:',node._pos, [x.pos for x in path])

      if verbose: print('Successors (before end check):', [x._pos for x in graph.successors(node)])
      if len(list(graph.successors(node))) == 0:
        if verbose: print('End of graph')
        # reached a final node, save this path.
        saved_paths.append((path))

      # for every successor, add to the queue
      for i,successor in enumerate(graph.successors(node)):
        queue_copy = copy(wordq)
        word = queue_copy.pop()
        if verbose: print('Successor ->', i, successor._pos)
        # check that the item in the queue matches the starting pattern
        if PatternMatcher.word_matches_pattern(word, successor):
          if verbose: print('Successor MATCH', word.pos, successor._pos)
          # if this word matches the 
          search_queue.append((successor, queue_copy, path + [word]))

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
        results = algorithm.find_all_paths(pattern.graph, entry, queuecopy, verbose)
        if len(results) > 0:
          matches += results
      sentence_queue.pop()
    return matches

