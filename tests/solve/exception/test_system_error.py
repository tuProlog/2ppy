from jpype import JClass

from tuprolog.core import atom, struct
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error import SyntaxError, syntax_error
from tuprolog.solve.exception.error.system import SystemError, system_error

from .helpers import solve_once, solver_raising


def test_system_error_is_the_logic_one():
    assert SystemError is not SyntaxError
    assert SystemError.class_.getName() == "it.unibo.tuprolog.solve.exception.error.SystemError"
    assert issubclass(SystemError, LogicError)


def test_system_error_for_uncaught_logic_error(context):
    cause = syntax_error(context, "bad")
    error = system_error(context, cause)
    assert isinstance(error, SystemError)
    assert error.cause == cause
    assert error.message == "Uncaught exception `error(syntax_error, 'Syntax error: bad')`"
    assert error.getType() == atom("system_error")
    assert error.error_struct == struct("error", atom("system_error"), atom(error.message))


def test_system_error_for_uncaught_term(context):
    error = system_error(context, struct("oops", atom("x")))
    assert isinstance(error, SystemError)
    assert error.cause is None
    assert error.message == "Uncaught exception `oops(x)`"


def test_system_error_for_uncaught_throwable(context):
    error = system_error(context, JClass("java.lang.IllegalStateException")("boom"))
    assert isinstance(error, SystemError)
    assert error.message == "Uncaught exception `IllegalStateException: boom`"


def test_system_error_raised_from_primitive_is_catchable():
    solver = solver_raising(sys=lambda r: system_error(r.context, atom("oops")))
    assert isinstance(solve_once(solver, "sys").getException(), SystemError)
    caught = solve_once(solver, "catch(sys, error(system_error, M), true)")
    assert caught.substitution.getByName("M") == atom("Uncaught exception `oops`")
