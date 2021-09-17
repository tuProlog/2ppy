from tuprolog.core.operators import EMPTY_OPERATORS
import unittest
from tuprolog import *
from tuprolog.core import *

class TestOperators(unittest.TestCase):

    def setUp(self):
        self._empty_operator = EMPTY_OPERATORS

    def test_operator(self):
        self.assertEqual(self._empty_operator, None)
 


if __name__ == '__main__':
    unittest.main()
