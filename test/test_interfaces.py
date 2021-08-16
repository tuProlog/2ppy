import unittest
from tuprolog.core import *

class TestInterfaces(unittest.TestCase):

    def test_term_visitor(self):
        class MyVisitor(AbstractTermVisitor):
            def defaultValue(self, term):
                return 'a'
        visitor = MyVisitor()
        someTerm = Atom.of('b')
        for term in [Atom.of('a'), Integer.of(1), Var.of("X")]:
            self.assertEqual(term.accept(visitor), 'a')

    def test_term_formatter(self):
        class MyFormatter(AbstractTermFormatter):
            def defaultValue(self, term):
                return str(term)
        formatter = MyFormatter()
        for term in [Atom.of('a'), Integer.of(1), Var.of("X")]:
            self.assertEqual(formatter.format(term), str(term))