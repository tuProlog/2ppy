from jpype import JInt

from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import Type, TypeError

__all__ = [
    "expected_type",
    "type_error",
    "type_error_for_argument",
    "type_error_for_argument_list",
    "type_error_for_goal",
    "type_error_for_term",
]


def type_error(context: ExecutionContext, expected: Type, actual: Term, message: str) -> TypeError:
    return TypeError.of(context, expected, actual, message)


def type_error_for_argument_list(
    context: ExecutionContext,
    procedure: Signature,
    expected: Type,
    actual: Term,
    index: int | None = None,
) -> TypeError:
    return TypeError.forArgumentList(
        context, procedure, expected, actual, None if index is None else JInt(index)
    )


def type_error_for_argument(
    context: ExecutionContext,
    procedure: Signature,
    expected: Type,
    actual: Term,
    index: int | None = None,
) -> TypeError:
    return TypeError.forArgument(
        context, procedure, expected, actual, None if index is None else JInt(index)
    )


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


def expected_type(name: str | Term) -> Type:
    if isinstance(name, str):
        return Type.of(name)
    else:
        return Type.fromTerm(name)
