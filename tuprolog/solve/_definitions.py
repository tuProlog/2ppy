"""The JVM types of 2P-Kt's solving API, re-exported by `tuprolog.solve`."""

import it.unibo.tuprolog.solve as _solve  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "ALL_SOLUTIONS",
    "MAX_TIMEOUT",
    "Durable",
    "ExecutionContext",
    "ExecutionContextAware",
    "MutableSolver",
    "Signature",
    "Solution",
    "SolutionFormatter",
    "SolveOptions",
    "Solver",
    "SolverBuilder",
    "SolverFactory",
    "Time",
]


Durable = _solve.Durable
"""An entity whose execution has a maximum duration, as `SolveOptions.timeout` sets.

Times are integers counting milliseconds (see `current_time_instant`). Members: `start_time`
(when the execution started), `max_duration`, `end_time` (`start_time + max_duration`),
`elapsed_time` and `remaining_time` (both relative to the current time).
Execution contexts and the requests to primitives (`tuprolog.solve.primitive.SolveRequest`) are
durable.
"""


ExecutionContext = _solve.ExecutionContext
"""The state of a solver during a resolution, as primitives and functions observe it.

A snapshot of everything a resolution depends on: the libraries, flags, static and dynamic
knowledge bases, operators and channels (see `ExecutionContextAware`), plus the current
`substitution` (the variable bindings found so far), the `procedure` (the goal being executed),
the `logic_stack_trace` (the goals being executed, innermost first), and `custom_data` (see
`tuprolog.solve.data`).

Execution contexts are immutable: primitives change the solver's state by returning side effects
(see `tuprolog.solve.sideffects`), never by changing the context. Primitives receive it as the
`context` of their request (`tuprolog.solve.primitive.SolveRequest`); `create_solver(...)` and
`create_mutable_solver(...)` make new solvers sharing its state, e.g. to solve sub-goals.
"""


ExecutionContextAware = _solve.ExecutionContextAware
"""An entity aware of the state of a solver: the base of `Solver` and `ExecutionContext`.

Members (read-only properties):

- `libraries`: the loaded libraries (a `tuprolog.solve.library.Runtime`);
- `flags`: the flags (a `tuprolog.solve.flags.FlagStore`);
- `static_kb` and `dynamic_kb`: the static and dynamic knowledge bases
  (`tuprolog.theory.Theory`);
- `operators`: the operators, i.e. those of the libraries and of the knowledge bases
  (`tuprolog.core.operators.OperatorSet`);
- `unificator`: the unification algorithm (`tuprolog.unify.Unificator`);
- `input_channels` and `output_channels`: the open channels, by name
  (`tuprolog.solve.channel.InputStore` and `OutputStore`);
- `standard_input`, `standard_output`, `standard_error` and `warnings`: shortcuts for the
  standard channels.
"""


MutableSolver = _solve.MutableSolver
"""A `Solver` whose state can also be changed by its users, between resolutions.

Solvers change their own state while solving (e.g. `assertz/1` adds clauses to the dynamic KB);
mutable solvers additionally let Python code change it, when no resolution is ongoing:

- knowledge bases: `load_static_kb(theory)`, `load_static_clauses(*clauses)`,
  `append_static_kb(theory)`, `reset_static_kb()`, and the same for the dynamic KB
  (`load_dynamic_kb`, `load_dynamic_clauses`, `append_dynamic_kb`, `reset_dynamic_kb`), plus
  `assertA(clause)`, `assertZ(clause)`, `retract(clause)` and `retractAll(clause)` on the
  dynamic KB;
- libraries: `load_library(library)`, `unload_library(library)`, `set_runtime(runtime)`;
- flags: `set_flag(name, value)`;
- operators: `add_operators(...)`, `remove_operators(...)`;
- channels: the assignable properties `standard_input`, `standard_output`, `standard_error` and
  `warnings`, which also take Python streams and callables (see
  `tuprolog.solve.channel.ensure_input_channel` and `ensure_output_channel`).

Solvers are mutable by default, e.g. `tuprolog.solve.prolog.prolog_solver(mutable=True)`.

Note:
    In 2P-Kt 3.0, assigning `standard_output` or `standard_error` has no effect on the channels
    predicates like `write/1` use: pass them when creating the solver instead (e.g.
    `prolog_solver(std_out=...)`).

Examples:
    >>> import io
    >>> from tuprolog.core import fact, struct
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> solver = prolog_solver()
    >>> solver.load_static_clauses(fact(struct("p", 1)), fact(struct("p", 2)))
    >>> solver.assertZ(struct("q", "a"))
    >>> list(solver.query("p(X), q(Y)"))
    [{'X': 1, 'Y': 'a'}, {'X': 2, 'Y': 'a'}]
    >>> solver.warnings = warnings = io.StringIO()
    >>> solver.solve_once("undefined").is_no
    True
    >>> warnings.getvalue().strip()
    'No such a predicate: undefined/0'
"""


