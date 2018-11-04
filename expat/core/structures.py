''' Common structures to pass data around. '''


class ListAttributes():
  def __init__(self, to_find, to_exclude, required_num):

    # easy to understand bool value. This could be put in a function, but it
    # works just fine here for now
    self.has_match_requirements = to_find != '*' and to_find != ''
    self.to_find = to_find.split(',')

    self.required_num = required_num

    # if nothing specified, nothing to exclude
    self.to_exclude = to_exclude.split(',')
    self.has_exclusions = to_exclude != ''
