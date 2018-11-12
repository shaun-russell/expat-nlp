from setuptools import setup

setup(
  name='expat',
  version='1.0',
  py_modules=['expat', 'core.parse', 'core.match', 'core.structures', 'core.annotators', 'core.helpers', 'core.search'],
  install_requires=['Click', 'pycorenlp', 'nltk', 'networkx'],
  entry_points='''
    [console_scripts]
    expat=expat:cli
  '''
)