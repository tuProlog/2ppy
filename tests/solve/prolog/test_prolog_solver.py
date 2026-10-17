import pytest

import tuprolog.solve.prolog as prolog_module
from tuprolog.core import atom, integer, struct, var
from tuprolog.core.operators import DEFAULT_OPERATORS, operator, operator_set, specifier
from tuprolog.core.parsing import parse_struct
from tuprolog.solve import MutableSolver, Solver, SolverFactory, solve_options
from tuprolog.solve.channel import input_channel, output_channel
from tuprolog.solve.flags import DEFAULT_FLAG_STORE, Unknown, flag_store
from tuprolog.solve.library import library
from tuprolog.solve.prolog import PROLOG_SOLVER_FACTORY, prolog_solver
from tuprolog.theory import mutable_theory, theory
from tuprolog.theory.parsing import parse_theory

PROGRAM = """
parent(abraham, isaac). parent(isaac, jacob). parent(jacob, joseph).
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

first_parent(X, Y) :- parent(X, Y), !.
max(X, Y, X) :- X >= Y, !.
max(_, Y, Y).

len([], 0).
len([_ | T], N) :- len(T, M), N is M + 1.

orphan(X) :- \\+ parent(_, X).

safe_div(X, Y, Z) :- catch(Z is X / Y, error(E, _), Z = error(E)).
fails_with(T) :- throw(my_error(T)).

loop :- loop.
"""


def answers(solver, goal, variable="X", options=None):
    sols = (
        solver.solve(parse_struct(goal))
        if options is None
        else solver.solve(parse_struct(goal), options)
    )
    return [str(s.value_of(variable)) for s in sols if s.is_yes]


def once(solver, goal):
    return solver.solve_once(parse_struct(goal))


@pytest.fixture
def solver():
    return prolog_solver(static_kb=parse_theory(PROGRAM))


def test_module_exports():
    assert prolog_module.prolog_solver is prolog_solver
    assert prolog_module.PROLOG_SOLVER_FACTORY is PROLOG_SOLVER_FACTORY
    assert isinstance(PROLOG_SOLVER_FACTORY, SolverFactory)


def test_factory_defaults():
    solver = prolog_solver()
    assert isinstance(solver, MutableSolver)
    assert len(solver.static_kb) == 0
    assert len(solver.dynamic_kb) == 0
    assert "prolog.lang" in {str(a) for a in solver.libraries.keySet()}
    assert solver.flags == DEFAULT_FLAG_STORE


def test_immutable_factory():
    solver = prolog_solver(mutable=False)
    assert isinstance(solver, Solver)
    assert not isinstance(solver, MutableSolver)


def test_backtracking(solver):
    assert answers(solver, "ancestor(abraham, X)") == ["isaac", "jacob", "joseph"]
    assert answers(solver, "ancestor(X, joseph)") == ["jacob", "abraham", "isaac"]


def test_conjunction_and_disjunction(solver):
    assert answers(solver, "(X = 1 ; X = 2 ; X = 3), X > 1") == ["2", "3"]


def test_cut(solver):
    assert answers(solver, "first_parent(X, _)") == ["abraham"]
    assert answers(solver, "max(3, 2, X)") == ["3"]
    assert answers(solver, "max(2, 3, X)") == ["3"]
    assert answers(solver, "member(X, [a, b, c]), !") == ["a"]


def test_if_then_else(solver):
    assert answers(solver, "(1 < 2 -> X = yes ; X = no)") == ["yes"]
    assert answers(solver, "(2 < 1 -> X = yes ; X = no)") == ["no"]


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("1 + 2 * 3", "7"),
        ("7 // 2", "3"),
        ("7 mod 3", "1"),
        ("2 ** 3", "8.0"),
        ("-(3)", "-3"),
        ("abs(-4)", "4"),
        ("max(2, 5)", None),
        ("7 / 2", "3.5"),
        pytest.param(
            "2 ** -1",
            "0.5",
            marks=pytest.mark.xfail(
                strict=True,
                reason="2P-Kt 0.31.16: 'X is 2 ** -1' leaks a raw java.lang.ArithmeticException "
                "out of solve instead of yielding 0.5 (or at least a Halt solution)",
            ),
        ),
        ("sqrt(16)", "4.0"),
        ("12345678901234567890 * 10", "123456789012345678900"),
    ],
)
def test_arithmetic(solver, expression, expected):
    solution = once(solver, f"X is {expression}")
    if expected is None:
        assert solution.is_halt
    else:
        assert str(solution.value_of("X")) == expected


def test_arithmetic_comparison(solver):
    assert once(solver, "1 + 1 =:= 2").is_yes
    assert once(solver, "1 + 1 =\\= 2").is_no
    assert once(solver, "3 >= 3").is_yes


