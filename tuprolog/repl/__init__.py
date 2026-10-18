r"""Interactive Prolog shells, i.e. read-eval-print loops (REPLs).

A REPL reads what the user types, evaluates it, prints the result, and loops. A Prolog REPL lets
users write a program clause by clause and query it, as in the shells of most Prolog systems:

- typing a clause (e.g. `parent(abe, homer).`) adds it to the solver's dynamic knowledge base;
- typing `?-` and a query (e.g. `?- parent(X, homer).`) prints all its solutions;
- typing `:-` and a goal (e.g. `:- op(700, xfx, likes).`) runs it as a directive;
- typing `:` and a command runs it: `:help` lists the commands, `:exit` leaves the REPL.

Input ends with a full stop (`.`): lines without one are joined to the next ones.

Run a REPL from the command line with `python -m tuprolog.repl.prolog` (for Prolog) or
`python -m tuprolog.repl.problog` (for ProbLog, i.e. probabilistic logic programming, whose
solutions also show their probability), or create a `PrologREPL` for any solver.

Examples:
    >>> import io
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> user_input = io.StringIO("parent(abe, homer).\n?- parent(abe, Who).\n:exit\n")
    >>> output = io.StringIO()
    >>> repl = PrologREPL(prolog_solver(mutable=True), "prolog", stdin=user_input, stdout=output)
    >>> repl.cmdloop(intro="")
    >>> print(output.getvalue())
    prolog>prolog>yes: parent(abe, homer)
        Who = homer
    prolog>

See Also:
    `tuprolog.solve`, for solving queries from Python.
"""

from ._definitions import *

__all__ = ["PrologREPL"]
