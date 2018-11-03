from setuptools import setup

setup(
  name='EXEC_NAME',
  version='1.0',
  py_modules=['MAIN', 'FILE2'],
  install_requires=['Click'],
  entry_points='''
    [console_scripts]
    MAIN=MAIN:cli
  '''
)