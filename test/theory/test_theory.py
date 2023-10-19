import unittest
from tuprolog.core import clause, var, struct, atom
from tuprolog.theory import theory


class TestTheory(unittest.TestCase):
    def test_empty_theory(self):
        t = theory()
        self.assertIsNotNone(t)
        self.assertEqual(0, len(t))
        self.assertTrue(t.is_empty)

    def test_retract(self):
        A = var('A')
        a = atom('a')

        def f(arg):
            return struct('f', arg)

        def g(arg):
            return struct('g', arg)

        t = theory([
            c1 := clause(f(A), g(A)),
            clause(g(a)),
        ])
        self.assertEqual(2, len(t))
        result = t.retract(c1)
        self.assertEqual(1, len(result.theory))

    def test_unificator(self):
        A = var('A')
        a = atom('a')

        def f(arg):
            return struct('f', arg)

        def g(arg):
            return struct('g', arg)

        t = theory([
            clause(g(a)),
        ])
        results = list(t[f(a)])
        self.assertEqual(0, len(results))

        t = theory([
            clause(f(A), g(A)),
            clause(g(a)),
        ])
        results = list(t[f(a)])
        self.assertEqual(1, len(results))
