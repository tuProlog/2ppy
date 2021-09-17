from tuprolog.core.operators import EMPTY_OPERATORS, XF, XFY, YF, YFX, FX, FY, XFX, operator, specifier, Specifier
import unittest
from tuprolog import *
from tuprolog.core import *

class TestOperators(unittest.TestCase):

    def setUp(self):
        self.constants = {XF, YF, FX, FY, XFY, YFX, XFX}
        self.my_operator = [operator('a', const, 1) for const in self.constants]
        self.operator1 = operator('a', XF, 1)
        self.operator2 = operator('a', XF, 1)
        self.my_operator_logic = [operator(integer(1), const.toTerm(), atom('a')) for const in self.constants]
        self.my_operator_struct = [operator(struct('op', integer(1), const.toTerm(), atom('a'))) for const in self.constants]

    def test_operator_construction(self):
        for operators in [self.my_operator, self.my_operator_logic, self.my_operator_struct]:
            for operator in operators:
                self.assertEqual(operator.getFunctor(), 'a')
                self.assertTrue(operator.getSpecifier() in self.constants)
                self.assertEqual(operator.getPriority(), 1)
                self.assertEqual(operator.functor, 'a')
                self.assertTrue(operator.specifier in self.constants)
                self.assertEqual(operator.priority, 1)

    def test_operator_equality(self):    
        self.assertEqual(self.operator1, self.operator2)
        self.assertTrue(self.operator1 == self.operator2)

 


if __name__ == '__main__':
    unittest.main()
