"""The ProbLog REPL, run as `python -m tuprolog.repl.problog`.

It starts a `tuprolog.repl.PrologREPL` on a ProbLog (probabilistic logic programming) solver,
showing the probability of each solution, with a mutable knowledge base to which typed clauses
are added. Importing this module does not start the REPL.
"""

from tuprolog.repl import PrologREPL
from tuprolog.solve.problog import problog_solver

__all__ = []


if __name__ == "__main__":
    PrologREPL(solver=problog_solver(mutable=True), name="problog").cmdloop()
