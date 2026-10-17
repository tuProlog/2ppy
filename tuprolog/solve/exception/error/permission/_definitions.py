from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.exception.error as _errors  # type: ignore


PermissionError = _errors.PermissionError


Operation = PermissionError.Operation


Permission = PermissionError.Permission


OPERATION_ACCESS = Operation.ACCESS


OPERATION_ADD_ALIAS = Operation.ADD_ALIAS


OPERATION_CLOSE = Operation.CLOSE


OPERATION_CREATE = Operation.CREATE


OPERATION_INPUT = Operation.INPUT


OPERATION_INVOKE = Operation.INVOKE


OPERATION_MODIFY = Operation.MODIFY


OPERATION_OPEN = Operation.OPEN


OPERATION_OUTPUT = Operation.OUTPUT


OPERATION_REPOSITION = Operation.REPOSITION


PERMISSION_BINARY_STREAM = Permission.BINARY_STREAM


PERMISSION_FLAG = Permission.FLAG


PERMISSION_OPERATOR = Permission.OPERATOR


PERMISSION_PAST_END_OF_STREAM = Permission.PAST_END_OF_STREAM


PERMISSION_PRIVATE_PROCEDURE = Permission.PRIVATE_PROCEDURE


PERMISSION_SOURCE_SINK = Permission.SOURCE_SINK


PERMISSION_STATIC_PROCEDURE = Permission.STATIC_PROCEDURE


PERMISSION_OOP_METHOD = Permission.OOP_METHOD


PERMISSION_STREAM = Permission.STREAM


PERMISSION_TEXT_STREAM = Permission.TEXT_STREAM


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.PermissionError.*")
