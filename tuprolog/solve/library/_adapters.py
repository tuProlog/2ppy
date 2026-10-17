from jpype import JImplementationFor
from ._definititions import Runtime


@JImplementationFor("it.unibo.tuprolog.solve.library.Library")
class _KtLibrary:
    def __jclass_init__(self):
        pass

    def to_runtime(self):
        return Runtime.of(self)


@JImplementationFor("it.unibo.tuprolog.solve.library.Runtime")
class _KtRuntime:
    def __jclass_init__(self):
        pass

    def __add__(self, other):
        return self.plus(other)
