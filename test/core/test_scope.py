import unittest
from tuprolog.core import scope, var, Scope, variables, struct


class TestScope(unittest.TestCase):

    def test_empty_scope_creation(self):
        empty_scope = scope()
        self.assertIsNotNone(empty_scope)
        self.assertIsInstance(empty_scope, Scope)
        self.assertEqual(0, len(empty_scope.variables))

    def test_scope_creation(self):
        full_scope = scope('A', var('B'))
        self.assertIsNotNone(full_scope)
        self.assertIsInstance(full_scope, Scope)
        self.assertEqual(2, len(full_scope.variables))
        for v in full_scope.variables:
            self.assertIn(v, {'A', 'B'})

    def test_variables_reuse(self):
        A, B = variables('A', 'B')
        s = scope(A, B)
        self.assertEqual(A, s['A'])
        self.assertEqual(B, s['B'])
        fAB = s.struct('f', s.var('A'), s.var('B'))
        self.assertEqual(struct('f', A, B), fAB)


if __name__ == '__main__':
    unittest.main()
