# Define predicates in Python

Solvers can call Python code: a predicate (e.g. `upper(abc, U)`) or an arithmetic function (e.g.
`X is half(3)`) can be implemented by a Python function. Implementations are packed into
*libraries*, which are given to solvers. This guide goes from the simplest way to the most
flexible one.

## Write a predicate as a plain function

`tuprolog.solve.primitive.predicate` turns a Python function into a predicate. The goal's arguments
are converted into Python values (atoms become strings, numbers numbers, lists lists; unbound
variables stay `tuprolog.core.Var`s), and the function either:

- returns a boolean: whether the goal succeeds (without binding variables);
- returns, or yields, tuples of argument values, one per solution: each tuple is unified with the
  goal's arguments, binding its variables (tuples that do not unify are skipped). For predicates of
  arity 1, plain values work too.

```pycon
>>> from tuprolog.solve.library import library
>>> from tuprolog.solve.primitive import predicate
>>> from tuprolog.solve.prolog import prolog_solver
>>> def between(low, high, _):
...     return ((low, high, x) for x in range(low, high + 1))
>>> lib = library(
...     "my.lib",
...     primitives={
...         "even/1": predicate(lambda n: n % 2 == 0),
...         "upper/2": predicate(lambda text, _: [(text, text.upper())]),
...         "between/3": predicate(between),
...     },
... )
>>> solver = prolog_solver(libraries=lib)
>>> list(solver.query("between(1, 6, X), even(X)"))
[{'X': 2}, {'X': 4}, {'X': 6}]
>>> list(solver.query("upper(abc, U)"))
[{'U': 'ABC'}]

```

Predicates are registered by *indicator*, `name/arity`. Yielding solutions lazily, as `between`
does, lets solvers stop as soon as they have enough.

## Write an arithmetic function

`tuprolog.solve.function.function` turns a Python function into an arithmetic function, usable
wherever Prolog evaluates expressions (`is/2`, `</2`, ...). Its arguments are evaluated first:

```pycon
>>> from tuprolog.solve.function import function
>>> lib = library("my.math", functions={"half/1": function(lambda x: x / 2)})
>>> list(prolog_solver(libraries=lib).query("X is half(3) + 1"))
[{'X': 2.5}]

```

## Bundle predicates, functions, clauses and operators

A library can hold any mix of primitives, functions, clauses written in Prolog, and operators:

```pycon
>>> from tuprolog.core.operators import DEFAULT_OPERATORS, XFX, operator, operator_set
>>> from tuprolog.theory.parsing import parse_clauses
>>> shouts = operator_set(operator("shouts", XFX, 700))
>>> lib = library(
...     "shout",
...     primitives={"upper/2": predicate(lambda text, _: [(text, text.upper())])},
...     clauses=parse_clauses(  # parsed with the operator, too
...         "X shouts Y :- upper(X, U), atom_concat(U, '!', Y).", DEFAULT_OPERATORS + shouts
...     ),
...     operators=shouts,
... )
>>> list(prolog_solver(libraries=lib).query("hello shouts Y"))
[{'Y': 'HELLO!'}]

```

Give several libraries to a solver with `tuprolog.solve.library.libraries`:

```pycon
>>> from tuprolog.solve.library import libraries
>>> from tuprolog.solve.libs import OOPLib
>>> solver = prolog_solver(libraries=libraries(lib, OOPLib))
>>> sorted(solver.libraries.aliases)  # prolog.lang holds the standard predicates
['prolog.lang', 'prolog.oop.python', 'shout']

```

## Report errors

Exceptions raised by your Python code become logic errors: a `system_error`, which Prolog code can
catch with `catch/3`, and which halts the query otherwise:

```pycon
>>> solver = prolog_solver(
...     libraries=library(
...         "my.lib",
...         primitives={
...             "upper/2": predicate(lambda text, _: [(text, text.upper())]),
...         },
...     )
... )
>>> solver.solve_once("catch(upper(42, U), error(E, _), true)")["E"]
system_error

```

To raise the standard ISO errors instead (e.g. `type_error(atom, 42)`), write a *primitive*, as
shown next, and check its arguments with the `ensuring_*` functions.

## Write a primitive

`tuprolog.solve.primitive.primitive` gives full control: the Python function receives the *solve
request* (`request.arguments` as terms, `request.context` with the solver's state) and yields
*solve responses*, one per solution, built by the request's `reply_*` methods:

| Method | Meaning |
|--------|---------|
| `request.reply_success(substitution)` (or `reply_with`) | a solution, binding variables as the substitution says |
| `request.reply_fail()` | no (more) solutions |
| `request.reply_exception(error)` | an error |

The `ensuring_*` functions check arguments, raising the matching ISO error (e.g.
`ensuring_argument_is_atom(request, 0)` raises `type_error(atom, Culprit)` unless the first
argument is an atom):

```pycon
>>> from tuprolog.core import atom
>>> from tuprolog.solve.primitive import ensuring_argument_is_atom, primitive
>>> def upper(request):
...     ensuring_argument_is_atom(request, 0)
...     text, result = request.arguments
...     upper_case = atom(str(text.value).upper())
...     yield request.reply_with(request.context.unificator.mgu(result, upper_case))
>>> solver = prolog_solver(libraries=library("my.lib", primitives={"upper/2": primitive(upper)}))
>>> list(solver.query("upper(abc, U)"))
[{'U': 'ABC'}]
>>> solver.solve_once("catch(upper(42, U), error(E, _), true)")["E"]
type_error(atom, 42)

```

Primitives can also change the solver's state (e.g. add clauses, set flags) via the *side effects*
of `tuprolog.solve.sideffects`, attached to responses.

## See also

- Example notebook: [Predicates and functions in Python](../examples/03-predicates-and-functions-in-python.ipynb).
- API: `tuprolog.solve.primitive` ([reference](../api/tuprolog/solve/primitive.md)),
  `tuprolog.solve.function` ([reference](../api/tuprolog/solve/function.md)),
  `tuprolog.solve.library` ([reference](../api/tuprolog/solve/library.md)),
  `tuprolog.solve.sideffects` ([reference](../api/tuprolog/solve/sideffects.md)).
- [Exceptions](../reference/exceptions.md), for the ISO error families.
- 2P-Kt's [primitives and functions](https://tuprolog.github.io/2p-kt/reference/primitives-and-functions/)
  and [libraries](https://tuprolog.github.io/2p-kt/reference/libraries/).
