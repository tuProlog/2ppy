import pytest

from tuprolog.core import atom, real, struct
from tuprolog.core.operators import DEFAULT_OPERATORS, operator, specifier
from tuprolog.core.parsing import ParseException, parse_struct
from tuprolog.solve import MutableSolver, Solver, SolverFactory
from tuprolog.solve.channel import output_channel
from tuprolog.solve.flags import DEFAULT_FLAG_STORE, Unknown
from tuprolog.solve.library import library
from tuprolog.solve.plp import probability, solve_options
from tuprolog.solve.problog import (
    ANNOTATION_OPERATOR,
    PROBLOG_OPERATORS,
    PROBLOG_SOLVER_FACTORY,
    PROBLOG_SPECIFIC_OPERATORS,
    Operators,
    problog_solver,
)
from tuprolog.theory import mutable_theory
from tuprolog.theory.parsing import parse_theory

PROBABILISTIC = solve_options(probabilistic=True)

COINS = """
0.6::heads(c1).
0.3::heads(c2).
both :- heads(c1), heads(c2).
some :- heads(c1).
some :- heads(c2).
none :- \\+ heads(c1), \\+ heads(c2).
"""


def problog_theory(text):
    return parse_theory(text, PROBLOG_OPERATORS)


def probabilities(solver, goal, options=PROBABILISTIC):
    return [
        (str(s.solved_query), round(float(probability(s)), 10))
        for s in solver.solve(parse_struct(goal), options)
        if s.is_yes
    ]


@pytest.fixture
def coins():
    return problog_solver(static_kb=problog_theory(COINS))


def test_definitions():
    assert isinstance(PROBLOG_SOLVER_FACTORY, SolverFactory)
    assert ANNOTATION_OPERATOR == operator("::", specifier("xfy"), 900)
    assert ANNOTATION_OPERATOR == Operators.ANNOTATION_OPERATOR
    assert list(PROBLOG_SPECIFIC_OPERATORS) == [ANNOTATION_OPERATOR]
    assert PROBLOG_OPERATORS == DEFAULT_OPERATORS.plus(PROBLOG_SPECIFIC_OPERATORS)


def test_annotations_need_problog_operators():
    with pytest.raises(ParseException):
        parse_theory("0.5::a.")
    (clause,) = problog_theory("0.5::a.")
    assert clause.head == struct("::", real(0.5), atom("a"))


def test_problog_solver_is_mutable_by_default():
    assert isinstance(problog_solver(), MutableSolver)


def test_problog_solver_immutable():
    solver = problog_solver(mutable=False)
    assert isinstance(solver, Solver)
    assert not isinstance(solver, MutableSolver)


def test_problog_solver_has_problog_builtins():
    solver = problog_solver()
    aliases = {str(alias) for alias in solver.libraries.keySet()}
    assert "problog.lang" in aliases
    assert ANNOTATION_OPERATOR in solver.operators


@pytest.mark.parametrize(
    "goal, expected",
    [
        ("heads(c1)", 0.6),
        ("heads(c2)", 0.3),
        ("both", 0.18),
        ("some", 0.72),
        ("none", 0.28),
    ],
)
def test_ground_query_probabilities(coins, goal, expected):
    assert probabilities(coins, goal) == [(goal, expected)]


def test_non_ground_query_probabilities(coins):
    assert probabilities(coins, "heads(X)") == [("heads(c1)", 0.6), ("heads(c2)", 0.3)]


def test_solve_once_probabilistic(coins):
    assert probability(coins.solve_once(atom("both"), PROBABILISTIC)) == pytest.approx(0.18)


def test_non_probabilistic_solving_has_default_probability(coins):
    assert probabilities(coins, "both", solve_options()) == [("both", 1.0)]
    assert [probability(s) for s in coins.solve(atom("both"))] == [1.0]


def test_eager_probabilistic_solving(coins):
    options = solve_options(lazy=False, probabilistic=True)
    assert probabilities(coins, "some", options) == [("some", 0.72)]


def test_probabilistic_rules():
    solver = problog_solver(
        static_kb=problog_theory(
            """
            0.5::coin(heads). 0.5::coin(tails).
            0.2::lucky(X) :- coin(X).
            """
        )
    )
    assert probabilities(solver, "lucky(X)") == [("lucky(heads)", 0.1), ("lucky(tails)", 0.1)]


def test_evidence_conditions_probabilities():
    solver = problog_solver(
        static_kb=problog_theory(
            """
            0.4::rain. 0.7::sprinkler.
            wet :- rain. wet :- sprinkler.
            evidence(wet, true).
            """
        )
    )
    # P(rain | wet) = 0.4 / (1 - 0.6 * 0.3)
    assert probabilities(solver, "rain") == [("rain", round(0.4 / 0.82, 10))]


def test_paths_in_probabilistic_graph():
    solver = problog_solver(
        static_kb=problog_theory(
            """
            0.6::edge(1,2). 0.1::edge(1,3). 0.4::edge(2,5). 0.3::edge(2,6).
            0.3::edge(3,4). 0.8::edge(4,5). 0.2::edge(5,6).
            path(X,Y) :- edge(X,Y).
            path(X,Y) :- edge(X,Z), Y \\== Z, path(Z,Y).
            """
        )
    )
    assert probabilities(solver, "path(1, 6)") == [("path(1, 6)", 0.2167296)]


def test_dynamic_kb_and_flags():
    warnings = []
    solver = problog_solver(
        dynamic_kb=mutable_theory(*problog_theory("0.5::d.")),
        flags=DEFAULT_FLAG_STORE.set(Unknown, Unknown.FAIL),
        warning=output_channel(warnings.append),
    )
    assert probabilities(solver, "d") == [("d", 0.5)]
    assert str(solver.flags[Unknown]) == "fail"
    assert probabilities(solver, "missing", solve_options()) == []
    assert warnings == []


def test_libraries_argument():
    solver = problog_solver(libraries=library("my.lib"))
    assert "my.lib" in {str(alias) for alias in solver.libraries.keySet()}


def test_errors_are_reported_as_halt(coins):
    solution = coins.solve_once(parse_struct("X is foo + 1"), PROBABILISTIC)
    assert solution.is_halt
    assert "type_error" in str(solution.get_exception().error_struct)


def test_negated_query(coins):
    assert probabilities(coins, "\\+ both") == [("'\\\\+'(both)", 0.82)]
