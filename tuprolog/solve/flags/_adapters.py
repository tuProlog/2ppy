from jpype import JImplementationFor
from tuprolog import logger
from ._definitions import NotableFlag


@JImplementationFor("it.unibo.tuprolog.solve.flags.FlagStore")
class _KtFlagStore:
    def __jclass_init__(cls):
        pass

    def __len__(self):
        return self.getSize()

    def __getitem__(self, notableFlag):
        return self.get(notableFlag)

    def __add__(self, other):
        return self.plus(other)

    def __sub__(self, other):
        if isinstance(other, NotableFlag):
            return self.minus(other.name)
        return self.minus(other)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.flags.*")
