import random
import string
import unittest

from tuprolog.core import *
from tuprolog.core.operators import DEFAULT_OPERATORS, EMPTY_OPERATORS, STANDARD_OPERATORS, XF, XFY, YF, YFX, FX, FY, \
    XFX, operator, operator_set, OperatorSet, specifier


class TestOperatorSets(unittest.TestCase):

    def setUp(self):
        self.priorities = {random.randint(1, 1200) for _ in range(10)}
        self.specifiers = {XF, YF, FX, FY, XFY, YFX, XFX}
        self.functors = {''.join(random.choices(string.ascii_lowercase, k=1)) for _ in range(10)}
        self.builtin_operator_sets = {EMPTY_OPERATORS, DEFAULT_OPERATORS, STANDARD_OPERATORS,
                                      OperatorSet.CONTROL_FLOW, OperatorSet.ARITHMETIC,
                                      OperatorSet.ARITHMETIC_COMPARISON,
                                      OperatorSet.CLAUSES, OperatorSet.TERM_COMPARISON}
        self.all_builtin_operators = {op for op_set in self.builtin_operator_sets for op in op_set}
        self.builtin_operators_set = operator_set(self.all_builtin_operators)
        self.random_operators = {operator(functor, spec, priority)
                                 for priority in self.priorities
                                 for spec in self.specifiers
                                 for functor in self.functors}
        self.random_operators_set = operator_set(self.random_operators)
        self.some_operators = [operator('a', XF, 1), operator('b', YF, 2)]

    def test_operator_set_creation(self):
        empty = operator_set()
        self.assertEqual(empty, EMPTY_OPERATORS)
        for op in self.random_operators:
            singleton = operator_set(op)
            self.assertEqual(len(singleton), 1)
            self.assertTrue(op in singleton)
        from_vararg = operator_set(*self.random_operators)
        self.assertEqual(from_vararg, self.random_operators_set)

    def test_operators_set_sum(self):
        my_appended_operators_set = operator_set(self.some_operators[0])
        my_appended_operators_set += self.some_operators[1]
        my_scratch_operators_set = operator_set(self.some_operators)
        self.assertEqual(my_appended_operators_set, my_scratch_operators_set)

    def test_operators_set_sub(self):
        my_scratch_operators_set = operator_set(self.some_operators[0])
        my_subtracted_operators_set = operator_set(self.some_operators)
        my_subtracted_operators_set -= self.some_operators[1]
        self.assertEqual(my_scratch_operators_set, my_subtracted_operators_set)

    def test_operators_set_eq(self):
        my_operator_set_1 = operator_set(self.some_operators)
        my_operator_set_2 = operator_set(self.some_operators)
        self.assertEqual(my_operator_set_1, my_operator_set_2)

    def test_constant_operators_set(self):
        # Assert empty set is properly empty
        self.assertEqual(len(EMPTY_OPERATORS), 0)
        # Assert standard and default sets are equal
        self.assertEqual(DEFAULT_OPERATORS, STANDARD_OPERATORS)
        # Assert standard operators are in set of builtin operators
        for op in STANDARD_OPERATORS:
            self.assertTrue(op in self.all_builtin_operators)


if __name__ == '__main__':
    unittest.main()
