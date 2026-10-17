from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error import SyntaxError
from tuprolog.solve.exception.error.system import SystemError


def test_system_error_is_the_logic_one():
    assert SystemError is not SyntaxError
    assert SystemError.class_.getName() == "it.unibo.tuprolog.solve.exception.error.SystemError"
    assert issubclass(SystemError, LogicError)
