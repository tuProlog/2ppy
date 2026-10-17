import pytest

from tuprolog.core import Substitution, atom, integer, struct, var
from tuprolog.core.parsing import parse_struct
from tuprolog.solve import ExecutionContext, Solution, solution_formatter
from tuprolog.solve.exception import ResolutionException
from tuprolog.solve.prolog import prolog_solver
from tuprolog.theory.parsing import parse_theory

X = var("X")


@pytest.fixture(scope="module")
def solver():
    return prolog_solver(
        static_kb=parse_theory(
            """
            p(1). p(2). p(3).
            color(red). color(green).
            colorful(C) :- color(C).
            """
        ),
        mutable=False,
    )


@pytest.fixture(scope="module")
def yes(solver):
    return solver.solve_once(struct("p", X))


@pytest.fixture(scope="module")
def no(solver):
    return solver.solve_once(struct("p", integer(4)))


@pytest.fixture(scope="module")
def halt(solver):
    return solver.solve_once(parse_struct("X is foo + 1"))


def test_yes_solution(yes):
    assert isinstance(yes, Solution.Yes)
    assert (yes.is_yes, yes.is_no, yes.is_halt) == (True, False, False)
    assert yes.query == struct("p", X)
    assert yes.solved_query == struct("p", integer(1))
    assert isinstance(yes.substitution, Substitution.Unifier)
    assert yes.substitution[X] == integer(1)
    assert yes.exception is None


def test_no_solution(no):
    assert isinstance(no, Solution.No)
    assert (no.is_yes, no.is_no, no.is_halt) == (False, True, False)
    assert no.query == struct("p", integer(4))
    assert no.solved_query is None
    assert no.substitution.is_failed
    assert no.exception is None


def test_halt_solution(halt):
    assert isinstance(halt, Solution.Halt)
    assert (halt.is_yes, halt.is_no, halt.is_halt) == (False, False, True)
    assert halt.solved_query is None
    assert halt.substitution.is_failed


def test_halt_exception_via_java_getter(halt):
    exception = halt.get_exception()
    assert isinstance(exception, ResolutionException)
    assert str(exception.message).startswith("The 1-th argument of `is/2` should be a `evaluable`")
    assert isinstance(exception.context, ExecutionContext)


def test_halt_exception_property(halt):
    assert halt.exception == halt.get_exception()


def test_value_of(yes):
    assert yes.value_of(X) == integer(1)
    assert yes.value_of("X") == integer(1)
    assert yes.value_of(var("Y")) is None


def test_casts(yes, no, halt):
    assert yes.as_yes() == yes
    assert yes.as_no() is None
    assert yes.as_halt() is None
    assert no.as_no() == no
    assert halt.as_halt() == halt
    assert yes.cast_to_yes() == yes
    with pytest.raises(Exception, match="Cannot cast"):
        yes.cast_to_no()
    with pytest.raises(Exception, match="Cannot cast"):
        no.cast_to_halt()


def test_solutions_are_values(solver, yes):
    assert solver.solve_once(struct("p", X)) == yes
    assert hash(solver.solve_once(struct("p", X))) == hash(yes)


def test_solution_str(yes, no):
    assert str(yes).startswith("Yes(query=p(X_")
    assert str(no) == "No(query=p(4))"


def test_solution_tags(yes):
    assert len(yes.tags) == 0
    tagged = yes.replace_tags({"key": "value"})
    assert tagged.contains_tag("key")
    assert tagged.tags["key"] == "value"
    assert not yes.contains_tag("key")


# --- solution sequences ------------------------------------------------------------------------


def test_iteration_ends_with_last_yes_when_no_choice_points_are_left(solver):
    solutions = list(solver.solve(struct("p", X)))
    assert [s.is_yes for s in solutions] == [True, True, True]


def test_iteration_ends_with_no_when_choice_points_remain(solver):
    solutions = list(solver.solve(parse_struct("member(X, [a, b])")))
    assert [s.is_yes for s in solutions] == [True, True, False]
    last = solutions[-1]
    assert last.is_no
    assert last.solved_query is None


def test_iteration_through_rules(solver):
    solutions = [s for s in solver.solve(struct("colorful", X)) if s.is_yes]
    assert [str(s.substitution[X]) for s in solutions] == ["red", "green"]


def test_failing_goal_yields_a_single_no(solver):
    solutions = list(solver.solve(atom("fail")))
    assert len(solutions) == 1
    assert solutions[0].is_no


def test_error_yields_a_single_halt(solver):
    solutions = list(solver.solve(parse_struct("atom_length(X, Y)")))
    assert len(solutions) == 1
    assert solutions[0].is_halt
    assert "instantiation_error" in str(solutions[0].get_exception().error_struct)


def test_solutions_after_halt_are_not_produced(solver):
    solutions = list(solver.solve(parse_struct("(X = 1 ; X = foo), Y is X + 1")))
    assert [s.is_yes for s in solutions] == [True, False]
    assert solutions[-1].is_halt


# --- formatting --------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "goal, expected",
    [
        ("p(X)", "yes: p(1)\n    X = 1"),
        ("X = f(Y), Y = 2", "yes: f(2) = f(2), 2 = 2\n    X = f(2)\n    Y = 2"),
        ("p(4)", "no."),
        ("p(1)", "yes: p(1)\n    "),
    ],
)
def test_formatted_solutions(solver, goal, expected):
    assert solution_formatter().format(solver.solve_once(parse_struct(goal))) == expected


def test_formatted_halt(solver):
    text = str(solution_formatter().format(solver.solve_once(parse_struct("atom_length(X, Y)"))))
    assert text.startswith("halt: ")
    assert "atom_length" in text
