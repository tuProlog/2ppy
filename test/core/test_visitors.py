import unittest
from tuprolog.core import *
from tuprolog.core.visitors import DefaultTermVisitor
import jpype.imports
import kotlin.jvm.functions as _functions

@jpype.JImplements(_functions.Function1)
class Lambda:
    def __init__(self, f):
        self.f = f

    @jpype.JOverride
    def invoke(self, arg):
        return self.f(arg)


class TestVisitors(unittest.TestCase):

    def test_term_visitor(self):
        visitor = DefaultTermVisitor.of(Lambda(lambda term: 'a'))
        for term in [Atom.of('a'), Integer.of(1), Var.of("X")]:
            self.assertEqual(term.accept(visitor), 'a')


if __name__ == '__main__':
    unittest.main()
