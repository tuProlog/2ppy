from jpype import JImplementationFor, JOverride

from tuprolog.core import Substitution


@JImplementationFor("it.unibo.tuprolog.solve.primitive.Solve.Request")
class _KtSolveRequest:
    def __jclass_init__(self):
        pass

    def reply_with(self, outcome, *side_effects):
        """Replies with a substitution, a solution, or a boolean condition."""
        return self.replyWith(outcome, None, *side_effects)

    def reply_success(self, substitution=None, *side_effects):
        if substitution is None:
            substitution = Substitution.empty()
        return self.replySuccess(substitution, None, *side_effects)

    def reply_fail(self, *side_effects):
        return self.replyFail(None, *side_effects)

    def reply_exception(self, exception, *side_effects):
        return self.replyException(exception, None, *side_effects)

    @JOverride
    def solve(self, goal, max_duration=None):
        """Solves goal in a sub-solver, by default within the remaining time of this request."""
        if max_duration is None:
            max_duration = self.getMaxDuration()
        return self._solve(goal, max_duration)
