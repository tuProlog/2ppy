import unittest
from tuprolog.core import Atom, Integer, Var
from tuprolog.core.visitors import AbstractTermVisitor
import jpype.imports
import kotlin.jvm.functions as _functions # type: ignore

import unittest
from tuprolog.core import *
from tuprolog.core.visitors import AbstractTermVisitor


class TestVisitors(unittest.TestCase):

    def test_term_visitor(self):
        class MyVisitor(AbstractTermVisitor):
            def defaultValue(self, term):
                return 'a'
        visitor = MyVisitor()
        for term in [Atom.of('a'), Integer.of(1), Var.of("X")]:
            self.assertEqual(term.accept(visitor), 'a')


if __name__ == '__main__':
    unittest.main()
