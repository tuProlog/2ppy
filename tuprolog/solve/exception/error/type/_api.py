from typing import Union
from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature
from ._definitions import TypeError, Type


def type_error_for_flag_values(
        context: ExecutionContext,
        procedure: Signature,
        expected: Type,
        actual: Term,
        message: str
) -> TypeError:
    return TypeError.of(context, procedure, expected, actual, message)


def type_error_for_argument_list(
        context: ExecutionContext,
        procedure: Signature,
        expected: Type,
        actual: Term,
        index: int = None
) -> TypeError:
    return TypeError.forArgumentList(context, procedure, expected, actual, index)


def type_error_for_argument(
        context: ExecutionContext,
        procedure: Signature,
        expected: Type,
        actual: Term,
        index: int = None
) -> TypeError:
    return TypeError.forArgument(context, procedure, expected, actual, index)


def type_error_for_term(
        context: ExecutionContext,
        expected: Type,
        actual_value: Term,
) -> TypeError:
    return TypeError.forTerm(context, expected, actual_value)


def type_error_for_goal(
        context: ExecutionContext,
        procedure: Signature,
        expected: Type,
        actual: Term,
) -> TypeError:
    return TypeError.forGoal(context, procedure, expected, actual)


def type(name: Union[str, Term]) -> Type:
    if isinstance(name, str):
        return TypeError.valueOf(name)
    else:
        return TypeError.fromTerm(name)
