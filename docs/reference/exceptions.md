# Exceptions

2P-Kt signals problems with JVM exceptions. 2PPy lets Python code handle them idiomatically:
every 2P-Kt exception is also an instance of a Python class of
[`tuprolog.errors`](../api/tuprolog/errors.md), and, where it makes sense, of a Python built-in
exception (e.g. a Prolog type error is a `TypeError`). The classes of `tuprolog.errors` only
*classify* JVM exceptions: they are never instantiated directly.

## When exceptions are raised

| Operation | How errors surface |
|---|---|
| Parsing (`parse_term`, `parse_theory`, ...) | raised: `ParsingError` (a `ValueError`) |
| Building or applying substitutions | raised: `SubstitutionError` (a `ValueError`) |
| Loading libraries (`runtime + library`, ...) | raised: `LibraryError` |
| `Solver.query(goal)` | raised, when a solution halts with an error |
| `Solver.solve(goal)`, `Solver.solve_once(goal)` | *not* raised: the solution is a *halt* solution, whose `exception` holds the error; `solution.raise_error()` raises it |
| Inside Prolog code | thrown as terms, which `catch/3` can catch (see below) |

```pycon
>>> from tuprolog.errors import ParsingError, PrologTypeError, TuPrologError
>>> from tuprolog.solve.prolog import prolog_solver
>>> solver = prolog_solver()
>>> solution = solver.solve_once("atom_length(123, N)")
>>> solution.is_halt
True
>>> error = solution.exception
>>> isinstance(error, PrologTypeError), isinstance(error, TypeError), isinstance(error, TuPrologError)
(True, True, True)
>>> error.type
type_error(atom, 123)
>>> try:
...     list(solver.query("X is foo + 1"))
... except TypeError as e:
...     print(e.type)
type_error(evaluable, foo/0)

```

## The classes

| Class | Python bases | Raised when | 2P-Kt class(es) classified |
|---|---|---|---|
| `TuPrologError` | `Exception` | 2P-Kt raises any exception | `TuPrologException` |
| `SubstitutionError` | `TuPrologError`, `ValueError` | a substitution is invalid | `SubstitutionException` |
| `ParsingError` | `TuPrologError`, `ValueError` | some text is not valid Prolog | `ParseException`, `PrologSyntaxException` |
| `UnificationError` | `TuPrologError`, `ValueError` | two terms do not unify (when unification is asked to raise) | `NoUnifyException` |
| `LibraryError` | `TuPrologError` | a library cannot be found or loaded | `LibraryException` |
| `ResolutionError` | `TuPrologError` | solving a query goes wrong | `ResolutionException` |
| `HaltError` | `ResolutionError` | a query halts the solver (`halt/0,1`) | `HaltException` |
| `TimeOutError` | `ResolutionError` | a query runs out of time | `TimeOutException` |
| `PrologWarning` | `ResolutionError`, `Warning` | a warning is issued while solving | `Warning` |
| `PrologError` | `ResolutionError` | an ISO error term `error(Type, Extra)` is thrown | `LogicError` |
| `PrologTypeError` | `PrologError`, `TypeError` | `type_error(Type, Culprit)` | `TypeError` |
| `PrologDomainError` | `PrologError`, `ValueError` | `domain_error(Domain, Culprit)` | `DomainError` |
| `PrologRepresentationError` | `PrologError`, `ValueError` | `representation_error(Limit)` | `RepresentationError` |
| `PrologInstantiationError` | `PrologError`, `ValueError` | `instantiation_error` | `InstantiationError` |
| `PrologEvaluationError` | `PrologError`, `ArithmeticError` | `evaluation_error(Error)` | `EvaluationError` |
| `PrologExistenceError` | `PrologError`, `LookupError` | `existence_error(Type, Culprit)` | `ExistenceError` |
| `PrologPermissionError` | `PrologError` | `permission_error(Action, Type, Culprit)` | `PermissionError` |
| `PrologSyntaxError` | `PrologError`, `ValueError` | `syntax_error(Message)` | `SyntaxError` |
| `PrologSystemError` | `PrologError`, `RuntimeError` | `system_error` | `SystemError` |
| `PrologMessageError` | `PrologError` | any other thrown term | `MessageError` |

The 2P-Kt classes of `Prolog*Error`s live in `it.unibo.tuprolog.solve.exception.error`, and are
re-exported, under their 2P-Kt names, by the sub-packages of
[`tuprolog.solve.exception.error`](../api/tuprolog/solve/exception/error.md) (e.g.
`tuprolog.solve.exception.error.type.TypeError`). JVM exceptions keep their JVM bases too (e.g.
`java.lang.RuntimeException`) and their `message`.

Useful members:

- every `TuPrologError`: `message`;
- `ResolutionError`: `context` (the solver's state when the error occurred) and
  `logic_stack_trace` (the goals being solved, innermost first);
- `PrologError`: `type` (the error term, e.g. `type_error(atom, 123)`) and `extra_data`;
- `HaltError`: `exit_status`.

## ISO error terms

In Prolog, errors are terms thrown by `throw/1`: by convention, built-in predicates throw
`error(Type, Extra)`, where `Type` says what went wrong and `Extra` carries implementation-defined
details (in 2P-Kt, a message). Prolog code catches them with `catch(Goal, Catcher, Recovery)`.

| Error term | Meaning | Example goal |
|---|---|---|
| `instantiation_error` | an argument is an unbound variable, where a value is needed | `X is Y + 1` |
| `type_error(Type, Culprit)` | an argument has the wrong type | `atom_length(123, N)` |
| `domain_error(Domain, Culprit)` | an argument has the right type, but an inadmissible value | `atom_length(abc, -1)` |
| `existence_error(Kind, Culprit)` | something referred to does not exist | calling an unknown predicate, with the `unknown` flag set to `error` |
| `permission_error(Action, Kind, Culprit)` | an operation is not allowed | `assertz(atom(x))` (modifying a built-in) |
| `representation_error(Limit)` | an implementation limit is exceeded | `char_code(C, -1)` |
| `evaluation_error(Error)` | an arithmetic expression cannot be evaluated | `X is 1 / 0` |
| `syntax_error(Message)` | text being read is not valid Prolog | reading malformed text with `read/1` |
| `system_error` | an internal problem, e.g. an exception raised by Python code implementing a predicate | |

```pycon
>>> list(solver.query("catch(X is 1 / 0, error(E, _), true)"))
[{'E': evaluation_error(zero_divisor)}]
>>> list(solver.query("catch(atom_length(abc, -1), error(E, _), true)"))
[{'E': domain_error(not_less_than_zero, -1)}]

```

Python code implementing predicates and functions (see
[Define predicates in Python](../how-to/define-predicates-in-python.md)) may raise these errors
too, building them with the factories of the `tuprolog.solve.exception.error` sub-packages (e.g.
`type_error_for_argument`); any other Python exception becomes a `system_error`.

## See also

- [Handle errors](../how-to/handle-errors.md), a practical guide.
- 2P-Kt's [errors and exceptions](https://tuprolog.github.io/2p-kt/reference/errors-and-exceptions/).
