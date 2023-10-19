from tuprolog.repl import PrologREPL
from tuprolog.solve.problog import problog_solver


if __name__ == '__main__':
    PrologREPL(solver=problog_solver(mutable=True), name="problog").cmdloop()
