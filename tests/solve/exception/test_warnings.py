from tuprolog.core import atom, struct
from tuprolog.solve.exception import ResolutionException, Warning
from tuprolog.solve.exception.error import syntax_error
from tuprolog.solve.exception.warning import (
    InitializationIssue,
    MissingPredicate,
    initialization_issue,
    missing_predicate,
)


def test_initialization_issue_on_failure(context):
    goal = struct("init", atom("x"))
    issue = initialization_issue(goal, context)
    assert isinstance(issue, InitializationIssue)
    assert isinstance(issue, Warning)
    assert isinstance(issue, ResolutionException)
    assert issue.goal == goal
    assert issue.cause is None
    assert issue.context == context
    assert issue.message == "Error while solving initialization goal init(x): failure"


def test_initialization_issue_with_cause(context):
    goal = struct("init", atom("x"))
    cause = syntax_error(context, "bad")
    issue = initialization_issue(goal, context, cause)
    assert issue.cause == cause
    assert issue.message == (
        "Error while solving initialization goal init(x): error(syntax_error, 'Syntax error: bad')"
    )


def test_initialization_issue_contexts(context):
    issue = initialization_issue(struct("init", atom("x")), context)
    pushed = issue.push_context(context)
    assert isinstance(pushed, InitializationIssue)
    assert len(pushed.contexts) == 2
    assert isinstance(issue.update_last_context(context), InitializationIssue)


def test_missing_predicate(context, procedure):
    warning = missing_predicate(procedure, context)
    assert isinstance(warning, MissingPredicate)
    assert isinstance(warning, Warning)
    assert warning.signature == procedure
    assert warning.cause is None
    assert warning.message == "No such a predicate: foo/2"


def test_missing_predicate_with_cause(context, procedure):
    cause = syntax_error(context, "bad")
    warning = missing_predicate(procedure, context, cause)
    assert warning.cause == cause
    assert isinstance(warning.push_context(context), MissingPredicate)
