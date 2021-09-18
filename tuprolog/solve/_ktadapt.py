from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.solve.SolverFactory")
class _KtSolverFactory:
    def __jclass_init__(self):
        pass


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.*")
