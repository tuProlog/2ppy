import random
import string
import unittest

from tuprolog.core import *
from tuprolog.core.operators import DEFAULT_OPERATORS, EMPTY_OPERATORS, STANDARD_OPERATORS, XF, XFY, YF, YFX, FX, FY, \
    XFX, operator, operator_set, OperatorSet, specifier


class TestOperators(unittest.TestCase):

    def setUp(self):
        self.priorities = {random.randint(1, 1200) for _ in range(10)}
        self.specifiers = {XF, YF, FX, FY, XFY, YFX, XFX}
        self.functors = {''.join(random.choices(string.ascii_lowercase, k=1)) for _ in range(10)}
        # Construct two identical operator to check equality
        self.operator1 = operator('a', XF, 1)
        self.operator2 = operator('a', XF, 1)
        # Construct operators using all override constuctors
        self.operators_by_spec = [operator('a', spec, 1) for spec in self.specifiers]
        self.operators_by_spec_logic = [operator(integer(1), const.toTerm(), atom('a')) for const in self.specifiers]
        self.operators_by_spec_struct = [operator(struct('op', integer(1), spec.toTerm(), atom('a')))
                                         for spec in self.specifiers]
        # Costruct default operators set to check their validity
        self.empty_operators_set = EMPTY_OPERATORS
        self.default_operators_set = DEFAULT_OPERATORS
        self.standard_operators_set = STANDARD_OPERATORS
        self.other_operators_sets = {OperatorSet.CONTROL_FLOW, OperatorSet.ARITHMETIC,
                                     OperatorSet.ARITHMETIC_COMPARISON,
                                     OperatorSet.CLAUSES, OperatorSet.TERM_COMPARISON, }
        self.other_operators = {op for op_set in self.other_operators_sets for op in op_set}
        # Define a new set of operators
        self.other_operators_struct = {operator(struct('op', integer(priority), spec.toTerm(), atom(functor)))
                                       for priority in self.priorities
                                       for spec in self.specifiers
                                       for functor in self.functors}
        self.other_operator_set_merged = operator_set(self.other_operators_struct)
        # Construct specifier to test it
        self.specifiers_names = {'XF', 'YF', 'FX', 'FY', 'XFY', 'YFX', 'XFX'}
        self.specifiers = [specifier(name) for name in self.specifiers_names]

    def test_operator_construction(self):
        for operators in [self.operators_by_spec, self.operators_by_spec_logic, self.operators_by_spec_struct]:
            for operator in operators:
                self.assertEqual(operator.getFunctor(), 'a')
                self.assertTrue(operator.getSpecifier() in self.specifiers)
                self.assertEqual(operator.getPriority(), 1)

                self.assertEqual(operator.functor, 'a')
                self.assertTrue(operator.specifier in self.specifiers)
                self.assertEqual(operator.priority, 1)

    def test_operator_equality(self):
        # Check operators are equal if built with same parameters
        self.assertEqual(self.operator1, self.operator2)
        self.assertTrue(self.operator1 == self.operator2)

    def test_operators_set_operations(self):
        operators = [operator(struct('op', integer(1), XF.toTerm(), atom('a'))),
                     operator(struct('op', integer(2), YF.toTerm(), atom('b'))), ]
        # Test addition
        my_appended_operators_set = operator_set(operators[0])
        my_appended_operators_set += operators[1]
        my_scratch_operators_set = operator_set(operators)
        self.assertEqual(my_appended_operators_set, my_scratch_operators_set)
        # Test subtraction
        my_scratch_operators_set = operator_set(operators[0])
        my_subtracted_operators_set = operator_set(operators)
        my_subtracted_operators_set -= operators[1]
        self.assertEqual(my_scratch_operators_set, my_subtracted_operators_set)
        # Test equality
        my_operator_set_1 = operator_set(operators)
        my_operator_set_2 = operator_set(operators)
        self.assertEqual(my_operator_set_1, my_operator_set_2)

    def test_operators_set(self):
        # Check operator set construction works properly
        for operator in self.other_operator_set_merged:
            self.assertTrue(operator in self.other_operators_struct)
            self.assertTrue(operator.functor in self.functors)
            self.assertTrue(operator.specifier in self.specifiers)
            self.assertTrue(operator.priority in self.priorities)

    def test_constant_operators_set(self):
        # Assert empty set is properly empty
        self.assertEqual(len(self.empty_operators_set), 0)
        for operator in self.empty_operators_set:
            self.assertTrue(operator is None)
        # Assert standard and default sets are equal
        self.assertEqual(self.default_operators_set, self.standard_operators_set)
        # Assert standard operators are in set of constantly defined operators
        for operator in self.standard_operators_set:
            self.assertTrue(operator in self.other_operators)

    def test_specifier(self):
        # Test specifier is in constants XF, YF, etc.
        for specifier in self.specifiers:
            self.assertTrue(specifier in self.specifiers)


if __name__ == '__main__':
    unittest.main()
