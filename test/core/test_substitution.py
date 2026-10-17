import unittest
from tuprolog.core import substitution, struct, atom, scope


class TestSubstitution(unittest.TestCase):

    def test_substitution_creation(self):
        sub = substitution({})
        self.assertEqual(0, len(sub))
        self.assertEqual(True, sub.isSuccess())
        self.assertEqual(True, sub.is_success)

    def test_substitution_application(self):
        sc = scope("X", "Y")
        term = struct("father", sc["X"], sc["Y"])
        sub1 = substitution({sc["X"]: atom("abraham")})
        sub2 = substitution({sc["Y"]: atom("isaac")})

        sub = sub1 + sub2

        result = sub.apply_to(term)
        self.assertEqual("father(abraham, isaac)", result.to_string())
