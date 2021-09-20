import unittest

from tuprolog.core import *
from tuprolog.core.operators import DEFAULT_OPERATORS, EMPTY_OPERATORS, STANDARD_OPERATORS, XF, XFY, YF, YFX, FX, FY, \
    XFX, operator, operator_set, OperatorSet, specifier

# noinspection PyUnresolvedReferences
from java.lang import IllegalArgumentException


class TestSpecifiers(unittest.TestCase):

    def setUp(self):
        self.actual_specifiers = {XF, YF, FX, FY, XFY, YFX, XFX}
        specifiers_names = {'Xf', 'yF', 'fX', 'fY', 'xFy', 'YfX', 'xFx'}
        self.specifiers_names = {x for name in specifiers_names for x in (name.lower(), name.upper())}
        self.specifiers = {specifier(name) for name in self.specifiers_names}

    def test_specifier_parsing(self):
        # Test specifier is in constants XF, YF, etc.
        for spec in self.specifiers:
            self.assertTrue(spec in self.actual_specifiers)
        self.assertEqual(self.specifiers, self.actual_specifiers)

    def test_specifier_from_terms(self):
        for name in self.specifiers_names:
            self.assertTrue(specifier(atom(name)) in self.actual_specifiers)
            with self.assertRaises(IllegalArgumentException):
                wrong_name = name + 'g'
                specifier(atom(wrong_name))

    def test_specifier_names(self):
        for name in self.specifiers_names:
            spec = specifier(name)
            enum_name = name.upper()
            logic_name = name.lower()
            self.assertEqual(spec.name(), enum_name)
            self.assertEqual(spec.toTerm(), atom(logic_name))
            self.assertEqual(spec.isPrefix(), len(logic_name) == 2 and logic_name[0] == 'f')
            self.assertEqual(spec.isPostfix(), len(logic_name) == 2 and logic_name[-1] == 'f')
            self.assertEqual(spec.isInfix(), len(logic_name) == 3 and logic_name[1] == 'f')


if __name__ == '__main__':
    unittest.main()
