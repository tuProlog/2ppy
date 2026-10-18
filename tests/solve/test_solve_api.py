import time

import pytest

import tuprolog.solve as solve_module
from tuprolog.core import (
    EMPTY_UNIFIER,
    atom,
    indicator,
    integer,
    pretty_variables_formatter,
    struct,
    substitution,
    var,
)
from tuprolog.core.parsing import parse_struct
from tuprolog.solve import (
    ALL_SOLUTIONS,
    MAX_TIMEOUT,
    Durable,
    ExecutionContext,
    ExecutionContextAware,
    MutableSolver,
    Signature,
    Solution,
    SolutionFormatter,
    SolveOptions,
    Solver,
    SolverBuilder,
    SolverFactory,
    Time,
    current_time_instant,
    halt_solution,
    no_solution,
    signature,
    solution_formatter,
    solve_options,
    yes_solution,
)
from tuprolog.solve.exception import ResolutionException
from tuprolog.solve.prolog import prolog_solver


@pytest.fixture(scope="module")
def resolution_error():
    halt = prolog_solver().solve_once(parse_struct("X is foo + 1"))
    return halt.getException()


@pytest.mark.parametrize(
    "jvm_type, name",
    [
        (Durable, "Durable"),
        (ExecutionContext, "ExecutionContext"),
        (ExecutionContextAware, "ExecutionContextAware"),
        (MutableSolver, "MutableSolver"),
        (Signature, "Signature"),
        (Solution, "Solution"),
        (SolutionFormatter, "SolutionFormatter"),
        (SolveOptions, "SolveOptions"),
        (Solver, "Solver"),
        (SolverBuilder, "SolverBuilder"),
        (SolverFactory, "SolverFactory"),
        (Time, "Time"),
    ],
)
def test_definitions_are_jvm_types(jvm_type, name):
    assert jvm_type.class_.getName() == f"it.unibo.tuprolog.solve.{name}"


def test_constants():
    assert MAX_TIMEOUT == 2**63 - 1
    assert ALL_SOLUTIONS == -1


def test_solver_hierarchy():
    assert issubclass(MutableSolver, Solver)
    assert issubclass(Solver, ExecutionContextAware)


def test_public_api_is_exported():
    for name in (
        "signature",
        "yes_solution",
        "no_solution",
        "halt_solution",
        "current_time_instant",
        "solution_formatter",
        "solve_options",
    ):
        assert callable(getattr(solve_module, name))


# --- signature ---------------------------------------------------------------------------------


def test_signature_from_name_and_arity():
    sig = signature("f", 2)
    assert isinstance(sig, Signature)
    assert sig.name == "f"
    assert sig.arity == 2
    assert sig.vararg is False


def test_signature_vararg():
    assert signature("f", 2, True).vararg is True
    assert signature("f", 2, vararg=True) == signature("f", 2, True)


def test_signature_keyword_arity():
    assert signature("f", arity=1) == signature("f", 1)


def test_signature_all_keyword_arguments():
    assert signature(name="f", arity=1) == signature("f", 1)


def test_signature_equality_and_hash():
    assert signature("f", 2) == signature("f", 2)
    assert signature("f", 2) != signature("f", 3)
    assert signature("f", 2) != signature("f", 2, True)
    assert hash(signature("f", 2)) == hash(signature("f", 2))
    assert {signature("f", 2): 1}[signature("f", 2)] == 1


def test_signature_from_indicator():
    assert signature(indicator("f", 2)) == signature("f", 2)


def test_signature_from_signature_term():
    assert signature(struct("/", atom("f"), integer(2))) == signature("f", 2)


def test_signature_from_vararg_signature_term():
    term = struct("/", atom("f"), struct("+", integer(2), atom("vararg")))
    assert signature(term) == signature("f", 2, True)


@pytest.mark.parametrize(
    "term",
    [
        pytest.param(atom("f"), id="atom"),
        pytest.param(integer(2), id="number"),
        pytest.param(indicator(var("X"), integer(2)), id="non-ground-indicator"),
    ],
)
def test_signature_from_invalid_terms_is_none(term):
    assert signature(term) is None


def test_signature_round_trips():
    sig = signature("f", 2)
    assert sig.to_indicator() == indicator("f", 2)
    assert signature(sig.to_indicator()) == sig
    assert signature(sig.to_term()) == sig
    vararg = signature("f", 2, True)
    assert signature(vararg.to_term()) == vararg


def test_signature_with_args():
    assert signature("f", 2).with_args([atom("a"), atom("b")]) == struct("f", atom("a"), atom("b"))


def test_signature_str():
    assert str(signature("f", 2)) == "Signature(name=f, arity=2, vararg=false)"


# --- solutions ---------------------------------------------------------------------------------


def test_yes_solution_from_signature():
    sol = yes_solution(signature("f", 1), [atom("a")])
    assert isinstance(sol, Solution.Yes)
    assert sol.is_yes
    assert sol.query == struct("f", atom("a"))
    assert sol.solved_query == struct("f", atom("a"))
    assert sol.substitution.is_empty


def test_yes_solution_from_signature_accepts_any_iterable():
    sol = yes_solution(signature("f", 2), (t for t in [atom("a"), atom("b")]))
    assert sol.query == struct("f", atom("a"), atom("b"))