Signature = _solve.Signature
"""The signature of a predicate or function: its name, arity, and whether it is variadic.

Predicates and functions are identified by name and arity (i.e. number of arguments), e.g.
`append/3`; variadic (*vararg*) signatures admit any number of arguments greater than or equal
to the arity. Members: `name`, `arity`, `vararg`, `to_term()` (the term `name/arity`),
`to_indicator()` (the `tuprolog.core.Indicator` `name/arity`, for non-variadic signatures).

Create signatures with `signature`, e.g. `signature("append/3")`.
"""


Solution = _solve.Solution
"""The outcome of solving a query: *yes*, *no*, or *halt*.

Each solution is one of three kinds, `Solution.Yes`, `Solution.No` and `Solution.Halt`, told
apart by the properties `is_yes`, `is_no` and `is_halt`:

- *yes*: the query holds; `substitution` binds its variables, and `solved_query` is the query
  with that substitution applied;
- *no*: the query does not hold (or has no more solutions); `substitution` is a failed one, and
  `solved_query` is `None`;
- *halt*: resolution stopped because of `exception`, a
  `tuprolog.solve.exception.ResolutionException` (e.g. a logic error).

Every solution also has the `query` it answers. Python additions:

- `bool(solution)` is `solution.is_yes`;
- `solution[name]` and `name in solution` look up the term bound to a variable, by name, among
  `solution.bindings`;
- `solution.to_dict()` converts the bindings to Python values;
- `solution.raise_error()` raises the exception of a *halt*.

Solutions are created by solvers, or by `yes_solution`, `no_solution` and `halt_solution`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> solution = prolog_solver().solve_once("X = f(Y), Y = 1")
    >>> solution.is_yes, solution.is_no, solution.is_halt
    (True, False, False)
    >>> solution["X"], "Y" in solution
    (f(1), True)
    >>> solution.to_dict()
    {'X': f(1), 'Y': 1}
"""


SolutionFormatter = _solve.SolutionFormatter
"""Formats solutions as human-readable text, as REPLs show them.

`format(solution)` gives, e.g., `yes: parent(abe, homer)` followed by the variable bindings, one
per line. Create one with `solution_formatter`.
"""


SolveOptions = _solve.SolveOptions
"""The options of a resolution: laziness, timeout, maximum number of solutions, and custom ones.

- *lazy* (the default) solving computes solutions one at a time, as the caller asks for the next
  one; *eager* solving computes them all before returning, as a list;
- the *timeout*, in milliseconds, bounds the duration of the whole resolution, after which the
  last solution is a *halt* with a `tuprolog.solve.exception.TimeOutException`
  (`MAX_TIMEOUT` means none);
- the *limit* bounds the number of solutions (`ALL_SOLUTIONS` means none);
- *custom* options, by name, are interpreted by specific solvers (e.g. the probabilistic option
  of `tuprolog.solve.plp`).

Options are immutable: `set_lazy(value)`, `set_timeout(value)`, `set_limit(value)`,
`set_options(dict)`, `add_options(dict)` return new options. Python additions make them a
read-only mapping, whose keys are `lazy`, `is_lazy`, `eager`, `is_eager`, `timeout`, `limit`,
and those of the custom options (also returned by the `options` property).

Create options with `solve_options`.

Examples:
    >>> from tuprolog.solve import solve_options
    >>> options = solve_options(limit=2, timeout=1000, my_option=1)
    >>> options.is_lazy, options.limit, options.timeout
    (True, 2, 1000)
    >>> options["my_option"], "timeout" in options
    (1, True)
"""


