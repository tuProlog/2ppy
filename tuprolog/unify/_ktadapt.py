from tuprolog import logger
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.unify.Unificator")
class _KtUnificator:
    def __jclass_init__(cls):
        pass

    @property
    def context(self):
        return self.getContext()


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.unify.*")
