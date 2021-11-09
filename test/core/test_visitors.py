import unittest
from tuprolog.core import *
from tuprolog.core.visitors import AbstractTermVisitor


class TestVisitors(unittest.TestCase):

    def test_term_visitor(self):
        class MyVisitor(AbstractTermVisitor):
            def defaultValue(self, term):
                return 'a'
        visitor = MyVisitor()
        someTerm = Atom.of('b')
        for term in [Atom.of('a'), Integer.of(1), Var.of("X")]:
            self.assertEqual(term.accept(visitor), 'a')


if __name__ == '__main__':
    unittest.main()
