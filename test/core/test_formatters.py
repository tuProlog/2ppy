import unittest
from tuprolog.core import *
from tuprolog.core.formatters import AbstractTermFormatter


class TestFormatters(unittest.TestCase):

    def test_term_formatter(self):
        class MyFormatter(AbstractTermFormatter):
            def defaultValue(self, term):
                return str(term)
        formatter = MyFormatter()
        for term in [Atom.of('a'), Integer.of(1), Var.of("X")]:
            self.assertEqual(formatter.format(term), str(term))


if __name__ == '__main__':
    unittest.main()
