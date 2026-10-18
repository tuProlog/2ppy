from tuprolog.core import Term
from tuprolog.solve import ExecutionContext, Signature

from ._definitions import Operation, Permission, PermissionError

__all__ = ["operation", "permission_error", "permission_type"]


def permission_error(
    context: ExecutionContext,
    procedure: Signature,
    operation: Operation,
    permission: Permission,
    culprit: Term,
) -> PermissionError:
    return PermissionError.of(context, procedure, operation, permission, culprit)


def operation(name: str | Term) -> Operation:
    if isinstance(name, str):
        return Operation.of(name)
    else:
        return Operation.fromTerm(name)


def permission_type(name: str | Term) -> Permission:
    if isinstance(name, str):
        return Permission.of(name)
    else:
        return Permission.fromTerm(name)
