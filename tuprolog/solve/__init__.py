from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve as _solve
from tuprolog.core import Indicator, Struct, Term, Substitution, EMPTY_UNIFIER, TermFormatter
from tuprolog.solve.exception import ResolutionException
from tuprolog.jvmutils import jlist, jmap, JavaSystem

from functools import singledispatch

from typing import Iterable, Mapping, Any


ExecutionContext = _solve.ExecutionContext

ExecutionContextAware = _solve.ExecutionContextAware

MutableSolver = _solve.MutableSolver

Signature = _solve.Signature

Solution = _solve.Solution

SolutionFormatter = _solve.SolutionFormatter

SolveOptions = _solve.SolveOptions

Solver = _solve.Solver

SolverFactory = _solve.SolverFactory

Time = _solve.Time


@singledispatch
def signature(name: str, arity: int, vararg: bool = False) -> Signature:
    return Signature(name, arity, vararg)


@signature.register
def _signature_from_indicator(indicator: Indicator) -> Signature:
    return Signature.fromIndicator(indicator)


@signature.register
def _signature_from_term(term: Term) -> Signature:
    return Signature.fromSignatureTerm(term)


@singledispatch
def yes_solution(
        signature: Signature,
        arguments: Iterable[Term],
        substitution: Substitution.Unifier = EMPTY_UNIFIER
) -> Solution.Yes:
    return Solution.yes(signature, jlist(arguments), substitution)


@yes_solution.register
def _yes_solution_from_query(query: Struct, substitution: Substitution.Unifier = EMPTY_UNIFIER) -> Solution.Yes:
    return Solution.yes(query, substitution)


@singledispatch
def no_solution(signature: Signature, arguments: Iterable[Term]) -> Solution.No:
    return Solution.no(signature, jlist(arguments))


@no_solution.register
def _no_solution_from_query(query: Struct) -> Solution.No:
    return Solution.no(query)


@singledispatch
def halt_solution(signature: Signature, arguments: Iterable[Term], exception: ResolutionException) -> Solution.Halt:
    return Solution.halt(signature, jlist(arguments), exception)


@halt_solution.register
def _halt_solution_from_query(query: Struct, exception: ResolutionException) -> Solution.No:
    return Solution.halt(query, exception)


def current_time_instant() -> int:
    return JavaSystem.currentTimeMillis()


def solution_formatter(term_formatter: TermFormatter = TermFormatter.prettyExpressions()) -> SolutionFormatter:
    return SolutionFormatter.of(term_formatter)


MAX_TIMEOUT: int = SolveOptions.MAX_TIMEOUT

ALL_SOLUTIONS: int = SolveOptions.ALL_SOLUTIONS


def solve_options(
        lazy: bool = True,
        timeout: int = MAX_TIMEOUT,
        limit: int = ALL_SOLUTIONS,
        custom: Mapping[str, Any] = dict(),
        **kwargs: Any
) -> SolveOptions:
    opts = dict(kwargs)
    for key in custom:
        opts[key] = custom[key]
    temp = SolveOptions.of(lazy, timeout, limit)
    if len(opts) > 0:
        return temp.setOptions(jmap(opts))
    return temp


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.*")
