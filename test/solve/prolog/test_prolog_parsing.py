import unittest
from tuprolog.core import struct, atom, integer
from tuprolog.theory.parsing import parse_theory
from tuprolog.solve.prolog import prolog_solver
from tuprolog.solve.flags import DEFAULT_FLAG_STORE, LastCallOptimization, FlagStore
from tuprolog.solve.channel import output_channel


class TestPrologWithParsingAndResolution(unittest.TestCase):
    def setUp(self) -> None:
        self.theory_text = """
        % Towers of Hanoi
        move(1,X,Y,_) :-  
            write('Move top disk from '), 
            write(X), 
            write(' to '), 
            write(Y), 
            nl. 
        move(N,X,Y,Z) :- 
            N>1, 
            M is N-1, 
            move(M,X,Z,Y), 
            move(1,X,Y,_), 
            move(M,Z,Y,X).
        """
        self.prints: list[str] = []
        self.maxDiff = None

    def print(self, message):
        self.prints.append(message)

    def print_output(self, message):
        message = str(message)
        if len(self.prints) == 0:
            self.prints.append(message)
        elif self.prints[-1].endswith('\n'):
            self.prints.append(message)
        else:
            self.prints[-1] += message
    @unittest.skip("TODO: fix this test")
    def test_prolog(self):
        logic_theory = parse_theory(self.theory_text)
        flags = DEFAULT_FLAG_STORE.set(LastCallOptimization, LastCallOptimization.OFF)
        solver = prolog_solver(
            static_kb=logic_theory,
            flags=flags,
            std_out=output_channel(self.print_output))
        query = struct("move", integer(3), atom("left"), atom("right"), atom("center"))
        for solution in solver.solve(query):
            if solution.is_yes:
                self.print(f"yes: {solution.solved_query}")

        self.assertEqual(
            self.prints,
            [
                'Move top disk from left to right\n',
                'Move top disk from left to center\n',
                'Move top disk from right to center\n',
                'Move top disk from left to right\n',
                'Move top disk from center to left\n',
                'Move top disk from center to right\n',
                'Move top disk from left to right\n',
                'yes: move(3, left, right, center)'
            ]
        )