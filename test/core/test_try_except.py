import unittest
from tuprolog.core.exception import *
from tuprolog.core import Substitution, Atom


class TestExceptions(unittest.TestCase):

    def test_TuprologException(self):
        try:
            raise TuPrologException("test")
        except TuPrologException as e:
            self.assertEqual("test", e.message)
    
    def test_SubstitutionException(self):
        sub = Substitution.empty()
        try:
            raise SubstitutionException(sub, "test")
        except SubstitutionException as e:
            self.assertEqual("test", e.message)
            self.assertEqual(sub, e.substitution)

    def test_SubstitutionApplicationException(self):
        term = Atom.of("test")
        sub = Substitution.empty()
        try:
            raise SubstitutionApplicationException(term, sub, "test")
        except SubstitutionApplicationException as e:
            self.assertEqual("test", e.message)
            self.assertEqual(sub, e.substitution)
            self.assertEqual(term, e.term)


if __name__ == '__main__':
    unittest.main()
