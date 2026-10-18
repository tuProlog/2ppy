from tuprolog.core import atom, struct
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error import SyntaxError, SystemError, syntax_error
from tuprolog.solve.exception.error.message import MessageError, message_error

from .helpers import solve_once, solver_raising


def test_message_error(context):
    content = struct("hello", atom("world"))
    error = message_error(content, context)
    assert isinstance(error, MessageError)
    assert isinstance(error, LogicError)
    assert error.content == content
    assert error.extra_data == content
    assert error.message == "hello(world)"
    assert error.cause is None
    assert error.error_struct == struct("error", atom(""), content)


def test_message_error_with_cause(context):
    cause = syntax_error(context, "bad")
    error = message_error(atom("hi"), context, cause)
    assert error.cause == cause
    assert isinstance(error.cause, SyntaxError)


def test_message_error_raised_from_primitive():
    solver = solver_raising(msg=lambda r: message_error(atom("hi"), r.context))
    solution = solve_once(solver, "msg")
    assert solution.is_halt
    # as for throw(hi), 2P-Kt reports an uncaught message as a system error
    exception = solution.getException()
    assert isinstance(exception, SystemError)
    assert isinstance(exception.cause, MessageError)
    assert exception.message == "Uncaught exception `hi`"
    caught = solve_once(solver, "catch(msg, M, true)")
    assert caught.substitution.getByName("M") == atom("hi")
