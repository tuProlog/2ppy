from tuprolog import logger
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.core.exception.SubstitutionException")
class _KtSubstitutionException:
    def __jclass_init__(cls):
        pass

    @property
    def substitution(self):
        return self.getSubstitution()


@jpype.JImplementationFor("it.unibo.tuprolog.core.exception.SubstitutionApplicationException")
class _KtSubstitutionApplicationException:
    def __jclass_init__(cls):
        pass

    @property
    def term(self):
        return self.getTerm()


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.core.exception.*")
