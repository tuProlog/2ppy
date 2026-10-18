"""The Python functions of the solving API, re-exported by `tuprolog.solve`."""

from collections.abc import Iterable, Mapping
from functools import singledispatch
from typing import Any

from tuprolog.core import (
    EMPTY_UNIFIER,
    Struct,
    Substitution,
    Term,
    TermFormatter,
    pretty_expressions_formatter,
)
from tuprolog.jvmutils import JavaSystem, jlist, jmap

from ._definitions import (
    ALL_SOLUTIONS,
    MAX_TIMEOUT,
    Signature,
    Solution,
    SolutionFormatter,
    SolveOptions,
)
from .exception import ResolutionException

__all__ = [
    "current_time_instant",
    "halt_solution",
    "no_solution",
    "signature",
    "solution_formatter",
    "solve_options",
    "yes_solution",
]


# JPype resolves `Signature.Companion` to the nested class, not to the companion instance
_SIGNATURE_COMPANION = Signature.class_.getField("Companion").get(None)


def signature(name: str | Term, arity: int | None = None, vararg: bool = False) -> Signature | None:
    """Creates the signature of a predicate or function, i.e. its name and arity.

    Three forms are accepted: `signature(name, arity, vararg=False)`, `signature("name/arity")`
    (split at the last slash), and `signature(term)`, where `term` is a signature term or an
    indicator, e.g. `f/2`, or `f/'+'(2, vararg)` for a variadic signature.

    Args:
        name: The name of the predicate or function, a `name/arity` string, or a signature term.
        arity: The number of arguments; omitted for `name/arity` strings and terms.
        vararg: Whether the signature is variadic, i.e. admits `arity` or more arguments.

    Returns:
        The signature, or `None` if `term` is not a well-formed signature term.

    Raises:
        TypeError: If `arity` is given with a term, or missing with a string not in the
            `name/arity` form.

    Examples:
        >>> from tuprolog.core import struct
        >>> signature("append/3")
        Signature(name=append, arity=3, vararg=false)
        >>> signature("f", 2) == signature(struct("/", "f", 2))
        True
        >>> signature("f", 1, vararg=True).vararg
        True
        >>> print(signature(struct("f", "x")))
        None
    """
    if isinstance(name, Term):
        if arity is not None:
            raise TypeError("signature(term) takes no arity")
        return _SIGNATURE_COMPANION.fromSignatureTerm(name)
    if arity is None:
        functor, slash, digits = name.rpartition("/")
        if not (slash and functor and digits.isdigit()):
            raise TypeError("signature(name, arity) requires an arity, or a `name/arity` string")
        name, arity = functor, int(digits)
    return Signature(name, arity, vararg)


@singledispatch
def yes_solution(
    signature: Signature,
    arguments: Iterable[Term],
    substitution: Substitution.Unifier = EMPTY_UNIFIER,
) -> Solution.Yes:
    """Creates a *yes* solution, i.e. one stating that a query holds.

    Called as `yes_solution(signature, arguments, substitution)`, where the query is the struct
    made of `signature`'s name and `arguments`, or as `yes_solution(query, substitution)`. Useful
    to test code handling solutions; solvers create their own.

    Args:
        signature: The signature of the query (or the query itself, a `tuprolog.core.Struct`).
        arguments: The arguments of the query.
        substitution: The variable bindings under which the query holds (none by default).

    Returns:
        The *yes* solution.

    Examples:
        >>> from tuprolog.core import atom, struct, substitution, var
        >>> X = var("X")
        >>> solution = yes_solution(struct("f", X), substitution({X: atom("a")}))
        >>> solution.is_yes, solution.solved_query
        (True, f(a))
        >>> yes_solution(signature("f/1"), [atom("a")]).query
        f(a)
    """
    return Solution.yes(signature, jlist(arguments), substitution)


@yes_solution.register
def _yes_solution_from_query(
    query: Struct, substitution: Substitution.Unifier = EMPTY_UNIFIER
) -> Solution.Yes:
    return Solution.yes(query, substitution)


@singledispatch
def no_solution(signature: Signature, arguments: Iterable[Term]) -> Solution.No:
    """Creates a *no* solution, i.e. one stating that a query does not hold.

    Called as `no_solution(signature, arguments)`, or as `no_solution(query)`.

    Args:
        signature: The signature of the query (or the query itself, a `tuprolog.core.Struct`).
        arguments: The arguments of the query.

    Returns:
        The *no* solution.

    Examples:
        >>> from tuprolog.core import struct
        >>> no_solution(struct("f", "a"))
        No(query=f(a))
    """
    return Solution.no(signature, jlist(arguments))


