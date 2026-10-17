from tuprolog.repl import PrologREPL
from tuprolog.solve.prolog import prolog_solver


if __name__ == '__main__':
    PrologREPL(solver=prolog_solver(mutable=True), name="prolog").cmdloop()
