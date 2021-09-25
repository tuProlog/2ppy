from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve as _solve
# noinspection PyUnresolvedReferences
from java.lang import System, Long
from tuprolog.core import Indicator, Struct, Term, Substitution, EMPTY_UNIFIER
from tuprolog.solve.exception import ResolutionException
from tuprolog.jvmutils import jlist

from functools import singledispatch

from typing import Iterable


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


def classic_solver_factory() -> SolverFactory:
    return Solver.getClassic()


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
    return System.currentTimeMillis()


MAX_TIME_DURATION: int = Long.MAX_VALUE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.*")
