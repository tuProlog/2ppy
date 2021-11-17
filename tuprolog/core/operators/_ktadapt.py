from tuprolog import logger
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.core.operators.Operator")
class _KtOperator:
    def __jclass_init__(cls):
        pass

    @property
    def functor(self):
        return self.getFunctor()

    @property
    def specifier(self):
        return self.getSpecifier()

    @property
    def priority(self):
        return self.getPriority()


@jpype.JImplementationFor("it.unibo.tuprolog.core.operators.OperatorSet")
class _KtOperatorSet:
    def __jclass_init__(cls):
        pass

    def __add__(self, other):
        return self.plus(other)

    def __sub__(self, other):
        return self.minus(other)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.core.operators.*")
