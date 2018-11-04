''' Tests for the match.py file. '''
import unittest
from core.match import Matching

# write tests for the following
class TestMatching(unittest.TestCase):
  # 1. Match startswith PASS
  def test_match_starts_pass(self):
    word = 'Apples'
    strings = 'A*'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings))

  # 2. Match startswith FAIL
  def test_match_starts_fail(self):
    word = 'Apples'
    strings = 'Apl*,Apple'.split(',')
    self.assertEqual(False, Matching.is_match(word, strings))

  # 3. Match endswith PASS
  def test_match_ends_pass(self):
    word = 'Apples'
    strings = '*le,*les'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings))

  # 4. Match endswith FAIL
  def test_match_ends_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Fruit*'.split(',')
    self.assertEqual(False, Matching.is_match(word, strings))

  # 5. Match exact PASS
  def test_match_exact_pass(self):
    word = 'Mangoes'
    strings = 'Mangoes'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings))

  # 6. Match exact FAIL
  def test_match_exact_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Orange Fruit Lemons'.split(',')
    self.assertEqual(False, Matching.is_match(word, strings))

  # 7. Match contains PASS
  def test_match_contains_pass(self):
    word = 'Orange Fruit Mangoes'
    strings = '*Fruit*,*Mangoe*'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings))

  # 8. Match contains FAIL
  def test_match_contains_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = '*Paper*'.split(',')
    self.assertEqual(False, Matching.is_match(word, strings))

  # 9. Match surround PASS
  def test_match_surround_pass(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Orange*oes'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings))

  # 10. Match surround FAIL
  def test_match_surround_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = 'A*Fruit Mangoes'.split(',')
    self.assertEqual(False, Matching.is_match(word, strings))

  # 11. Match mixed PASS 1
  def test_match_mixed_pass1(self):
    word = 'Oranges'
    strings = 'Fruit*,*papers,*ang*'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings))

  # 12. Match mixed PASS 2
  def test_match_mixed_pass2(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Or*eg,Orange Fruit Mango,*ruit*'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings))

  # 13. Match mixed FAIL 1
  def test_match_mixed_fail1(self):
    word = 'Potatoes'
    strings = 'Potatos*,*topato*,POTATO'.split(',')
    self.assertEqual(False, Matching.is_match(word, strings))

  # 14. Match mixed FAIL 2
  def test_match_mixed_fail2(self):
    word = 'ABCDEFg'
    strings = 'ABCDEF,*BCDEF'.split(',')
    self.assertEqual(False, Matching.is_match(word, strings))

  # 15. Match no-ignore-case PASS 1
  def test_match_case_pass1(self):
    word = 'ABCdefGEH'
    strings = 'ABCd*'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings))

  # 16. Match no-ignore-case PASS 2
  def test_match_case_pass2(self):
    word = 'AbCdE'
    strings = 'AbCdE'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings), False)

  # 16. Match ignore-case PASS 1
  def test_match_case_pass3(self):
    word = 'AbCdE'
    strings = 'AbCdE'.split(',')
    self.assertEqual(True, Matching.is_match(word, strings), True)

  # 18. Match no-ignore-case FAIL 1
  def test_match_case_fail1(self):
    word = 'AbCdE'
    strings = 'aBcde'.split(',')
    self.assertEqual(False, Matching.is_match(word, strings, False))

  # 19. Match no-ignore-case FAIL 2
  def test_match_case_fail2(self):
    word = 'Orange Fruit Mangoes'
    strings = '*fruit*'.split(',')
    self.assertEqual(False, Matching.is_match(word, strings, False))
