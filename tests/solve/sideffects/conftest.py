from collections.abc import Callable

import pytest

from tests.solve.primitive._support import single_primitive_library
from tuprolog.solve import Solver
from tuprolog.solve.prolog import prolog_solver
from tuprolog.solve.sideffects import SideEffect

EMIT = "emit"


def emitting_solver(*side_effects: SideEffect, **kwargs) -> Solver:
    """A solver where `emit/0` succeeds once, emitting the given side effects."""

    def implementation(request):
        yield request.reply_success(None, *side_effects)

    library = single_primitive_library(EMIT, 0, implementation, alias="test.emit")
    return prolog_solver(libraries=library, **kwargs)


@pytest.fixture
def emitting() -> Callable[..., Solver]:
    return emitting_solver
