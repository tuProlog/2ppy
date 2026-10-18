"""The Prolog REPL, run as `python -m tuprolog.repl.prolog`.

It starts a `tuprolog.repl.PrologREPL` on a Prolog solver, with a mutable knowledge base
to which typed clauses are added. Importing this module does not start the REPL.
"""

from tuprolog.repl import PrologREPL
from tuprolog.solve.prolog import prolog_solver

__all__ = []


if __name__ == "__main__":
    PrologREPL(solver=prolog_solver(mutable=True), name="prolog").cmdloop()
