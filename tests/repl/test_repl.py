import io
import unittest

from tuprolog.repl._definitions import PrologREPL
from tuprolog.solve.prolog import prolog_solver
from tuprolog.theory.parsing import parse_theory


class BoundedInput(io.StringIO):
    """Fails instead of looping forever if the REPL keeps reading after end of input."""

    def __init__(self, text: str, max_reads: int = 100):
        super().__init__(text)
        self.reads = max_reads

    def readline(self, size: int = -1, /) -> str:  # type: ignore[override]
        self.reads -= 1
        if self.reads < 0:
            raise AssertionError("REPL did not stop at end of input")
        return super().readline(size)


class TestPrologREPL(unittest.TestCase):
    def run_repl(self, text: str) -> str:
        solver = prolog_solver(static_kb=parse_theory("p(1)."))
        stdout = io.StringIO()
        PrologREPL(solver, "prolog", stdin=BoundedInput(text), stdout=stdout).cmdloop()
        return stdout.getvalue()

    def test_exits_on_end_of_input(self):
        self.assertIn("X = 1", self.run_repl("?- p(X).\n"))

    def test_exits_on_end_of_input_with_pending_clause(self):
        self.run_repl("q(1)\n")
