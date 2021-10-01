from typing import Iterable, Union
from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.exception.error as errors
from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature

DomainError = errors.DomainError

Domain = DomainError.Expected

DOMAIN_wATOM_PROPERTY = Domain.ATOM_PROPERTY

DOMAIN_BUFFERING_MODE = Domain.BUFFERING_MODE

DOMAIN_CHARACTER_CODE_LIST = Domain.CHARACTER_CODE_LIST

DOMAIN_CLOSE_OPTION = Domain.CLOSE_OPTION

DOMAIN_DATE_TIME = Domain.DATE_TIME

DOMAIN_EOF_ACTION = Domain.EOF_ACTION

DOMAIN_FLAG_VALUE = Domain.FLAG_VALUE

DOMAIN_FORMAT_CONTROL_SEQUENCE = Domain.FORMAT_CONTROL_SEQUENCE

DOMAIN_IO_MODE = Domain.IO_MODE

DOMAIN_WELL_FORMED_LIST = Domain.WELL_FORMED_LIST

DOMAIN_NON_EMPTY_LIST = Domain.NON_EMPTY_LIST

DOMAIN_NOT_LESS_THAN_ZERO = Domain.NOT_LESS_THAN_ZERO

DOMAIN_OPERATOR_PRIORITY = Domain.OPERATOR_PRIORITY

DOMAIN_OPERATOR_SPECIFIER = Domain.OPERATOR_SPECIFIER

DOMAIN_ORDER = Domain.ORDER

DOMAIN_OS_FILE_PERMISSION = Domain.OS_FILE_PERMISSION

DOMAIN_OS_FILE_PROPERTY = Domain.OS_FILE_PROPERTY

DOMAIN_OS_PATH = Domain.OS_PATH

DOMAIN_PREDICATE_PROPERTY = Domain.PREDICATE_PROPERTY

DOMAIN_FLAG = Domain.FLAG

DOMAIN_READ_OPTION = Domain.READ_OPTION

DOMAIN_SELECTABLE_ITEM = Domain.SELECTABLE_ITEM

DOMAIN_SOCKET_ADDRESS = Domain.SOCKET_ADDRESS

DOMAIN_SOCKET_DOMAIN = Domain.SOCKET_DOMAIN

DOMAIN_SOURCE_SINK = Domain.SOURCE_SINK

DOMAIN_STREAM = Domain.STREAM

DOMAIN_STREAM_OPTION = Domain.STREAM_OPTION

DOMAIN_STREAM_OR_ALIAS = Domain.STREAM_OR_ALIAS

DOMAIN_STREAM_POSITION = Domain.STREAM_POSITION

DOMAIN_STREAM_PROPERTY = Domain.STREAM_PROPERTY

DOMAIN_STREAM_SEEK_METHOD = Domain.STREAM_SEEK_METHOD

DOMAIN_STREAM_TYPE = Domain.STREAM_TYPE

DOMAIN_TERM_STREAM_OR_ALIAS = Domain.TERM_STREAM_OR_ALIAS

DOMAIN_VAR_BINDING_OPTION = Domain.VAR_BINDING_OPTION

DOMAIN_WRITE_OPTION = Domain.WRITE_OPTION

DOMAIN_CLAUSE = Domain.CLAUSE

DOMAIN_RULE = Domain.RULE

DOMAIN_FACT = Domain.FACT

DIRECTIVE = Domain.DIRECTIVE


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


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.DomainError.*")
