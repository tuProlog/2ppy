import unittest
from tuprolog.core import rule, struct, var, fact, atom
from tuprolog.theory import theory
from tuprolog.solve.prolog import prolog_solver


class TestPrologWithResolution(unittest.TestCase):
    def test_abraham_family_tree(self):
        my_program = theory([
            rule(
                struct("ancestor", var("X"), var("Y")),  # :-
                struct("parent", var("X"), var("Y")),
            ),
            rule(
                struct("ancestor", var("X"), var("Y")),  # :-
                struct("parent", var("X"), var("Z")),
                struct("ancestor", var("Z"), var("Y")),
            ),
            fact(struct("parent", atom("abraham"), atom("isaac"))),
            fact(struct("parent", atom("isaac"), atom("jacob"))),
            fact(struct("parent", atom("jacob"), atom("joseph"))),
        ])
        solver = prolog_solver(static_kb=my_program)
        who = var("Who")
        query = struct("ancestor", atom("abraham"), who)
        result = list[str]()
        for solution in solver.solve(query):
            if solution.is_yes:
                result.append(str(solution.substitution[who]))
        self.assertSequenceEqual(result, ["isaac", "jacob", "joseph"])