def test_lists(solver):
    assert answers(solver, "append(X, [c], [a, b, c])") == ["[a, b]"]
    assert answers(solver, "len([a, b, c], X)") == ["3"]
    assert len(answers(solver, "append(X, _, [a, b])")) == 3
    assert answers(solver, "member(X, [1, 2])") == ["1", "2"]
    assert answers(solver, "reverse([1, 2, 3], X)") == ["[3, 2, 1]"]


def test_findall_bagof_setof(solver):
    assert answers(solver, "findall(Y, parent(Y, _), X)") == ["[abraham, isaac, jacob]"]
    assert answers(solver, "bagof(Y, member(Y, [c, a]), X)") == ["[c, a]"]
    assert answers(solver, "findall(Y, fail, X)") == ["[]"]
    assert answers(solver, "bagof(Y, fail, X)") == []


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 0.31.16: setof/3 removes duplicates but does not sort ([c, b, a])",
)
def test_setof_sorts(solver):
    assert answers(solver, "setof(Y, member(Y, [c, a, b, a]), X)") == ["[a, b, c]"]


def test_negation(solver):
    assert once(solver, "orphan(abraham)").is_yes
    assert once(solver, "orphan(isaac)").is_no
    assert once(solver, "not(parent(joseph, _))").is_yes


def test_catch_error(solver):
    assert answers(solver, "safe_div(1, 0, X)") == ["error(evaluation_error(zero_divisor))"]
    assert answers(solver, "safe_div(4, 2, X)") == ["2.0"]


def test_catch_throw(solver):
    assert answers(solver, "catch(fails_with(1), my_error(X), true)") == ["1"]
    assert answers(solver, "catch(throw(foo), X, true)") == ["foo"]


def test_uncaught_throw_is_halt(solver):
    solution = once(solver, "fails_with(2)")
    assert solution.is_halt
    # 2P-Kt wraps uncaught exceptions into a system_error
    assert "my_error(2)" in str(solution.get_exception().error_struct)


@pytest.mark.parametrize(
    "goal, error",
    [
        ("X is Y + 1", "instantiation_error"),
        ("X is foo + 1", "type_error(evaluable, foo/0)"),
        ("atom_length(1, X)", "type_error(atom, 1)"),
        ("X is 1 / 0", "evaluation_error(zero_divisor)"),
        ("call(1)", "type_error(callable, 1)"),
    ],
)
def test_errors_surface_as_halt(solver, goal, error):
    solution = once(solver, goal)
    assert solution.is_halt
    assert str(solution.get_exception().error_struct).startswith(f"error({error.split('/')[0]}")


def test_unknown_procedure_default_warns_and_fails():
    warnings = []
    solver = prolog_solver(warning=output_channel(warnings.append))
    assert once(solver, "nope(1)").is_no
    assert len(warnings) == 1
    assert "nope/1" in str(warnings[0])


@pytest.mark.parametrize(
    "flags, expected",
    [
        (DEFAULT_FLAG_STORE.set(Unknown, Unknown.ERROR), "halt"),  # type: ignore[attr-defined]
        (flag_store(unknown=atom("fail")), "no"),
    ],
)
def test_flags_passed_to_factory(flags, expected):
    warnings = []
    solver = prolog_solver(flags=flags, warning=output_channel(warnings.append))
    solution = once(solver, "nope(1)")
    assert ("halt" if solution.is_halt else "no") == expected
    assert warnings == []
    assert solver.flags[Unknown] == flags[Unknown]


def test_prolog_flags_at_runtime(solver):
    assert answers(solver, "current_prolog_flag(unknown, X)") == ["warning"]
    assert answers(solver, "set_prolog_flag(unknown, fail), current_prolog_flag(unknown, X)") == [
        "fail"
    ]
    assert str(solver.flags[Unknown]) == "fail"


def test_assert_and_retract_on_dynamic_kb(solver):
    assert once(solver, "assertz(counter(1)), asserta(counter(0))").is_yes
    assert answers(solver, "counter(X)") == ["0", "1"]
    assert once(solver, "retract(counter(0))").is_yes
    assert answers(solver, "counter(X)") == ["1"]
    assert once(solver, "retractall(counter(_))").is_yes
    assert answers(solver, "counter(X)") == []
    assert len(solver.dynamic_kb) == 0


def test_assert_persists_on_immutable_solver_too():
    solver = prolog_solver(mutable=False)
    assert once(solver, "assertz(fact(1))").is_yes
    assert answers(solver, "fact(X)") == ["1"]
    assert len(solver.dynamic_kb) == 1


@pytest.mark.parametrize("goal", ["assertz(parent(a, b))", "retract(parent(abraham, isaac))"])
def test_static_kb_is_not_modifiable(solver, goal):
    solution = once(solver, goal)
    assert solution.is_halt
    assert "permission_error" in str(solution.get_exception().error_struct)
    assert len(solver.static_kb) == len(parse_theory(PROGRAM))


