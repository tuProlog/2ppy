import pytest

from tuprolog.core import atom, struct
from tuprolog.solve import ALL_SOLUTIONS, MAX_TIMEOUT, SolveOptions, plp, yes_solution
from tuprolog.solve import solve_options as base_solve_options
from tuprolog.solve.plp import (
    ProbExtensions,
    is_probabilistic,
    probabilistic,
    probability,
    set_probabilistic,
    set_probability,
    solve_options,
)
from tuprolog.theory import theory

PROBABILISTIC_OPTION = "it.unibo.tuprolog.solve.options.probabilistic"


def test_prob_extensions_is_the_jvm_facade():
    assert ProbExtensions.class_.getName() == "it.unibo.tuprolog.solve.ProbExtensions"
    assert ProbExtensions.DEFAULT_PROBABILITY == 1.0
    assert ProbExtensions.DEFAULT_PROBABILISTIC_OPTION is False


@pytest.mark.parametrize(
    "taggable",
    [
        pytest.param(
            lambda: yes_solution(struct("f", atom("a"))),  # type: ignore[call-arg]
            id="solution",
        ),
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


def test_is_probabilistic_defaults_to_false():
    assert is_probabilistic(base_solve_options()) is False
    assert is_probabilistic(SolveOptions.allLazily()) is False


def test_set_probabilistic():
    opts = set_probabilistic(base_solve_options(), True)
    assert is_probabilistic(opts) is True
    assert bool(opts.options[PROBABILISTIC_OPTION])
    assert is_probabilistic(set_probabilistic(opts, False)) is False


def test_probabilistic():
    assert is_probabilistic(probabilistic(base_solve_options())) is True


def test_probabilistic_keeps_other_options():
    opts = probabilistic(base_solve_options(lazy=False, timeout=5, limit=2, custom={"k": "v"}))
    assert (opts.is_lazy, opts.timeout, opts.limit) == (False, 5, 2)
    assert opts.options["k"] == "v"
    assert bool(opts.options[PROBABILISTIC_OPTION])


def test_probabilistic_options_are_mapping_entries():
    opts = solve_options(probabilistic=True)
    assert PROBABILISTIC_OPTION in opts
    assert bool(opts[PROBABILISTIC_OPTION])


def test_solve_options_defaults():
    opts = solve_options()
    assert isinstance(opts, SolveOptions)
    assert opts.is_lazy is True
    assert opts.timeout == MAX_TIMEOUT
    assert opts.limit == ALL_SOLUTIONS
    assert is_probabilistic(opts) is False
    assert len(opts.options) == 0


def test_solve_options_probabilistic():
    opts = solve_options(lazy=False, timeout=7, limit=3, probabilistic=True, custom={"k": 1}, j=2)
    assert (opts.is_lazy, opts.timeout, opts.limit) == (False, 7, 3)
    assert is_probabilistic(opts) is True
    assert opts.options["k"] == 1
    assert opts.options["j"] == 2


def test_solve_options_explicitly_non_probabilistic():
    assert is_probabilistic(solve_options(probabilistic=False)) is False
    assert solve_options(probabilistic=False) == base_solve_options()


@pytest.mark.xfail(
    strict=True,
    reason="the binary decision diagram helpers of ProbExtensions "
    "(hasBinaryDecisionDiagram, binaryDecisionDiagram, setBinaryDecisionDiagram) are not wrapped",
)
def test_binary_decision_diagram_helpers_are_wrapped():
    for name in (
        "has_binary_decision_diagram",
        "binary_decision_diagram",
        "set_binary_decision_diagram",
    ):
        assert callable(getattr(plp, name))