@no_solution.register
def _no_solution_from_query(query: Struct) -> Solution.No:
    return Solution.no(query)


@singledispatch
def halt_solution(
    signature: Signature, arguments: Iterable[Term], exception: ResolutionException
) -> Solution.Halt:
    """Creates a *halt* solution, i.e. one stating that resolution stopped because of an error.

    Called as `halt_solution(signature, arguments, exception)`, or as
    `halt_solution(query, exception)`.

    Args:
        signature: The signature of the query (or the query itself, a `tuprolog.core.Struct`).
        arguments: The arguments of the query.
        exception: The error that stopped resolution (see `tuprolog.solve.exception`).

    Returns:
        The *halt* solution.
    """
    return Solution.halt(signature, jlist(arguments), exception)


@halt_solution.register
def _halt_solution_from_query(query: Struct, exception: ResolutionException) -> Solution.No:
    return Solution.halt(query, exception)


def current_time_instant() -> int:
    """Returns the current time, as solvers measure it: milliseconds since the Unix epoch.

    Returns:
        The current time instant, as the JVM's `System.currentTimeMillis()` returns it.

    Examples:
        >>> import time
        >>> abs(current_time_instant() - time.time() * 1000) < 60_000
        True
    """
    return JavaSystem.currentTimeMillis()


def solution_formatter(term_formatter: TermFormatter | None = None) -> SolutionFormatter:
    """Creates a formatter of solutions as human-readable text, as REPLs show them.

    Args:
        term_formatter: How to format terms; by default, a pretty formatter writing operators in
            infix notation (see `tuprolog.core.pretty_expressions_formatter`).

    Returns:
        The solution formatter, whose `format(solution)` method returns the text.

    Examples:
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> solution = prolog_solver().solve_once("X = 1 + 2")
        >>> print(solution_formatter().format(solution))
        yes: 1 + 2 = 1 + 2
            X = 1 + 2
    """
    if term_formatter is None:
        term_formatter = pretty_expressions_formatter()
    return SolutionFormatter.of(term_formatter)


def solve_options(
    lazy: bool = True,
    timeout: int = MAX_TIMEOUT,
    limit: int = ALL_SOLUTIONS,
    custom: Mapping[str, Any] = {},
    *,
    probabilistic: bool = False,
    **kwargs: Any,
) -> SolveOptions:
    """Creates the options of a resolution, for `Solver.solve` and `Solver.solve_once`.

    Args:
        lazy: Whether solutions are computed one at a time, as the caller asks for them (lazy),
            or all at once before returning (eager, in which case `Solver.solve` returns a list:
            beware of queries with infinitely many solutions).
        timeout: The maximum duration of the resolution, in milliseconds; when it expires, the
            last solution is a *halt* with a `tuprolog.solve.exception.TimeOutException`.
            `MAX_TIMEOUT` (the default) means no timeout.
        limit: The maximum number of solutions; `ALL_SOLUTIONS` (the default) means no limit.
        custom: Custom options, by name, interpreted by specific solvers; they override the
            homonymous `kwargs`.
        probabilistic: Whether to compute the probabilities of solutions, for probabilistic
            solvers (see `tuprolog.solve.plp` and `tuprolog.solve.problog`).
        **kwargs: More custom options.

    Returns:
        The solve options.

    Examples:
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> solver = prolog_solver()
        >>> options = solve_options(lazy=False, limit=2)
        >>> options.is_eager, options.limit, options.timeout == MAX_TIMEOUT
        (True, 2, True)
        >>> [solution["X"] for solution in solver.solve("member(X, [a, b, c])", options)]
        [a, b]
        >>> solver.solve_once("repeat, fail", solve_options(timeout=50)).is_halt
        True
    """
    opts = dict(kwargs)
    for key in custom:
        opts[key] = custom[key]
    temp = SolveOptions.of(lazy, timeout, limit)
    if len(opts) > 0:
        temp = temp.setOptions(jmap(opts))
    if probabilistic:
        from tuprolog.solve.plp import set_probabilistic

        temp = set_probabilistic(temp, True)
    return temp
