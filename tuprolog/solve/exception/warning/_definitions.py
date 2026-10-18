import it.unibo.tuprolog.solve.exception.warning as _warnings  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = ["InitializationIssue", "MissingPredicate"]


InitializationIssue = _warnings.InitializationIssue
"""The warning that an initialization goal, e.g. a directive of a theory, did not succeed.

Reported instead of aborting the loading of a theory, so that one misbehaving directive (e.g.
`:- initialization(Goal).`) does not prevent loading the rest.

Members (snake_case aliases as well): `goal`, the goal that failed or raised an error; `cause`,
the error it raised (`None` if it simply failed); besides those of
`tuprolog.solve.exception.ResolutionException`.

Examples:
    >>> from tuprolog.solve.channel import output_channel
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> from tuprolog.theory.parsing import parse_theory
    >>> warnings = []
    >>> _ = prolog_solver(
    ...     static_kb=parse_theory(":- initialization(fail)."),
    ...     warning=output_channel(warnings.append),
    ... )
    >>> [(type(w) is InitializationIssue, str(w.goal), w.cause) for w in warnings]
    [(True, 'fail', None)]
"""


MissingPredicate = _warnings.MissingPredicate
"""The warning that a goal called an undefined predicate.

Reported when the `unknown` flag is `warning` (the default; with `error`, an `existence_error`
is raised instead, and with `fail` the goal fails silently). The goal then fails.

Members (snake_case aliases as well): `signature`, the `tuprolog.solve.Signature` of the missing
predicate; besides those of `tuprolog.solve.exception.ResolutionException`.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.exception.warning.*")
