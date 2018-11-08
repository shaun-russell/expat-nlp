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
  def find_all_paths(graph, start_node, queue):
    ''' Provide a graph reference, the starting node, and the search queue. '''
    saved_paths = []
    # prep the queue with the first items
    search_queue = deque()
    search_queue.append((start_node,queue,[]))

    # go until the search queue is empty
    while search_queue:
      print('>  Search queue loop:')
      # each search_queue item is the graph-node, the current queue of words,
      # and the saved path
      node,wordq,path = search_queue.pop()
      print('Popped:',node._pos, [x.pos for x in path])

      print('Successors (before end check):', [x._pos for x in graph.successors(node)])
      if len(list(graph.successors(node))) == 0:
        print('End of graph')
        # reached a final node, save this path.
        saved_paths.append((path))

      # for every successor, add to the queue
      for i,successor in enumerate(graph.successors(node)):
        queue_copy = copy(wordq)
        word = queue_copy.pop()
        print('Successor ->', i, successor._pos)
        # check that the item in the queue matches the starting pattern
        if PatternMatcher.word_matches_pattern(word, successor):
          print('Successor MATCH', word.pos, successor._pos)
          # if this word matches the 
          search_queue.append((successor, queue_copy, path + [word]))

    return saved_paths


class MatchBuilder():
  @staticmethod
  def find_all_matches(annotated_sentence, pattern, algorithm):
    sentence_queue = annotated_sentence.get_queue()
    matches = []
    # for every word in the sentence...
    while sentence_queue:
      print('Sentence Q loop')
      # get the word that starts the queue
      word = sentence_queue.pop()
      print(word.word, word.pos)
      # make a copy because we can have queues
      queuecopy = copy(sentence_queue)
      # see if the word matches any of the entry points for the pattern
      for entry in pattern.graph_entry_points:
        print('Test entry: {}={}, {}={}'.format(word.word, entry.word, word.pos, entry._pos))
        if PatternMatcher.word_matches_pattern(word, entry):
          print('MATCH: ', entry.word, entry._pos)
          # if it meets the entry requirements, find all the pattern matches
          results = algorithm.find_all_paths(pattern.graph, entry, queuecopy)
          # save the matches, if there are any
          if len(results) > 0:
            matches += results
    
    return matches

