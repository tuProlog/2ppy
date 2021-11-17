from tuprolog import logger
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.unify.exception.NoUnifyException")
class _KtNoUnifyException:
    def __jclass_init__(cls):
        pass

    @property
    def term1(self):
        return self.getTerm1()

    @property
    def term2(self):
        return self.getTerm2()


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.unify.exception.*")
