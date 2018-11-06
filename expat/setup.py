from setuptools import setup

setup(
  name='expat-nlp',
  version='1.0',
  py_modules=['main', 'parse', 'match', 'structures', 'annotators', 'helpers'],
  install_requires=['Click', 'pycorenlp', 'nltk'],
  entry_points='''
    [console_scripts]
    main=main:cli
  '''
)