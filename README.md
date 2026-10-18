# 2PPy: tuProlog for Python

[![PyPI](https://img.shields.io/pypi/v/2ppy)](https://pypi.org/project/2ppy/)
[![Python](https://img.shields.io/pypi/pyversions/2ppy)](https://pypi.org/project/2ppy/)
[![CI/CD](https://github.com/tuProlog/2ppy/actions/workflows/check.yml/badge.svg)](https://github.com/tuProlog/2ppy/actions/workflows/check.yml)
[![Docs](https://img.shields.io/badge/docs-tuprolog.github.io%2F2ppy-blue)](https://tuprolog.github.io/2ppy/)
[![License](https://img.shields.io/github/license/tuProlog/2ppy)](https://github.com/tuProlog/2ppy/blob/master/LICENSE)

2PPy brings [tuProlog](https://github.com/tuProlog/2p-kt) (2P-Kt) to Python: an object-oriented,
modular ecosystem for symbolic AI and logic programming. With it, Python programs can

- build, parse, inspect and format **logic terms** (atoms, numbers, variables, compound terms,
  lists, clauses), converting them from and to Python values;
- **unify** terms, i.e. find the substitutions of variables making two terms equal;
- store logic **theories** (collections of clauses) and query them;
- **solve** queries with an ISO-compliant **Prolog** solver, or with a probabilistic
  **ProbLog** one, getting solutions as Python dictionaries or exceptions;
- extend solvers with **predicates and functions written in Python**, and let Prolog code
  **drive Python objects** (OOPLib) or read and write files and streams (IOLib);
- experiment interactively with a Prolog **REPL**.

2PPy wraps 2P-Kt (written in Kotlin) via [JPype](https://jpype.readthedocs.io): the logic is 2P-Kt's,
the API is Pythonic. No knowledge of 2P-Kt, Kotlin or Java is needed, and no Java installation
either.

> 2PPy is in __alpha__: its API may still change between minor versions.

## Installation

2PPy requires Python 3.10 or later:

```bash
pip install 2ppy        # or: uv add 2ppy
```

The package ships 2P-Kt's JARs, and depends on [`jdk4py`](https://pypi.org/project/jdk4py/),
which bundles a Java runtime. The Java virtual machine (JVM) is started, once per process, when
`tuprolog` is first imported: expect the first import to take a second or two.

## Quick start

```pycon
>>> from tuprolog.solve.prolog import prolog_solver
>>> from tuprolog.theory.parsing import parse_theory
>>> kb = parse_theory("""
...     parent(abe, homer). parent(homer, bart). parent(homer, lisa).
...     ancestor(X, Y) :- parent(X, Y).
...     ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
... """)
>>> solver = prolog_solver(static_kb=kb)
>>> for answer in solver.query("ancestor(abe, D)"):
...     print(answer)
{'D': 'homer'}
{'D': 'bart'}
{'D': 'lisa'}

```

## Guide

The examples below are [doctests](https://docs.python.org/3/library/doctest.html), checked by the
test suite. Every module, class and function has a docstring: use `help(...)` for the details, or
browse the [API reference](https://tuprolog.github.io/2ppy/reference/tuprolog/).

### Terms

Everything a logic program manipulates is a **term** (`tuprolog.core.Term`):

| Term | Prolog syntax | Python factory |
|------|---------------|----------------|
| atom (a symbolic constant) | `abe`, `'hello world'`, `[]` | `atom("abe")` |
| number (integer or real, of arbitrary precision) | `42`, `3.14` | `integer(42)`, `real(3.14)`, `numeric(...)` |
| variable (a placeholder for any term) | `X`, `_Tail`, `_` | `var("X")` |
| compound term, or structure (a functor applied to arguments) | `point(1, 2)` | `struct("point", 1, 2)` |
| list | `[1, 2 \| Tail]` | `logic_list(1, 2)`, `logic_list_from([1, 2], last=var("Tail"))` |
| tuple | `(a, b, c)` | `logic_tuple("a", "b", "c")` |
| clause (fact, rule or directive) | `p(X) :- q(X).` | `fact(...)`, `rule(...)`, `directive(...)`, `clause(...)` |

Terms are immutable. They can be created from Python values or parsed from Prolog text:

```pycon
>>> from tuprolog.core import struct, to_python, to_term, var
>>> from tuprolog.core.parsing import parse_term
>>> term = parse_term("f(X, [1, 2 | T], 'hello world')")
>>> term.functor, term.arity, term[1]
('f', 3, [1, 2 | T_...])
>>> term.is_struct, term.is_ground, term[1].is_list
(True, False, True)
>>> struct("point", 1, 2.5) == parse_term("point(1, 2.5)")
True
>>> to_term([1, "a", (2, 3)])  # Python values become terms...
[1, a, (2, 3)]
>>> to_python(parse_term("[1, a, (2, 3)]"))  # ...and back
[1, 'a', (2, 3)]

```

Factories expecting terms convert Python values with `to_term`: strings become atoms, numbers
numerics, booleans `true`/`false`, lists logic lists and tuples logic tuples.
Each `var("X")` call creates a *distinct* variable, whose printed name gets a unique suffix
(`X_0`, `X_1`, ...): reuse the same `Var` object to refer to the same variable.

```pycon
>>> from tuprolog.core import rule
>>> X = var("X")
>>> rule(struct("mortal", X), struct("human", X))
mortal(X_...) :- human(X_...)

```

### Unification

Two terms **unify** if some substitution of their variables makes them equal. The most general one
(the *most general unifier*, or mgu) is what Prolog computes when matching a goal against a clause:

```pycon
>>> from tuprolog.unify import match, mgu, unify
>>> substitution = mgu(parse_term("point(X, 2)"), parse_term("point(1, Y)"))
>>> substitution
{X_...=1, Y_...=2}
>>> substitution.is_success
True
>>> unify(parse_term("point(X, 2)"), parse_term("point(1, Y)"))  # the unified term
point(1, 2)
>>> match(parse_term("point(1, 2)"), parse_term("point(3, Y)"))
False

```

### Theories

A **theory** (or knowledge base) is an ordered collection of clauses: *facts* (`parent(abe, homer).`)
state what is true, *rules* (`ancestor(X, Y) :- parent(X, Y).`) what is true provided that their
body is. Theories are parsed from text (or files, see below) or built from clauses:

```pycon
>>> from tuprolog.core import fact
>>> from tuprolog.theory import theory
>>> kb = parse_theory("parent(abe, homer). parent(homer, bart).")
>>> len(kb)
2
>>> [str(clause) for clause in kb]
['parent(abe, homer) :- true', 'parent(homer, bart) :- true']
>>> len(kb + theory(fact(struct("parent", "homer", "lisa"))))
3

```

### Solving queries

A **solver** answers queries (goals) against a theory, enumerating their **solutions**:

- `solver.query(goal)` yields the bindings of each solution, as a dictionary from variable names
  to Python values, and raises the error a goal may halt with;
- `solver.solve_once(goal)` returns the first `Solution`, which is truthy if the goal succeeded;
- `solver.solve(goal, options)` iterates over all `Solution`s, each being a *yes* (with a
  substitution), a *no* (the goal failed), or a *halt* (the goal raised an error).

Goals are strings, parsed with the solver's operators, or terms.

```pycon
>>> solver = prolog_solver(static_kb=kb)
>>> list(solver.query("parent(abe, Child)"))
[{'Child': 'homer'}]
>>> solution = solver.solve_once("parent(Parent, bart)")
>>> bool(solution), solution["Parent"], solution.to_dict()
(True, homer, {'Parent': 'homer'})
>>> solver.solve_once("parent(bart, _)")
No(query=parent(bart, ...))
>>> list(solver.query("member(X, [a, b, c])", limit=2))  # at most two solutions
[{'X': 'a'}, {'X': 'b'}]

```

Solvers come with Prolog's standard built-in predicates (e.g. `member/2`, `findall/3`, `is/2`,
`assertz/1`, `catch/3`). A solver has a *static* knowledge base (`static_kb`), whose clauses
cannot be modified, and a *dynamic* one (`dynamic_kb`), which `assertz/1` and `retract/1` change:

```pycon
>>> solver = prolog_solver(dynamic_kb=parse_theory("counter(0)."))
>>> list(solver.query("retract(counter(N)), M is N + 1, assertz(counter(M))"))
[{'N': 0, 'M': 1}]
>>> list(solver.query("counter(N)"))
[{'N': 1}]

```

`tuprolog.solve.solve_options` sets how a query is solved: lazily or eagerly, with a `timeout`
(in milliseconds) or a `limit` on the number of solutions.

### Errors

Errors raised by 2P-Kt are Python exceptions, classified by `tuprolog.errors` *and* by Python's
built-in exceptions: e.g. parsing errors are `ParsingError`s and `ValueError`s, a logic
`type_error` is a `PrologTypeError` and a `TypeError`, and every error is a `TuPrologError`.

```pycon
>>> from tuprolog.errors import PrologTypeError
>>> try:
...     list(solver.query("X is foo + 1"))
... except PrologTypeError as error:
...     print(error.type)
type_error(evaluable, foo/0)
>>> solver.solve_once("atom_length(X, 3)").is_halt  # solve and solve_once do not raise
True

```

### Input and output

Python streams (`io.IOBase`: files, `sys.stdin`, `io.StringIO`, `io.BytesIO`, ...) are accepted
wherever 2P-Kt reads or writes: by parsers (e.g. `read_theory(open("kb.pl"))`), by solvers' channels,
and by JVM methods expecting streams, readers or writers. Binary streams are UTF-8 encoded.
By default, solvers read from and write on Python's current `sys.stdin`, `sys.stdout` and
`sys.stderr`.

```pycon
>>> import io
>>> output = io.StringIO()
>>> prolog_solver(std_out=output).solve_once("write(hello), nl").is_yes
True
>>> output.getvalue()
'hello\n'

```

### Predicates and functions in Python

Solvers can be extended with **libraries** of plain Python functions, whose arguments and results
are converted from and to terms:

- `tuprolog.solve.primitive.predicate` makes a predicate (a *primitive*) out of a function
  returning a boolean (whether the goal succeeds), or returning (or yielding) tuples of argument
  values, one per solution;
- `tuprolog.solve.function.function` makes an arithmetic function, usable in `is/2`.

```pycon
>>> from tuprolog.solve.function import function
>>> from tuprolog.solve.library import library
>>> from tuprolog.solve.primitive import predicate
>>> lib = library(
...     "my.lib",
...     primitives={
...         "upper/2": predicate(lambda text, _: [(text, text.upper())]),
...         "even/1": predicate(lambda n: n % 2 == 0),
...     },
...     functions={"half/1": function(lambda x: x / 2)},
... )
>>> solver = prolog_solver(libraries=lib)
>>> list(solver.query("upper(abc, U), H is half(3)"))
[{'U': 'ABC', 'H': 1.5}]
>>> list(solver.query("member(N, [1, 2, 3, 4]), even(N)"))
[{'N': 2}, {'N': 4}]

```

Python exceptions raised by these functions become logic `system_error`s, which `catch/3` can
handle. Lower-level primitives, working on terms and solver requests, are made by
`tuprolog.solve.primitive.primitive`.

### Libraries: IOLib and OOPLib

`tuprolog.solve.libs` offers two more libraries, to be passed to solvers (combine several ones with
`tuprolog.solve.library.libraries`):

- `IOLib`, ISO Prolog's stream predicates (`open/3`, `read/1`, `get_char/1`, `write/1`, ...);
- `OOPLib`, letting Prolog code create Python objects, call their methods and read their
  attributes (via the `:=` operator and aliases like `$math`).

```pycon
>>> from tuprolog.solve.libs import OOPLib
>>> solver = prolog_solver(libraries=OOPLib)
>>> list(solver.query("X := $math.sqrt(16)"))
[{'X': 4.0}]
>>> list(solver.query("new_object($list, [], L), L.append(a), L.append(b), list_items(L, Items)"))
[{'L': '<object:list#...>', 'Items': ['a', 'b']}]
>>> list(solver.query("X := '42' as $int"))  # conversions call types
[{'X': 42}]

```

Aliases (`$name`) cover Python's built-in types (also under OOPLib's names, e.g. `$arraylist`),
`$builtins`, `$stdin`/`$stdout`/`$stderr`, and side-effect free standard modules (`$math`, `$json`,
`$re`, `$itertools`, ...). Only those modules are importable, and private attributes are not
accessible: `oop_lib(allow_all_imports=True, allow_private=True, aliases={...})` builds a library
lifting these limits or adding aliases. They limit what Prolog code can reach, without sandboxing it.

### Probabilistic logic programming

A [ProbLog](https://dtai.cs.kuleuven.be/problog/) solver handles clauses annotated with
probabilities (`P::Clause`), and computes the probability of each solution:

```pycon
>>> from tuprolog.solve import solve_options
>>> from tuprolog.solve.plp import probability
>>> from tuprolog.solve.problog import PROBLOG_OPERATORS, problog_solver
>>> coins = parse_theory(
...     "0.6::heads(c1). 0.5::heads(c2). two_heads :- heads(c1), heads(c2).", PROBLOG_OPERATORS
... )
>>> solver = problog_solver(static_kb=coins)
>>> [probability(s) for s in solver.solve("two_heads", solve_options(probabilistic=True))]
[0.3]

```

### Interactive use

- `python -m tuprolog` opens a Python shell with the whole API imported;
- `python -m tuprolog.repl.prolog` opens a Prolog [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop),
  `python -m tuprolog.repl.problog` a ProbLog one.

## Package overview

| Package | Content |
|---------|---------|
| `tuprolog.core` | terms and clauses: types, factories, conversions from and to Python, formatters |
| `tuprolog.core.parsing` | parsing terms and clauses from strings and streams |
| `tuprolog.core.operators` | operators (e.g. `:-`, `+`, `is`), which drive parsing and formatting |
| `tuprolog.unify` | unification and substitutions |
| `tuprolog.theory`, `tuprolog.theory.parsing` | theories (indexed collections of clauses) and their parsing |
| `tuprolog.collections` | other indexed collections of clauses (multisets and queues) |
| `tuprolog.solve` | the solver API: solvers, solutions, solve options |
| `tuprolog.solve.prolog`, `tuprolog.solve.problog`, `tuprolog.solve.plp` | Prolog and ProbLog solvers, probabilistic utilities |
| `tuprolog.solve.primitive`, `tuprolog.solve.function`, `tuprolog.solve.library` | predicates, functions and libraries, also from Python code |
| `tuprolog.solve.libs`, `tuprolog.solve.stdlib` | IOLib and OOPLib, and the standard built-ins |
| `tuprolog.solve.channel`, `tuprolog.solve.flags`, `tuprolog.solve.sideffects`, `tuprolog.solve.data` | solvers' I/O channels, flags, side effects, custom data |
| `tuprolog.solve.exception`, `tuprolog.errors` | logic errors and warnings, and their Python exception classes |
| `tuprolog.repl` | the REPLs |

JVM objects keep their JVM methods, with snake_case aliases (`getArity()` is also the property
`arity`, `isGround()` the property `is_ground`): the methods without a Pythonic counterpart may
return JVM types (e.g. `java.lang.String`).

## Further reading

2PPy mirrors the design and the module structure of 2P-Kt, whose
[documentation](https://tuprolog.github.io/2p-kt/) explains its concepts in depth (e.g. the
[term hierarchy](https://tuprolog.github.io/2p-kt/reference/term-hierarchy/), the
[solver API](https://tuprolog.github.io/2p-kt/reference/solver-api/), the
[default predicates](https://tuprolog.github.io/2p-kt/reference/default-predicates/)), and whose
[API reference](https://tuprolog.github.io/2p-kt/api/) documents the JVM types 2PPy exposes.

## How to contribute to 2PPy

The project follows [template-python-project-uv](https://github.com/gciatto/template-python-project-uv).
Requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/) and
[Apache Maven](https://maven.apache.org/install.html) (`mvn` on the `PATH`), which downloads
2P-Kt's JARs from [Maven Central](https://mvnrepository.com/artifact/it.unibo.tuprolog), as declared in
[`pom.xml`](https://github.com/tuProlog/2ppy/blob/master/pom.xml).

```bash
uv sync                      # create the environment, with the development tools
uv run poe fetch-jars        # download the JARs into tuprolog/libs/ (needed before testing or building)
uv run poe test              # run the tests (including the examples in docstrings and in this README)
uv run poe static-checks     # compileall, ruff format --check, ruff check, mypy (what CI runs)
uv run poe static-fixes      # ruff check --fix + ruff format
uv run poe coverage && uv run poe coverage-report
uv run poe docs              # documentation site in site/ (API reference from the docstrings)
uv run poe docs-serve        # the same, served with live reload
uv build                     # wheel and sdist in dist/ (JARs included)
```

Write the code inside `tuprolog/` and the tests inside `tests/`.
Contributor notes (layout, conventions, documentation style) are in [`AGENTS.md`](https://github.com/tuProlog/2ppy/blob/master/AGENTS.md).
Optional local Git hooks: `uv run poe install-hooks [HOOK...]` (`pre-commit`, `conventional-commits`,
`no-ai-signature`, `pre-push`).

### Releases

Commits follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):
on every push to `master`, [semantic-release](https://semantic-release.gitbook.io/semantic-release/)
derives the next version from them, publishes it on [PyPI](https://pypi.org/project/2ppy/), and creates the
corresponding [GitHub Release](https://github.com/tuProlog/2ppy/releases).
`pyproject.toml` is the only version source: never bump it by hand.
The release workflow needs the `PYPI_TOKEN` and `RELEASE_TOKEN` repository secrets.

CI runs the static checks and the tests on Ubuntu, Windows and macOS, with Python 3.10 to 3.13,
and builds the documentation site, which every push to `master` deploys on
[GitHub Pages](https://tuprolog.github.io/2ppy/).
Dependencies are kept up to date by [Renovate](https://docs.renovatebot.com/).
