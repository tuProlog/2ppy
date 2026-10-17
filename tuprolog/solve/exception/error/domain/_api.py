from typing import Iterable, Union
from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature
from ._definitions import DomainError, Domain


def domain_error_for_flag_values(
        context: ExecutionContext,
        procedure: Signature,
        flag_values: Iterable[Term],
        actual: Term,
        index: int = None
) -> DomainError:
    return DomainError.forFlagValues(context, procedure, flag_values, actual, index)


def domain_error_for_argument(
        context: ExecutionContext,
        procedure: Signature,
        expected: Domain,
        actual: Term,
        index: int = None
) -> DomainError:
    return DomainError.forArgument(context, procedure, expected, actual, index)


def domain_error_for_term(
        context: ExecutionContext,
        expected: Domain,
        actual_value: Term,
) -> DomainError:
    return DomainError.forTerm(context, expected, actual_value)


def domain_error_for_goal(
        context: ExecutionContext,
        procedure: Signature,
        expected: Domain,
        actual: Term,
) -> DomainError:
    return DomainError.forGoal(context, procedure, expected, actual)


def domain(name: Union[str, Term]) -> Domain:
    if isinstance(name, str):
        return Domain.of(name)
    else:
        return Domain.fromTerm(name)
