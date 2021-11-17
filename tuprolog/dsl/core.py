from functools import singledispatch
from typing import Callable

from tuprolog import logger
from tuprolog.core import Term
from tuprolog.core.operators import OperatorSet
from tuprolog.core.parsing import parse_term


def _logic_with_operators(operators: OperatorSet = None):
    def wrapper(func):
        def create_string(*args, **kwargs):
            return logic_programming(operators) @ func(*args, **kwargs)
        return create_string
    return wrapper


# noinspection PyPep8Naming
class logic_programming:
    def __init__(self, operators: OperatorSet = None):
        self._operators = operators

    def _parse(self, string: str) -> Term:
        return parse_term(string, self._operators)

    def __or__(self, other: str) -> Term:
        return self._parse(other)

    def __matmul__(self, other: str) -> Term:
        return self._parse(other)

    def __gt__(self, other: str) -> Term:
        return self._parse(other)

    def __call__(self, func):
        return _logic_with_operators(self._operators)(func)


lp = logic_programming()


def logic(operators=None):
    if operators is None or isinstance(operators, OperatorSet):
        return _logic_with_operators(operators)
    else:
        return _logic_with_operators()(operators)


logger.debug("Configure Python DSL adapters for types in it.unibo.tuprolog.core.*")
