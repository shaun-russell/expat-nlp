''' Tests for the match.py file. '''
import unittest
from core.match import StringMatching, ListMatching
from core.structures import ListAttributes

# STRING MATCHING
# write tests for the following
class TestMatching(unittest.TestCase):
  # 1. Match startswith PASS
  def test_match_starts_pass(self):
    word = 'Apples'
    strings = 'A*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 2. Match startswith FAIL
  def test_match_starts_fail(self):
    word = 'Apples'
    strings = 'Apl*,Apple'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 3. Match endswith PASS
  def test_match_ends_pass(self):
    word = 'Apples'
    strings = '*le,*les'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 4. Match endswith FAIL
  def test_match_ends_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Fruit*'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 5. Match exact PASS
  def test_match_exact_pass(self):
    word = 'Mangoes'
    strings = 'Mangoes'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 6. Match exact FAIL
  def test_match_exact_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Orange Fruit Lemons'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 7. Match contains PASS
  def test_match_contains_pass(self):
    word = 'Orange Fruit Mangoes'
    strings = '*Fruit*,*Mangoe*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 8. Match contains FAIL
  def test_match_contains_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = '*Paper*'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 9. Match surround PASS
  def test_match_surround_pass(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Orange*oes'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 10. Match surround FAIL
  def test_match_surround_fail(self):
    word = 'Orange Fruit Mangoes'
    strings = 'A*Fruit Mangoes'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 11. Match mixed PASS 1
  def test_match_mixed_pass1(self):
    word = 'Oranges'
    strings = 'Fruit*,*papers,*ang*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 12. Match mixed PASS 2
  def test_match_mixed_pass2(self):
    word = 'Orange Fruit Mangoes'
    strings = 'Or*eg,Orange Fruit Mango,*ruit*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 13. Match mixed FAIL 1
  def test_match_mixed_fail1(self):
    word = 'Potatoes'
    strings = 'Potatos*,*topato*,POTATO'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 14. Match mixed FAIL 2
  def test_match_mixed_fail2(self):
    word = 'ABCDEFg'
    strings = 'ABCDEF,*BCDEF'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings))

  # 15. Match no-ignore-case PASS 1
  def test_match_case_pass1(self):
    word = 'ABCdefGEH'
    strings = 'ABCd*'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings))

  # 16. Match no-ignore-case PASS 2
  def test_match_case_pass2(self):
    word = 'AbCdE'
    strings = 'AbCdE'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings), False)

  # 16. Match ignore-case PASS 1
  def test_match_case_pass3(self):
    word = 'AbCdE'
    strings = 'AbCdE'.split(',')
    self.assertEqual(True, StringMatching.is_match(word, strings), True)

  # 18. Match no-ignore-case FAIL 1
  def test_match_case_fail1(self):
    word = 'AbCdE'
    strings = 'aBcde'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings, False))

  # 19. Match no-ignore-case FAIL 2
  def test_match_case_fail2(self):
    word = 'Orange Fruit Mangoes'
    strings = '*fruit*'.split(',')
    self.assertEqual(False, StringMatching.is_match(word, strings, False))


  # ATTRIBUTE LIST MATCHING
  def test_attr_list_pass1(self):
    value = 'DEF'
    attributes = ListAttributes('ABC,DEF', 'GHI', 1)
    self.assertEqual(True, ListMatching.is_match(value, attributes))

  def test_attr_list_pass2(self):
    value = 'FHI'
    attributes = ListAttributes('*', 'G*', 1)
    self.assertEqual(True, ListMatching.is_match(value, attributes))

  def test_attr_list_pass3(self):
    value = 'AVG'
    attributes = ListAttributes('A*,*G', 'GHI', 2)
    self.assertEqual(True, ListMatching.is_match(value, attributes))

  def test_attr_list_pass4(self):
    # matches the 2 required
    value = 'PNG,JPG,TIFF'
    attributes = ListAttributes('*G*', '', 1)
    self.assertEqual(True, ListMatching.is_match(value, attributes, required=2))

  def test_attr_list_pass5(self):
    # no restrictions on matching
    value = '123'
    attributes = ListAttributes('', '', 1)
    self.assertEqual(True, ListMatching.is_match(value, attributes))

  def test_attr_list_fail1(self):
    # exact match exclusion
    value = 'GHI'
    attributes = ListAttributes('ABC,DEF', 'GHI', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail2(self):
    # check an exclusion inside
    value = '1234 HI5'
    attributes = ListAttributes('ABC,DEF', '*HI*', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail3(self):
    # check that exclusions take precedence over matches
    value = 'AVG'
    attributes = ListAttributes('A*,*F', '*G', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail4(self):
    # check matching * but having a matching exclusion
    value = 'GBG'
    attributes = ListAttributes('*', 'G*', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail5(self):
    # check list of exclusions
    value = 'GBG'
    attributes = ListAttributes('*', 'A*,B*,G*', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail6(self):
    # doesn't match the 3 required
    value = 'PNG,JPG,TIFF'
    attributes = ListAttributes('*G*', '', 3)
    self.assertEqual(False, ListMatching.is_match(value, attributes))

  def test_attr_list_fail7(self):
    # matches the 2 required
    value = 'PNG,JPG,TIFF'
    attributes = ListAttributes('*G*', '', 1)
    self.assertEqual(False, ListMatching.is_match(value, attributes, required=3))

