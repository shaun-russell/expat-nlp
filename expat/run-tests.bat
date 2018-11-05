cls
echo Running tests.
python -m unittest tests/test_match.py
python -m unittest tests/test_parse.py
python -m unittest tests/test_annotate.py