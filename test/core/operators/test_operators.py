import random
import string
import unittest

from tuprolog.core import *
from tuprolog.core.operators import DEFAULT_OPERATORS, EMPTY_OPERATORS, STANDARD_OPERATORS, XF, XFY, YF, YFX, FX, FY, \
    XFX, operator, operator_set, OperatorSet, specifier


class TestOperators(unittest.TestCase):

    def setUp(self):
        self.priorities = {random.randint(2, 1199) for _ in range(10)}
        self.specifiers = {XF, YF, FX, FY, XFY, YFX, XFX}
        self.functors = {''.join(random.choices(string.ascii_lowercase, k=1)) for _ in range(10)}
        self.random_operators = {operator(functor, spec, priority)
                                 for priority in self.priorities
                                 for spec in self.specifiers
                                 for functor in self.functors}

    def test_operator_construction(self):
        for priority in self.priorities:
            for spec in self.specifiers:
                for functor in self.functors:
                    op_simple = operator(functor, spec, priority)
                    op_terms = operator(integer(priority), spec.toTerm(), atom(functor))
                    op_struct = operator(struct('op', integer(priority), spec.toTerm(), atom(functor)))

                    for op in {op_simple, op_struct, op_terms}:
                        self.assertEqual(op.getFunctor(), functor)
                        self.assertTrue(op.getSpecifier(), spec)
                        self.assertEqual(op.getPriority(), priority)

                        self.assertEqual(op.functor, functor)
                        self.assertEqual(op.specifier, spec)
                        self.assertEqual(op.priority, priority)

    def test_operator_equality(self):
        for priority in self.priorities:
            for spec in self.specifiers:
                for functor in self.functors:
                    op = operator(functor, spec, priority)
                    op2 = operator(functor, spec, priority)
                    op_terms = operator(integer(priority), spec.toTerm(), atom(functor))
                    op_struct = operator(struct('op', integer(priority), spec.toTerm(), atom(functor)))

                    self.assertTrue(op == op2)
                    self.assertTrue(op == op_terms)
                    self.assertTrue(op == op_struct)

                    different1 = operator(functor + "_", spec, priority)
                    different2 = operator(functor, spec, priority + 1)

                    self.assertTrue(op != different1)
                    self.assertTrue(op != different2)


if __name__ == '__main__':
    unittest.main()