Solver = _solve.Solver
"""A logic solver: it solves queries against its knowledge bases and libraries.

The state of a solver (see `ExecutionContextAware`) is made of libraries, flags, a static and a
dynamic knowledge base, operators, and input/output channels. Solvers are *not* immutable: the
dynamic knowledge base, the flags, the operators and the channels change while solving queries
(e.g. by `assertz/1`), and can be changed between queries if the solver is a `MutableSolver`.

Solving methods take a goal, i.e. a `tuprolog.core.Struct` or a string, which is parsed with the
solver's operators:

- `query(goal, *, limit=None, timeout=None)`: Pythonic querying, yielding the variable bindings
  of each *yes* solution as a dict of Python values (see `Solution.to_dict`), and raising the
  exception of a *halt* one;
- `solve(goal, options=None)`: the solutions of `goal`, lazily (an iterable of `Solution`s, which
  may be infinite), or eagerly (a list) if `options.is_eager` (see `solve_options`); the last
  one is a *no* if the solver could not tell there were no more solutions until looking for
  them, or a *halt* if resolution stopped because of an error;
- `solve_once(goal, options=None)`: the first solution only;
- `solve_list(goal, ...)`: all the solutions, as a JVM list.

Other members: `copy(...)` and `clone()`, deriving a new solver from this one.

Create solvers with `tuprolog.solve.prolog.prolog_solver` or
`tuprolog.solve.problog.problog_solver`, or with a `SolverFactory`.

Examples:
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> solver = prolog_solver()
    >>> list(solver.query("member(X, [a, b, c])", limit=2))
    [{'X': 'a'}, {'X': 'b'}]
    >>> [solution.is_yes for solution in solver.solve("member(X, [a, b])")]
    [True, True, False]
    >>> solver.solve_once("atom_length(hello, N)")["N"]
    5
"""


SolverBuilder = _solve.SolverBuilder
"""A builder of solvers, step by step, as an alternative to the factory functions.

Get one from a `SolverFactory` (`new_builder()`), configure it with its fluent methods, called by
their JVM (camelCase) names as their snake_case names are the builder's properties (e.g.
`staticKb(theory)`, `dynamicKb(theory)`, `flags(store)`, `library(library)`, `noBuiltins()`,
`standardOutput(channel)`), and build a solver with `build()` or `build_mutable()`.

Examples:
    >>> from tuprolog.solve.prolog import PROLOG_SOLVER_FACTORY
    >>> from tuprolog.theory.parsing import parse_theory
    >>> builder = PROLOG_SOLVER_FACTORY.new_builder().staticKb(parse_theory("a."))
    >>> solver = builder.build()
    >>> list(solver.query("a"))
    [{}]
"""


SolverFactory = _solve.SolverFactory
"""A factory of solvers following one resolution strategy (e.g. Prolog's, or ProbLog's).

Factories hold the defaults of their solvers (e.g. `default_builtins`, the library of standard
predicates, and `default_flags`), and create them via `solver_of(...)`,
`solver_with_default_builtins(...)`, `mutable_solver_of(...)` and
`mutable_solver_with_default_builtins(...)`, taking all the parts of a solver's state, or via
`new_builder()` (see `SolverBuilder`). The factory functions
`tuprolog.solve.prolog.prolog_solver` and `tuprolog.solve.problog.problog_solver` are simpler to
use.
"""


Time = _solve.Time
"""2P-Kt's utilities for times, measured in milliseconds (see `current_time_instant`)."""


MAX_TIMEOUT: int = SolveOptions.MAX_TIMEOUT
"""The timeout meaning *no timeout*, i.e. the largest JVM long integer."""


ALL_SOLUTIONS: int = SolveOptions.ALL_SOLUTIONS
"""The limit meaning *all the solutions*, i.e. no limit on their number (`-1`)."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.*")