def test_dynamic_kb_argument():
    solver = prolog_solver(dynamic_kb=parse_theory("d(1)."))
    assert once(solver, "retract(d(1))").is_yes
    assert len(solver.dynamic_kb) == 0


def test_knowledge_bases_are_copied():
    static, dynamic = theory(*parse_theory("s(1).")), mutable_theory(*parse_theory("d(1)."))
    solver = prolog_solver(static_kb=static, dynamic_kb=dynamic)
    once(solver, "assertz(d(2))")
    assert len(dynamic) == 1
    assert len(solver.dynamic_kb) == 2
    assert solver.static_kb == static


def test_clause_inspection(solver):
    bodies = answers(solver, "clause(max(A, B, C), X)")
    assert len(bodies) == 2
    assert bodies[1] == "true"
    assert answers(solver, "clause(parent(abraham, X), true)") == ["isaac"]


def test_write_to_custom_stdout():
    out = []
    solver = prolog_solver(std_out=output_channel(lambda m: out.append(str(m))))
    assert once(solver, "write(hello), nl, write('a b'), write(f(1 + 2, \"s\"))").is_yes
    assert "".join(out) == "hello\na bf(1 + 2, s)"


def test_write_on_immutable_solver_uses_custom_stdout():
    out = []
    solver = prolog_solver(std_out=output_channel(out.append), mutable=False)
    once(solver, "write(x)")
    assert [str(m) for m in out] == ["x"]


def test_custom_std_channels_are_installed():
    stdin = input_channel("foo.")
    stderr = output_channel(lambda _: None)
    solver = prolog_solver(std_in=stdin, std_err=stderr)
    assert solver.standard_input == stdin
    assert solver.standard_error == stderr


def test_custom_libraries():
    solver = prolog_solver(libraries=library("my.lib", clauses=parse_theory("hello(world).")))
    assert answers(solver, "hello(X)") == ["world"]
    # replacing the runtime keeps the default builtins
    assert once(solver, "X is 1 + 1").is_yes


def test_operators_from_theory_directives():
    solver = prolog_solver(static_kb=parse_theory(":- op(700, xfx, likes). likes(john, mary)."))
    likes = operator("likes", specifier("xfx"), 700)
    assert likes in solver.operators
    assert likes not in DEFAULT_OPERATORS


def test_op_at_runtime(solver):
    assert once(solver, "op(700, xfx, ===>)").is_yes
    assert operator("===>", specifier("xfx"), 700) in solver.operators


def test_parsing_with_solver_operators():
    solver = prolog_solver(static_kb=parse_theory(":- op(700, xfx, likes)."))
    program = parse_theory("john likes mary.", solver.operators)
    solver.load_static_kb(program)
    assert answers(solver, "likes(john, X)") == ["mary"]
    assert solver.operators.plus(operator_set()) == solver.operators


def test_timeout_halts_infinite_loops(solver):
    solution = solver.solve_once(atom("loop"), solve_options(timeout=100))
    assert solution.is_halt
    assert "TimeOut" in type(solution.get_exception()).__name__


def test_limit_and_lazy_iteration(solver):
    assert answers(solver, "between(1, 1000000, X)", options=solve_options(limit=3)) == [
        "1",
        "2",
        "3",
    ]
    lazy = iter(solver.solve(parse_struct("repeat")))
    assert all(next(lazy).is_yes for _ in range(5))


def test_halt_builtin(solver):
    solution = once(solver, "halt")
    assert solution.is_halt
    assert "Halt" in type(solution.get_exception()).__name__


def test_atoms_and_strings(solver):
    assert answers(solver, "atom_concat(foo, bar, X)") == ["foobar"]
    assert answers(solver, "atom_length(hello, X)") == ["5"]
    assert answers(solver, "atom_chars(X, [h, i])") == ["hi"]


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 0.31.16: sub_atom(hello, 1, 3, _, X) yields a spurious second Yes "
    "with an empty substitution",
)
def test_sub_atom_is_deterministic_when_fully_specified(solver):
    assert [str(s) for s in solver.solve(parse_struct("sub_atom(hello, 1, 3, _, X)"))] == [
        "Yes(query=sub_atom(hello, 1, 3, __0, X_0), substitution={X_0=ell})"
    ]


def test_term_inspection(solver):
    assert answers(solver, "functor(f(a, b), N, X)") == ["2"]
    assert answers(solver, "arg(2, f(a, b), X)") == ["b"]
    assert answers(solver, "f(a, b) =.. X") == ["[f, a, b]"]
    assert answers(solver, "copy_term(f(Y), X)") != []


def test_solving_terms_built_in_python(solver):
    who = var("Who")
    solutions = solver.solve(struct("ancestor", atom("abraham"), who))
    assert [str(s.substitution[who]) for s in solutions if s.is_yes] == [
        "isaac",
        "jacob",
        "joseph",
    ]
    assert solver.solve_once(struct("len", parse_struct("[a]"), integer(1))).is_yes
