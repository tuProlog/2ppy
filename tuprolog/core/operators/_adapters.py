from jpype import JImplementationFor

from tuprolog import logger


@JImplementationFor("it.unibo.tuprolog.core.operators.OperatorSet")
class _KtOperatorSet:
    def __jclass_init__(cls):
        pass

    def __add__(self, other):
        """Adds operators: `s + other` has the operators of both, those of `other` (an `OperatorSet`
        or an `Operator`) replacing those with the same functor and specifier.
        """
        return self.plus(other)

    def __sub__(self, other):
        """Removes operators: `s - other` lacks the operators of `other` (an `OperatorSet` or an
        `Operator`)."""
        return self.minus(other)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.core.operators.*")
