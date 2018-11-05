''' Helper functions. '''

def get_value(label, source, default):
  if label in source:
    return source[label]
  else:
    return default