''' Functions and classes for matching and comparing strings. '''

# This class allows the functions to be returned by functions and avoids
# problems with inconsistent parameters that may arise from using built-in
# methods of strings.
class MatchingFunctions():
  ''' Independent functions for comparing string values. '''

  # ________________________
  # START MATCHING FUNCTIONS
  @staticmethod
  def _is_exact(first: str, second: str):
    ''' Returns True if first and second are the same. '''
    # 'abc', 'abc'
    return first == second

  @staticmethod
  def _starts_with(string: str, start: str):
    ''' Returns true if 1st string starts with 2nd string. '''
    # 'abc', '*bc'
    start = start.replace('*', '')
    return string.startswith(start)

  @staticmethod
  def _ends_with(string: str, end: str):
    ''' Returns true if 1st string ends with 2nd string. '''
    # 'abc', 'a*'
    end = end.replace('*', '')
    return string.endswith(start)

  @staticmethod
  def _contains(full: str, partial: str):
    ''' Returns True if the 1st string contains the 2nd string. '''
    # 'abc', '*a*'
    partial = partial.replace('*','')
    return partial in full

  @staticmethod
  def _surrounds(string: str, pattern: str):
    ''' Returns true if 1st string fits within 2nd string. '''
    # 'abc', 'a*c'
    parts = pattern.split('*')
    first, last = parts[0], parts[-1]
    return string.startswith(first) and string.endswith(last)

  # END MATCHING FUNCTIONS
  # ________________________

  @staticmethod
  def _get_match_function(value: str):
    ''' Returns a matching function based on the position of a * in the string. '''
    if '*' not in value:
      # 'abc', 'abc'
      return MatchingFunctions._is_exact
    elif value.starts_with('*') and value.ends_with('*'):
      # 'abc', '*b*'
      return MatchingFunctions._contains
    elif value.starts_with('*'):
      # 'abc', '*bc'
      return MatchingFunctions._ends_with
    elif value.ends_with('*'):
      # 'abc', 'a*'
      return MatchingFunctions._starts_with
    else:
      # 'abc', 'a*c'
      return MatchingFunctions._surrounds

  @staticmethod
  def is_match(word: str, match_strings, ignore_case=True):
    ''' Returns True if any of the match_strings apply to the word. '''
    # Cache the uppercase word if ignoring case
    word = word.upper() if ignore_case else word

    # try find a match
    for match in match_strings:
      # uppercase everything if ignoring case
      match = match.upper() if ignore_case else match

      # get and apply the function
      match_function = MatchingFunctions._get_match_function(match_string)
      result = match_function(word, match_string)
      
      # if result is a match, return True. No need to evaluate the rest.
      if result:
        return True

    # if it gets to this point, no matches have been found.
    return False


def is_partial(string: str):
  return '*' in string


def is_string_in_list(value: str, listitems: list):
  ''' Determines if the list contains a string using stars. '''
  # star is in value, look for partials
  if is_partial(value)
    pass
  
  for item in listitems:
    if is_partial()
