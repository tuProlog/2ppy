# Standard predicates

Prolog solvers made by `prolog_solver()` load the standard library `prolog.lang`
([`tuprolog.solve.stdlib`](../api/tuprolog/solve/stdlib.md)). It provides the predicates and the
arithmetic functions below, a subset of ISO Prolog's built-ins plus a few extensions. Predicates
are named by their **indicator**, `name/arity` (e.g. `member/2` takes two arguments).

More predicates come from other libraries: [IOLib](iolib.md) (streams), [OOPLib](ooplib.md)
(Python objects), and the libraries you write (see
[Define predicates in Python](../how-to/define-predicates-in-python.md)). For the detailed
semantics of each predicate, see 2P-Kt's
[default predicates](https://tuprolog.github.io/2p-kt/reference/default-predicates/), or ask the
solver itself: `help(Indicator, Text)` gives the documentation of a predicate.

```pycon
>>> from tuprolog.solve.prolog import prolog_solver
>>> solver = prolog_solver()
>>> print(solver.solve_once("help(member/2, Text)").to_dict()["Text"])
`member(?Element, ?List)`
<BLANKLINE>
Succeeds when `Element` is an element of `List`. ...

```

## Control

| Predicate | Meaning |
|---|---|
| `true/0`, `fail/0`, `false/0` | succeed; fail (these are atoms handled by the solver) |
| `','/2` | conjunction: `A, B` |
| `';'/2` | disjunction: `A ; B` (with `->/2`, if-then-else: `C -> T ; E`) |
| `'->'/2` | if-then: `C -> T` |
| `!/0` | cut: commit to the choices made since entering the current clause |
| `'\+'/1`, `not/1` | negation as failure: succeed if the goal has no solution |
| `call/1` | call a goal given as a term |
| `once/1` | the first solution of a goal only |
| `catch/3`, `throw/1` | catch and throw exceptions (see [Exceptions](exceptions.md)) |
| `repeat/0` | succeed infinitely many times on backtracking |
| `halt/0`, `halt/1` | stop the solver (with an exit code) |
| `sleep/1` | wait some milliseconds |

## Unification and comparison

| Predicate | Meaning |
|---|---|
| `'='/2`, `'\='/2` | unify; do not unify |
| `'=='/2`, `'\=='/2` | identical; not identical (no binding) |
| `'@<'/2`, `'@=<'/2`, `'@>'/2`, `'@>='/2` | standard order of terms |
| `'=@='/2`, `'\=@='/2` | equal in the standard order of terms; not equal (unlike ISO Prolog's, a variable equals only itself: `f(X) =@= f(Y)` fails) |
| `copy_term/2` | copy a term with fresh variables |

## Type checking

`var/1`, `nonvar/1`, `atom/1`, `number/1`, `integer/1`, `float/1`, `atomic/1`, `compound/1`,
`callable/1`, `ground/1`, `natural/1` (non-negative integer, or enumerates them),
`ensure_executable/1` (fails or raises unless the argument is a callable term).

## Term construction and inspection

| Predicate | Meaning |
|---|---|
| `functor/3` | `functor(f(a, b), f, 2)`: name and arity of a term, or a term from them |
| `arg/3` | `arg(1, f(a, b), a)`: the N-th argument of a compound term |
| `'=..'/2` | "univ": `f(a, b) =.. [f, a, b]` |

## Arithmetic

| Predicate | Meaning |
|---|---|
| `is/2` | `X is Expr` evaluates `Expr` and unifies the result with `X` |
| `'=:='/2`, `'=\='/2` | arithmetic equality, inequality |
| `'<'/2`, `'=<'/2`, `'>'/2`, `'>='/2` | arithmetic comparison |
| `between/3` | `between(Low, High, X)`: integers between bounds |

Functions usable in arithmetic expressions:

| Kind | Functions |
|---|---|
| operators | `+/2`, `-/2`, `-/1`, `*/2`, `//2` (division), `///2` (integer division), `**/2` (power, as a real), `mod/2`, `rem/2` |
| bitwise | `/\/2` (and), `\//2` (or), `\/1` (complement), `<</2`, `>>/2` (shifts) |
| rounding | `abs/1`, `sign/1`, `round/1`, `floor/1`, `ceiling/1`, `truncate/1`, `float/1`, `float_integer_part/1`, `float_fractional_part/1` |
| transcendental | `sqrt/1`, `exp/1`, `log/1`, `sin/1`, `cos/1`, `atan/1` |

```pycon
>>> list(solver.query("X is 7 // 2, Y is 7 mod 2, Z is 2 ** 3, W is sqrt(16)"))
[{'X': 3, 'Y': 1, 'Z': 8.0, 'W': 4.0}]

```

## Atoms and characters

`atom_length/2`, `atom_chars/2`, `atom_codes/2`, `atom_concat/3`, `sub_atom/5`, `char_code/2`,
`number_chars/2`, `number_codes/2`.

## Lists

`append/3`, `member/2`, `reverse/2`.

!!! note
    `length/2`, `sort/2` and `msort/2` are not available in the default solver (a known 2P-Kt
    issue): define what you need, e.g. by loading the clauses
    `length([], 0). length([_|T], N) :- length(T, M), N is M + 1.`

## All solutions

`findall/3`, `bagof/3`, `setof/3`: collect the solutions of a goal into a list (`setof/3`
removing duplicates).

```pycon
>>> list(solver.query("findall(X, member(X, [c, a, b, a]), L), setof(X, member(X, [c, a, b, a]), S)"))
[{'L': ['c', 'a', 'b', 'a'], 'S': ['c', 'a', 'b']}]

```

!!! note
    Unlike ISO Prolog's, 2P-Kt's `setof/3` does not sort the solutions: it keeps them in the order
    they are found.

## Knowledge base

| Predicate | Meaning |
|---|---|
| `assert/1`, `asserta/1`, `assertz/1` | add a clause to the dynamic knowledge base (`asserta` at the beginning, `assert` and `assertz` at the end) |
| `retract/1`, `retractall/1` | remove the first matching clause; all matching clauses |
| `abolish/1` | remove all the clauses of a predicate, given its indicator |
| `clause/2` | `clause(Head, Body)`: enumerate the clauses whose head unifies with `Head` |

The static knowledge base (`static_kb`) cannot be modified: changing its predicates raises a
`permission_error`. See [Solvers and solutions](../explanation/solvers-and-solutions.md).

## Flags and operators

| Predicate | Meaning |
|---|---|
| `current_prolog_flag/2`, `set_prolog_flag/2` | read and change flags (see `tuprolog.solve.flags`) |
| `current_flag/2`, `set_flag/2` | the same, also for flags other than ISO ones |
| `op/3`, `current_op/3` | define and enumerate operators |

## Output

`write/1` and `nl/0` write on the current output (by default, Python's `sys.stdout`). The
other output predicates, and all the input ones, come from [IOLib](iolib.md).

## Custom data

`set_durable/2`, `get_durable/2`, `set_ephemeral/2`, `get_ephemeral/2`, `set_persistent/2`,
`get_persistent/2`: store and read values attached to the solver's state, with different lifetimes
(see [`tuprolog.solve.data`](../api/tuprolog/solve/data.md)).

## Unknown predicates

By default, calling a predicate that does not exist fails, printing a warning (e.g. `No such a
predicate: foo/0`). Set the `unknown` flag to `error` to raise an `existence_error` instead, or to
`fail` to fail silently:

```pycon
>>> from tuprolog.solve.flags import DEFAULT_FLAG_STORE
>>> strict = prolog_solver(flags=DEFAULT_FLAG_STORE + {"unknown": "error"})
>>> strict.solve_once("catch(foo, error(E, _), true)")["E"]
existence_error(procedure, foo/0)

```

## ProbLog solvers

Solvers made by `problog_solver()` load the library `problog.lang` instead, which supports
probabilistic clauses (see [Run probabilistic programs](../how-to/run-probabilistic-programs.md)).
