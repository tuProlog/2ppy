from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.DomainError")
class _KtDomainError:
    def __jclass_init__(self):
        pass

    @property
    def expected_domain(self):
        return self.getExpectedDomain()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.DomainError.Expected")
class _KtExpectedDomain:
    def __jclass_init__(self):
        pass

    @property
    def domain(self):
        return self.getDomain()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.EvaluationError")
class _KtEvaluationError:
    def __jclass_init__(self):
        pass

    @property
    def error_type(self):
        return self.getErrorType()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.ExistenceError")
class _KtExistenceError:
    def __jclass_init__(self):
        pass

    @property
    def expected_object(self):
        return self.getExpectedObject()

    @property
    def culprit(self):
        return self.getCulprit()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.ExistenceError.ObjectType")
class _KtObjectType:
    def __jclass_init__(self):
        pass

    @property
    def type(self):
        return self.getType()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.InstantiationError")
class _KtInstantiationError:
    def __jclass_init__(self):
        pass

    @property
    def culprit(self):
        return self.getCulprit()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.MessageError")
class _KtMessageError:
    def __jclass_init__(self):
        pass

    @property
    def content(self):
        return self.getContent()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.PermissionError")
class _KtPermissionError:
    def __jclass_init__(self):
        pass

    @property
    def culprit(self):
        return self.getCulprit()

    @property
    def operation(self):
        return self.getOperation()

    @property
    def permission(self):
        return self.getPermission()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.ExistenceError.PermissionError.Operation")
class _KtOperation:
    def __jclass_init__(self):
        pass

    @property
    def operation(self):
        return self.getOperation()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.ExistenceError.PermissionError.Permission")
class _KtPermission:
    def __jclass_init__(self):
        pass

    @property
    def permission(self):
        return self.getPermission()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.RepresentationError")
class _KtRepresentationError:
    def __jclass_init__(self):
        pass

    @property
    def limit(self):
        return self.getLimit()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.ExistenceError.RepresentationError.Limit")
class _KtLimit:
    def __jclass_init__(self):
        pass

    @property
    def limit(self):
        return self.getLimit()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.TypeError")
class _KtTypeError:
    def __jclass_init__(self):
        pass

    @property
    def expected_type(self):
        return self.getExpectedDomain()

    @property
    def culprit(self):
        return self.getCulprit()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.error.TypeError.Expected")
class _KtExpectedType:
    def __jclass_init__(self):
        pass

    @property
    def type(self):
        return self.getType()


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.exception.error.*")
