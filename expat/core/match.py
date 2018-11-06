''' Functions and classes for matching and comparing strings. '''

from core.structures import ListAttributes

# This class allows the functions to be returned by functions and avoids
# problems with inconsistent parameters that may arise from using built-in
# methods of strings.


class StringMatching():
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
        return string.endswith(end)

    @staticmethod
    def _contains(full: str, partial: str):
        ''' Returns True if the 1st string contains the 2nd string. '''
        # 'abc', '*a*'
        partial = partial.replace('*', '')
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
            return StringMatching._is_exact
        elif value.startswith('*') and value.endswith('*'):
            # 'abc', '*b*'
            return StringMatching._contains
        elif value.startswith('*'):
            # 'abc', '*bc'
            return StringMatching._ends_with
        elif value.endswith('*'):
            # 'abc', 'a*'
            return StringMatching._starts_with
        else:
            # 'abc', 'a*c'
            return StringMatching._surrounds

    @staticmethod
    def is_match(word: str, match_strings: list, ignore_case=True, required=1):
        ''' Returns True if any of the match_strings apply to the word. '''
        # Cache the uppercase word if ignoring case
        word = word.upper() if ignore_case else word

        match_count = 0
        # try find a match
        for match in match_strings:
            # uppercase everything if ignoring case
            match = match.upper() if ignore_case else match

            # get and apply the function
            match_function = StringMatching._get_match_function(match)
            result = match_function(word, match)

            # Return True if there is the correct number of matches
            if result:
                match_count += 1
                if match_count >= required:
                    return True

        # if it gets to this point, no matches have been found.
        return False


class ListMatching():
    @staticmethod
    def is_match(values: str, attributes: ListAttributes, required=1):
        # Match the required number of values using the requirements in the
        # provided ListAttributes object
        match_count = 0
        for value in values.split(','):
            # first check that the value has the required attributes
            matches = True
            if attributes.has_match_requirements:
                matches = StringMatching.is_match(value, attributes.to_find,
                                                required=attributes.required_num)
            # False if it failed this check
            if not matches:
                continue
            
            # now check that it doesn't have the excluded
            if attributes.has_exclusions:
                matches = not StringMatching.is_match(value, attributes.to_exclude)

            # If the value we're checking has an excluded value, then rather than
            # skip it (like we would for a non-match), this disqualifies all values.
            if not matches:
                return False

            # didn't fail any of the checks, therefore it passes
            match_count += 1

        # Only return True if enough matches were found.
        if match_count >= required:
            return True
        else:
            return False


class PatternMatcher():
    ''' The main class that finds pattern matches in annotated sentences.'''
    @staticmethod
    def get_pattern_matches(sentence_tokens):
        # TODO this.
        pass