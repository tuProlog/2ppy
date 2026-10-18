from ._api import *
from ._definitions import *
from ._definitions import (
    PermissionError,  # not in __all__, as star-imports would shadow the builtin
)

__all__ = [
    "OPERATION_ACCESS",
    "OPERATION_ADD_ALIAS",
    "OPERATION_CLOSE",
    "OPERATION_CREATE",
    "OPERATION_INPUT",
    "OPERATION_INVOKE",
    "OPERATION_MODIFY",
    "OPERATION_OPEN",
    "OPERATION_OUTPUT",
    "OPERATION_REPOSITION",
    "PERMISSION_BINARY_STREAM",
    "PERMISSION_FLAG",
    "PERMISSION_OOP_METHOD",
    "PERMISSION_OPERATOR",
    "PERMISSION_PAST_END_OF_STREAM",
    "PERMISSION_PRIVATE_PROCEDURE",
    "PERMISSION_SOURCE_SINK",
    "PERMISSION_STATIC_PROCEDURE",
    "PERMISSION_STREAM",
    "PERMISSION_TEXT_STREAM",
    "Operation",
    "Permission",
    "operation",
    "permission_error",
    "permission_type",
]
