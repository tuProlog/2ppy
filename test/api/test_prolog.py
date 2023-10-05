import unittest
from tuprolog.core import rule, struct, var, fact, atom
from tuprolog.solve import *

class TestPrologWithResolution(unittest.TestCase):
    def test_abraham_family_tree(self):
        program = [
            rule(
                struct("ancestor", var("X"), var("Y")), # :-
                    struct("parent", var("X"), var("Y"))
            ),
            rule(
                struct("ancestor", var("X"), var("Y")), # :-
                    struct("parent", var("X"), var("Z")),
                    struct("ancestor", var("Z"), var("Y"))
            ),
            fact(struct("parent", atom("abraham"), atom("isaac"))),
            fact(struct("parent", atom("isaac"), atom("jacob"))),
            fact(struct("parent", atom("jacob"), atom("joseph"))),
        ]
        # TODO: solve
