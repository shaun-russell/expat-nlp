from setuptools import setup

setup(
  name='expat',
  version='1.1.0',
  py_modules=['expat', 'core.parse', 'core.match', 'core.structures', 'core.annotators', 'core.helpers', 'core.search', 'core.main'],
  install_requires=['Click>=7', 'pycorenlp', 'nltk', 'networkx', 'colorama'],
  entry_points='''
    [console_scripts]
    expat=expat:cli
  '''
)