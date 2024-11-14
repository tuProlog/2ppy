import unittest
from tuprolog.core import struct, var
from tuprolog.theory.parsing import parse_theory
from tuprolog.solve.plp import solve_options, probability
from tuprolog.solve.problog import problog_solver
from tuprolog.solve.problog.operators import PROBLOG_OPERATORS


class ExemplifyProblog(unittest.TestCase):

    def setUp(self) -> None:
        self.probabilisticTheoryText = """
        0.6::edge(1,2).
        0.1::edge(1,3).
        0.4::edge(2,5).
        0.3::edge(2,6).
        0.3::edge(3,4).
        0.8::edge(4,5).
        0.2::edge(5,6).
        
        path(X,Y) :- edge(X,Y).
        path(X,Y) :- edge(X,Z),Y \\== Z,path(Z,Y).
        """
        self.prints = []

    def print(self, message):
        self.prints.append(message)

    def test_problog(self):
        probabilisticTheory = parse_theory(self.probabilisticTheoryText, PROBLOG_OPERATORS)
        probabilisticSolver = problog_solver(static_kb=probabilisticTheory)
        query = struct('path', var('From'), var('To'))
        for solution in probabilisticSolver.solve(query, solve_options(lazy=True, probabilistic=True)):
            if solution.is_yes:
                self.print(f"yes: {solution.solved_query} with probability {probability(solution)}")

        self.assertEquals(
            self.prints,
            [
                'yes: path(1, 2) with probability 0.6',
                'yes: path(1, 3) with probability 0.1',
                'yes: path(2, 5) with probability 0.4',
                'yes: path(2, 6) with probability 0.356',
                'yes: path(3, 4) with probability 0.3',
                'yes: path(4, 5) with probability 0.8',
                'yes: path(5, 6) with probability 0.2',
                'yes: path(1, 5) with probability 0.25824',
                'yes: path(1, 6) with probability 0.2167296',
                'yes: path(1, 4) with probability 0.03',
                'yes: path(3, 5) with probability 0.24',
                'yes: path(3, 6) with probability 0.04800000000000001',
                'yes: path(4, 6) with probability 0.16000000000000003'
            ]
        )


if __name__ == '__main__':
    pass
    # unittest.main()
