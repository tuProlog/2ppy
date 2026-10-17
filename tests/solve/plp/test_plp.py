import pytest

from tuprolog.core import atom, struct
from tuprolog.solve import yes_solution
from tuprolog.solve.plp import (
    probability,
    set_probability,
)
from tuprolog.theory import theory

PROBABILISTIC_OPTION = "it.unibo.tuprolog.solve.options.probabilistic"


@pytest.mark.parametrize(
    "taggable",
    [
        pytest.param(lambda: yes_solution(struct("f", atom("a"))), id="solution"),
        pytest.param(lambda: theory(), id="theory"),
        pytest.param(lambda: atom("a"), id="term"),
    ],
)
def test_default_probability_is_one(taggable):
    assert probability(taggable()) == 1.0


def test_set_probability_returns_a_tagged_copy():
    solution = yes_solution(struct("f", atom("a")))
    tagged = set_probability(solution, 0.25)
    assert probability(tagged) == 0.25
    assert probability(solution) == 1.0
    assert tagged.query == solution.query


@pytest.mark.parametrize("value, expected", [(-1.0, 0.0), (0.0, 0.0), (1.0, 1.0), (3.5, 1.0)])
def test_set_probability_clamps_into_unit_interval(value, expected):
    assert probability(set_probability(atom("a"), value)) == expected


def test_set_probability_accepts_python_ints():
    assert probability(set_probability(atom("a"), 0)) == 0.0


