from collections.abc import Iterable, Mapping
from functools import singledispatch
from typing import Any

from tuprolog.core import EMPTY_UNIFIER, Struct, Substitution, Term, TermFormatter
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


@singledispatch
def signature(name: str, arity: int, vararg: bool = False) -> Signature:
    return Signature(name, arity, vararg)


# JPype resolves `Signature.Companion` to the nested class, not to the companion instance
_SIGNATURE_COMPANION = Signature.class_.getField("Companion").get(None)


@signature.register
def _signature_from_term(term: Term) -> Signature | None:
    # also covers indicators, including vararg ones (e.g. f/'+'(2, vararg))
    return _SIGNATURE_COMPANION.fromSignatureTerm(term)


@singledispatch
def yes_solution(
    signature: Signature,
    arguments: Iterable[Term],
    substitution: Substitution.Unifier = EMPTY_UNIFIER,
) -> Solution.Yes:
    return Solution.yes(signature, jlist(arguments), substitution)


@yes_solution.register
def _yes_solution_from_query(
    query: Struct, substitution: Substitution.Unifier = EMPTY_UNIFIER
) -> Solution.Yes:
    return Solution.yes(query, substitution)


@singledispatch
def no_solution(signature: Signature, arguments: Iterable[Term]) -> Solution.No:
    return Solution.no(signature, jlist(arguments))


@no_solution.register
def _no_solution_from_query(query: Struct) -> Solution.No:
    return Solution.no(query)


@singledispatch
def halt_solution(
    signature: Signature, arguments: Iterable[Term], exception: ResolutionException
) -> Solution.Halt:
    return Solution.halt(signature, jlist(arguments), exception)


@halt_solution.register
def _halt_solution_from_query(query: Struct, exception: ResolutionException) -> Solution.No:
    return Solution.halt(query, exception)


def current_time_instant() -> int:
    return JavaSystem.currentTimeMillis()


def solution_formatter(term_formatter: TermFormatter | None = None) -> SolutionFormatter:
    if term_formatter is None:
        term_formatter = TermFormatter.prettyExpressions()
    return SolutionFormatter.of(term_formatter)


def solve_options(
    lazy: bool = True,
    timeout: int = MAX_TIMEOUT,
    limit: int = ALL_SOLUTIONS,
    custom: Mapping[str, Any] = {},
    **kwargs: Any,
) -> SolveOptions:
    opts = dict(kwargs)
    for key in custom:
        opts[key] = custom[key]
    temp = SolveOptions.of(lazy, timeout, limit)
    if len(opts) > 0:
        return temp.setOptions(jmap(opts))
    return temp
