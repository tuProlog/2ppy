from jpype import JImplementationFor
from tuprolog.core import Substitution


@JImplementationFor("it.unibo.tuprolog.solve.primitive.Solve.Request")
class _KtSolveRequest:
    def __jclass_init__(self):
        pass

    def reply_with(self, substitution):
        return self.replyWith(substitution, None)

    def reply_success(self):
        return self.replySuccess(Substitution.empty(), None)
