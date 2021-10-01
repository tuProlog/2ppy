from typing import Union
# noinspection PyUnresolvedReferences
import jpype.imports
from tuprolog import logger
from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.exception.error as errors


TypeError = errors.TypeError

Type = TypeError.Expected

TYPE_ATOM = Type.ATOM

TYPE_ATOMIC = Type.ATOMIC

TYPE_BOOLEAN = Type.BOOLEAN

TYPE_BYTE = Type.BYTE

TYPE_CALLABLE = Type.CALLABLE

TYPE_CHARACTER = Type.CHARACTER

TYPE_COMPOUND = Type.COMPOUND

TYPE_DEALIASING_EXPRESSION = Type.DEALIASING_EXPRESSION

TYPE_EVALUABLE = Type.EVALUABLE

TYPE_FLOAT = Type.FLOAT

TYPE_INTEGER = Type.INTEGER

TYPE_IN_CHARACTER = Type.IN_CHARACTER

TYPE_LIST = Type.LIST

TYPE_NUMBER = Type.NUMBER

TYPE_OBJECT_REFERENCE = Type.OBJECT_REFERENCE

TYPE_PAIR = Type.PAIR

TYPE_PREDICATE_INDICATOR = Type.PREDICATE_INDICATOR

TYPE_REFERENCE = Type.REFERENCE

TYPE_TYPE_REFERENCE = Type.TYPE_REFERENCE

TYPE_URL = Type.URL

TYPE_VARIABLE = Type.VARIABLE

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


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.TypeError.*")
