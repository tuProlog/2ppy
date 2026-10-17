from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.exception.error as errors  # type: ignore


ExistenceError = errors.ExistenceError


ObjectType = ExistenceError.ObjectType


OBJECT_PROCEDURE = ObjectType.PROCEDURE


OBJECT_SOURCE_SINK = ObjectType.SOURCE_SINK


OBJECT_RESOURCE = ObjectType.RESOURCE


OBJECT_STREAM = ObjectType.STREAM


OBJECT_OOP_ALIAS = ObjectType.OOP_ALIAS


OBJECT_OOP_METHOD = ObjectType.OOP_METHOD


OBJECT_OOP_CONSTRUCTOR = ObjectType.OOP_CONSTRUCTOR


OBJECT_OOP_PROPERTY = ObjectType.OOP_PROPERTY


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.error.ExistenceError.*")
