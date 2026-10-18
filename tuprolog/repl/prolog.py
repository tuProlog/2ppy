from tuprolog.repl import PrologREPL
from tuprolog.solve.prolog import prolog_solver

__all__ = []


if __name__ == "__main__":
    PrologREPL(solver=prolog_solver(mutable=True), name="prolog").cmdloop()
