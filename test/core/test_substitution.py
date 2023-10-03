import unittest
from tuprolog.core import substitution, var, struct, FAIL


class TestSubstitution(unittest.TestCase):
    
    def test_substitution_creation(self):
        sub = substitution({})
        self.assertEqual(0, len(sub))
        self.assertEqual(True, sub.isSuccess())
        self.assertEqual(True, sub.is_success)