def test_yes_solution_from_signature_with_substitution():
    x = var("X")
    sol = yes_solution(signature("f", 1), [x], substitution({x: atom("a")}))
    assert sol.query == struct("f", x)
    assert sol.solved_query == struct("f", atom("a"))
    assert sol.substitution[x] == atom("a")


def test_yes_solution_from_query():
    sol = yes_solution(struct("f", atom("a")))
    assert isinstance(sol, Solution.Yes)
    assert sol.substitution == EMPTY_UNIFIER


def test_yes_solution_from_query_with_substitution():
    x = var("X")
    sol = yes_solution(struct("f", x), substitution({x: atom("a")}))
    assert sol.solved_query == struct("f", atom("a"))
    assert sol.value_of(x) == atom("a")


def test_no_solution_from_signature():
    sol = no_solution(signature("f", 1), [atom("a")])
    assert isinstance(sol, Solution.No)
    assert sol.is_no
    assert not sol.is_yes
    assert sol.query == struct("f", atom("a"))
    assert sol.solved_query is None
    assert sol.substitution.is_failed


def test_no_solution_from_query():
    sol = no_solution(struct("f", atom("a")))
    assert isinstance(sol, Solution.No)
    assert sol.query == struct("f", atom("a"))


def test_halt_solution_from_signature(resolution_error):
    sol = halt_solution(signature("f", 1), [atom("a")], resolution_error)
    assert isinstance(sol, Solution.Halt)
    assert sol.is_halt
    assert sol.query == struct("f", atom("a"))
    assert sol.getException() == resolution_error


def test_halt_solution_from_query(resolution_error):
    sol = halt_solution(struct("f", atom("a")), resolution_error)
    assert isinstance(sol, Solution.Halt)
    assert sol.get_exception() == resolution_error
    assert isinstance(sol.get_exception(), ResolutionException)


def test_solution_factories_reject_wrong_arity():
    with pytest.raises(Exception):  # noqa: B017 - JVM-side IllegalArgumentException
        yes_solution(signature("f", 2), [atom("a")])


# --- current_time_instant ----------------------------------------------------------------------


def test_current_time_instant_is_epoch_millis():
    before = int(time.time() * 1000)
    now = current_time_instant()
    after = int(time.time() * 1000)
    assert before - 1000 <= now <= after + 1000


def test_current_time_instant_is_monotonic_enough():
    assert current_time_instant() <= current_time_instant()


# --- solution_formatter ------------------------------------------------------------------------


@pytest.fixture(scope="module")
def solver():
    from tuprolog.theory.parsing import parse_theory

    return prolog_solver(static_kb=parse_theory("p(1). p(2). q(a + b)."))


def test_solution_formatter_default(solver):
    fmt = solution_formatter()
    assert isinstance(fmt, SolutionFormatter)
    yes = solver.solve_once(struct("p", var("X")))
    assert fmt.format(yes) == "yes: p(1)\n    X = 1"


def test_solution_formatter_pretty_prints_expressions(solver):
    yes = solver.solve_once(struct("q", var("X")))
    assert solution_formatter().format(yes) == "yes: q(a + b)\n    X = a + b"


def test_solution_formatter_no(solver):
    no = solver.solve_once(struct("p", integer(3)))
    assert solution_formatter().format(no) == "no."


def test_solution_formatter_halt(solver):
    halt = solver.solve_once(parse_struct("X is foo + 1"))
    text = str(solution_formatter().format(halt))
    assert text.startswith("halt: The 1-th argument of `is/2` should be a `evaluable`")


def test_solution_formatter_with_custom_term_formatter(solver):
    yes = solver.solve_once(struct("q", var("X")))
    fmt = solution_formatter(pretty_variables_formatter())
    assert fmt.format(yes) == "yes: q('+'(a, b))\n    X = '+'(a, b)"


# --- solve_options -----------------------------------------------------------------------------


def test_solve_options_defaults():
    opts = solve_options()
    assert isinstance(opts, SolveOptions)
    assert opts.is_lazy is True
    assert opts.is_eager is False
    assert opts.timeout == MAX_TIMEOUT
    assert opts.limit == ALL_SOLUTIONS
    assert not opts.is_limited
    assert len(opts.options) == 0


def test_solve_options_explicit():
    opts = solve_options(lazy=False, timeout=100, limit=3)
    assert opts.is_lazy is False
    assert opts.is_eager is True
    assert opts.timeout == 100
    assert opts.limit == 3
    assert opts.is_limited


def test_solve_options_custom_mapping_and_kwargs():
    opts = solve_options(custom={"a": 1}, b="x")
    assert opts.options["a"] == 1
    assert opts.options["b"] == "x"
    assert set(map(str, opts.options.keySet())) == {"a", "b"}


def test_solve_options_equality():
    assert solve_options() == solve_options()
    assert solve_options(limit=1) != solve_options()
    assert solve_options(custom={"a": 1}) == solve_options(a=1)


def test_solve_options_are_immutable_values():
    opts = solve_options()
    changed = opts.set_limit(2).set_lazy(False).set_timeout(5)
    assert (changed.limit, changed.is_lazy, changed.timeout) == (2, False, 5)
    assert (opts.limit, opts.is_lazy, opts.timeout) == (ALL_SOLUTIONS, True, MAX_TIMEOUT)


def test_signature_requires_an_arity_unless_from_a_term():
    with pytest.raises(TypeError):
        signature("f")
    with pytest.raises(TypeError):
        signature(struct("/", atom("f"), integer(1)), 1)
