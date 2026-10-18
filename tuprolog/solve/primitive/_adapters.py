from jpype import JImplementationFor, JOverride

from tuprolog.core import Substitution


@JImplementationFor("it.unibo.tuprolog.solve.primitive.Solve.Request")
class _KtSolveRequest:
    """Pythonic methods of `SolveRequest`s, to reply to them and to solve sub-goals."""

    def __jclass_init__(self):
        pass

    def reply_with(self, outcome, *side_effects):
        """Replies with a success or a failure, depending on `outcome`.

        Args:
            outcome: a substitution (success binding the goal's variables as it says, or failure if
                it is a failed one, e.g. a failed `mgu`), a `tuprolog.solve.Solution`, or a boolean
                (success without bindings, or failure).
            *side_effects: side effects on the solver's state to apply along with the response
                (see `tuprolog.solve.sideffects`).

        Returns:
            The response, to be returned or yielded by the primitive.

        Examples:
            >>> from tuprolog.core import atom
            >>> from tuprolog.solve.library import library
            >>> from tuprolog.solve.primitive import primitive
            >>> from tuprolog.solve.prolog import prolog_solver
            >>> def is_hello(request):
            ...     [argument] = request.arguments
            ...     yield request.reply_with(request.unificator.mgu(argument, atom("hello")))
            >>> lib = library("demo", primitives={"hello/1": primitive(is_hello)})
            >>> list(prolog_solver(libraries=lib).query("hello(X)"))
            [{'X': 'hello'}]
        """
        return self.replyWith(outcome, None, *side_effects)

    def reply_success(self, substitution=None, *side_effects):
        """Replies with a success.

        Args:
            substitution: the bindings of the goal's variables; none, by default.
            *side_effects: side effects on the solver's state to apply along with the response
                (see `tuprolog.solve.sideffects`).

        Returns:
            The response, to be returned or yielded by the primitive.
        """
        if substitution is None:
            substitution = Substitution.empty()
        return self.replySuccess(substitution, None, *side_effects)

    def reply_fail(self, *side_effects):
        """Replies with a failure, i.e. the goal has no (more) solutions.

        Args:
            *side_effects: side effects on the solver's state to apply along with the response
                (see `tuprolog.solve.sideffects`).

        Returns:
            The response, to be returned or yielded by the primitive.
        """
        return self.replyFail(None, *side_effects)

    def reply_exception(self, exception, *side_effects):
        """Replies with an error, ending the solutions (Prolog code can catch it, by `catch/3`).

        Raising `exception` from the primitive has the same effect.

        Args:
            exception: the error, a `tuprolog.solve.exception.ResolutionException` (e.g. one built
                by the factories of `tuprolog.solve.exception.error`).
            *side_effects: side effects on the solver's state to apply along with the response
                (see `tuprolog.solve.sideffects`).

        Returns:
            The response, to be returned or yielded by the primitive.
        """
        return self.replyException(exception, None, *side_effects)

    @JOverride
    def solve(self, goal, max_duration=None):
        """Solves a goal in a sub-solver sharing this request's context.

        Args:
            goal: the goal to solve (a `tuprolog.core.Struct`).
            max_duration: the time limit, in milliseconds; by default, the time left to this
                request.

        Returns:
            The (lazy) sequence of the goal's solutions (`tuprolog.solve.Solution`s).

        Examples:
            >>> from tuprolog.core import integer, struct, var
            >>> from tuprolog.solve.library import library
            >>> from tuprolog.solve.primitive import primitive
            >>> from tuprolog.solve.prolog import prolog_solver
            >>> def count_members(request):
            ...     items, count = request.arguments
            ...     solutions = request.solve(struct("member", var("X"), items))
            ...     n = sum(1 for solution in solutions if solution.is_yes)
            ...     yield request.reply_with(request.unificator.mgu(count, integer(n)))
            >>> lib = library("demo", primitives={"count_members/2": primitive(count_members)})
            >>> list(prolog_solver(libraries=lib).query("count_members([a, b, c], N)"))
            [{'N': 3}]
        """
        if max_duration is None:
            max_duration = self.getMaxDuration()
        return self._solve(goal, max_duration)
