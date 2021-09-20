import random
import string
import unittest

from tuprolog.core import *
from tuprolog.core.operators import DEFAULT_OPERATORS, EMPTY_OPERATORS, STANDARD_OPERATORS, XF, XFY, YF, YFX, FX, FY, \
    XFX, operator, operator_set, OperatorSet, specifier

# noinspection PyUnresolvedReferences
from java.lang import IllegalArgumentException


class AbstractTestOperatorStuff(unittest.TestCase):

    def setUp(self):
        # Setup shared parameters
        self.priorities = {random.randint(2, 1199) for _ in range(10)}
        self.specifiers = {XF, YF, FX, FY, XFY, YFX, XFX}
        self.functors = {''.join(random.choices(string.ascii_lowercase, k=1)) for _ in range(10)}
        # Setup random operators
        self.random_operators = {operator(functor, spec, priority)
                                 for priority in self.priorities
                                 for spec in self.specifiers
                                 for functor in self.functors}


class TestOperators(AbstractTestOperatorStuff):

    def test_operator_construction(self):
        # Iterate over each priority, specification and functor...
        for priority in self.priorities:
            for spec in self.specifiers:
                for functor in self.functors:
                    # ... build the corresponding operator using three possible contructors...
                    op_simple = operator(functor, spec, priority)
                    op_terms = operator(integer(priority), spec.toTerm(), atom(functor))
                    op_struct = operator(struct('op', integer(priority), spec.toTerm(), atom(functor)))
                    # ... check each constructor works properly...
                    for op in {op_simple, op_struct, op_terms}:
                        self.assertEqual(op.getFunctor(), functor)
                        self.assertTrue(op.getSpecifier(), spec)
                        self.assertEqual(op.getPriority(), priority)
                        # ... using pythonic way, too.
                        self.assertEqual(op.functor, functor)
                        self.assertEqual(op.specifier, spec)
                        self.assertEqual(op.priority, priority)

    def test_operator_equality(self):
        # Iterate over each priority, specification and functor...
        for priority in self.priorities:
            for spec in self.specifiers:
                for functor in self.functors:
                    # ... build the corresponding operator using three possible contructors...
                    op = operator(functor, spec, priority)
                    op2 = operator(functor, spec, priority)
                    op_terms = operator(integer(priority), spec.toTerm(), atom(functor))
                    op_struct = operator(struct('op', integer(priority), spec.toTerm(), atom(functor)))
                    # ... check different constructors build equal objects...
                    self.assertTrue(op == op2)
                    self.assertTrue(op == op_terms)
                    self.assertTrue(op == op_struct)
                    # ... check different sepcifications build different objects...
                    different1 = operator(functor + "_", spec, priority)
                    different2 = operator(functor, spec, priority + 1)
                    self.assertTrue(op != different1)
                    self.assertTrue(op != different2)


class TestSpecifiers(AbstractTestOperatorStuff):

    def setUp(self):
        # Setup shared parameters
        self.actual_specifiers = {XF, YF, FX, FY, XFY, YFX, XFX}
        specifiers_names = {'Xf', 'yF', 'fX', 'fY', 'xFy', 'YfX', 'xFx'}
        self.specifiers_names = {x for name in specifiers_names for x in (name.lower(), name.upper())}
        # Build all possible specifiers
        self.specifiers = {specifier(name) for name in self.specifiers_names}

    def test_specifier_parsing(self):
        # Test specifier is in constants XF, YF, etc.
        for spec in self.specifiers:
            self.assertTrue(spec in self.actual_specifiers)
        self.assertEqual(self.specifiers, self.actual_specifiers)

    def test_specifier_from_terms(self):
        # For each specifier name build corresponding specifier from atom
        for name in self.specifiers_names:
            self.assertTrue(specifier(atom(name)) in self.actual_specifiers)
            # Assert specifier raises IllegalArgumentException when wrong name is passed
            with self.assertRaises(IllegalArgumentException):
                wrong_name = name + 'g'
                specifier(atom(wrong_name))

    def test_specifier_names(self):
        # For each possible names for specifiers check that names are ok
        for name in self.specifiers_names:
            spec = specifier(name)
            enum_name = name.upper()
            logic_name = name.lower()
            self.assertEqual(spec.name(), enum_name)
            self.assertEqual(spec.toTerm(), atom(logic_name))
            self.assertEqual(spec.isPrefix(), len(logic_name) == 2 and logic_name[0] == 'f')
            self.assertEqual(spec.isPostfix(), len(logic_name) == 2 and logic_name[-1] == 'f')
            self.assertEqual(spec.isInfix(), len(logic_name) == 3 and logic_name[1] == 'f')


class TestOperatorSets(AbstractTestOperatorStuff):

    def setUp(self):
        # Extend shared setup function
        super().setUp()
        # Define builtin operators, builtin operators sets and some random operators
        self.builtin_operator_sets = {EMPTY_OPERATORS, DEFAULT_OPERATORS, STANDARD_OPERATORS,
                                      OperatorSet.CONTROL_FLOW, OperatorSet.ARITHMETIC,
                                      OperatorSet.ARITHMETIC_COMPARISON,
                                      OperatorSet.CLAUSES, OperatorSet.TERM_COMPARISON}
        self.all_builtin_operators = {op for op_set in self.builtin_operator_sets for op in op_set}
        self.builtin_operators_set = operator_set(self.all_builtin_operators)
        self.random_operators_set = operator_set(self.random_operators)
        self.some_operators = [operator('a', XF, 1), operator('b', YF, 2)]

    def test_operator_set_creation(self):
        # Check that EMPTY_OPERATORS is properly empty
        empty = operator_set()
        self.assertEqual(empty, EMPTY_OPERATORS)
        # For each operator in the set of random operators check singleton contruction
        for op in self.random_operators:
            singleton = operator_set(op)
            self.assertEqual(len(singleton), 1)
            self.assertTrue(op in singleton)
        # Check construction from vararg
        from_vararg = operator_set(*self.random_operators)
        self.assertEqual(from_vararg, self.random_operators_set)

    def test_operators_set_sum(self):
        # Check appension of operator to existing operators_set
        my_appended_operators_set = operator_set(self.some_operators[0])
        my_appended_operators_set += self.some_operators[1]
        my_scratch_operators_set = operator_set(self.some_operators)
        self.assertEqual(my_appended_operators_set, my_scratch_operators_set)

    def test_operators_set_sub(self):
        # Check removal of operator from existing operators_set
        my_scratch_operators_set = operator_set(self.some_operators[0])
        my_subtracted_operators_set = operator_set(self.some_operators)
        my_subtracted_operators_set -= self.some_operators[1]
        self.assertEqual(my_scratch_operators_set, my_subtracted_operators_set)

    def test_operators_set_eq(self):
        # Test equality between operators sets
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
