from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.warning.InitializationIssue")
class _KtInitializationIssue:
    def __jclass_init__(self):
        pass

    @property
    def goal(self):
        return self.getGoal()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.warning.MissingPredicate")
class _KtMissingPredicate:
    def __jclass_init__(self):
        pass

    @property
    def signature(self):
        return self.getSignature()


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.exception.warning.*")
