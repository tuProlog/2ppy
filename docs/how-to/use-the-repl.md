# Use the REPL

A REPL (read-eval-print loop) is an interactive shell: you type clauses and queries, and it prints
the answers. 2PPy has a Prolog REPL and a ProbLog one, plus a Python shell with the whole API
imported.

## Start a REPL

```bash
python -m tuprolog.repl.prolog     # Prolog
python -m tuprolog.repl.problog    # ProbLog: solutions also show their probability
python -m tuprolog                 # a Python shell, with the whole tuprolog API imported
```

## Write and query a program

In the Prolog REPL:

- a clause (e.g. `parent(abe, homer).`) is added to the knowledge base;
- `?-` followed by a query (e.g. `?- parent(X, homer).`) prints all its solutions;
- `:-` followed by a goal (e.g. `:- op(700, xfx, likes).`) runs it as a directive;
- `:help` lists the commands, and `:exit` (or end of input) leaves the REPL.

Input ends with a full stop: a line without one continues on the next line (prompted by `...>`).

```text
prolog> parent(abe, homer).
prolog> parent(homer, bart).
prolog> ?- parent(X,
...>   Y).
yes: parent(abe, homer)
    X = abe
    Y = homer
yes: parent(homer, bart)
    X = homer
    Y = bart
prolog> :- op(700, xfx, likes).
prolog> bart likes skate.
prolog> ?- X likes Y.
yes: bart likes skate
    X = bart
    Y = skate
prolog> ?- parent(bart, X).
no.
prolog> :exit
```

In the ProbLog REPL, clauses may carry probabilities (`0.6::heads.`), and each solution is
followed by its probability.

## Embed a REPL in a program

`tuprolog.repl.PrologREPL` runs a REPL over any solver, reading from and writing on any streams (it
is a [`cmd.Cmd`](https://docs.python.org/3/library/cmd.html)):

```pycon
>>> import io
>>> from tuprolog.repl import PrologREPL
>>> from tuprolog.solve.prolog import prolog_solver
>>> session = io.StringIO("parent(abe, homer).\n?- parent(X, homer).\n:exit\n")
>>> output = io.StringIO()
>>> PrologREPL(prolog_solver(), "prolog", stdin=session, stdout=output).cmdloop(intro="")
>>> print(output.getvalue())
prolog>prolog>yes: parent(abe, homer)
    X = abe
prolog>

```

## See also

- API: `tuprolog.repl` ([reference](../api/tuprolog/repl.md)).
- [Run probabilistic programs](run-probabilistic-programs.md).
