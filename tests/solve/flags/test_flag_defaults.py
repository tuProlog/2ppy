"""Default values of the notable flags 2P-Kt 3.x introduced, and their effect on solving."""

from tuprolog.core.parsing import parse_struct
from tuprolog.solve.flags import (
    DEFAULT_FLAG_STORE,
    GroundQueriesHaveBooleanSolution,
    ShowWildCardVariablesInSolutions,
    UniqueSolutions,
)
from tuprolog.solve.prolog import prolog_solver
from tuprolog.theory.parsing import parse_theory


def test_defaults():
    assert DEFAULT_FLAG_STORE[UniqueSolutions] == UniqueSolutions.OFF
    assert (
        DEFAULT_FLAG_STORE[ShowWildCardVariablesInSolutions] == ShowWildCardVariablesInSolutions.ON
    )
    assert (
        DEFAULT_FLAG_STORE[GroundQueriesHaveBooleanSolution] == GroundQueriesHaveBooleanSolution.OFF
    )


def _solutions(flags):
    solver = prolog_solver(flags=flags, static_kb=parse_theory("p(a). p(a). p(b)."))
    return [
        str(s.substitution.getByName("X")) for s in solver.solve(parse_struct("p(X)")) if s.is_yes
    ]


def test_unique_solutions_drops_duplicates():
    assert _solutions(DEFAULT_FLAG_STORE) == ["a", "a", "b"]
    assert _solutions(DEFAULT_FLAG_STORE.set(UniqueSolutions, UniqueSolutions.ON)) == ["a", "b"]
