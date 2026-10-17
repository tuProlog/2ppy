"""The `ensuring_*` checks offered to primitives implemented in Python."""

import pytest
from jpype import JClass

import tuprolog.solve.primitive as primitives
from tests.solve.primitive._support import (
    CAPTURE,
    RequestCapturer,
    bindings,
    error_of,
    python_int,
    solve_all,
    solver_with_primitive,
)
from tuprolog.core import Term, atom, fact, integer, logic_list, real, struct, var
from tuprolog.core.parsing import parse_term
from tuprolog.solve import signature
from tuprolog.solve.exception import LogicError
from tuprolog.solve.exception.error import (
    OPERATION_ACCESS,
    OPERATION_MODIFY,
    DomainError,
    InstantiationError,
    PermissionError,
    RepresentationError,
    TypeError,
)
from tuprolog.solve.primitive import (
    check_term_is_recursively_callable,
    ensuring_all_arguments_are_instantiated,
    ensuring_argument_is_atom,
    ensuring_argument_is_integer,
    ensuring_clause_procedure_has_permission,
    ensuring_procedure_has_permission,
    ensuring_term_is_char_code,
    ensuring_term_is_well_formed_list,
    is_character_code,
    not_implemented,
    not_supported,
)
from tuprolog.unify import mgu

# tuprolog.solve.exception.error.SystemError is mistakenly bound to SyntaxError
JvmSystemError = JClass("it.unibo.tuprolog.solve.exception.error.SystemError")


@pytest.fixture(scope="module")
def capturer() -> RequestCapturer:
    return RequestCapturer()


SAMPLES: dict[str, Term] = {
    "atom": atom("a"),
    "var": var("X"),
    "code": integer(65),
    "negative": integer(-1),
    "real": real("1.5"),
    "compound": parse_term("f(x)"),
    "list": logic_list(atom("a")),
    "partial_list": parse_term("[a|_]"),
    "indicator": parse_term("foo/2"),
    "clause": parse_term("(h :- b)"),
    "specifier": atom("xfx"),
}

OK = None
TE = "type_error"
IE = "instantiation_error"
DE = "domain_error"
RE = "representation_error"

# For every check, the outcome on each sample: OK, or (error functor, first argument of the error)
EXPECTATIONS: dict[str, dict[str, tuple[str, str] | None]] = {
    "ensuring_argument_is_atom": {
        "atom": OK,
        "var": (TE, "atom"),
        "code": (TE, "atom"),
        "compound": (TE, "atom"),
        "list": (TE, "atom"),
        "specifier": OK,
    },
    "ensuring_argument_is_integer": {
        "atom": (TE, "integer"),
        "code": OK,
        "negative": OK,
        "real": (TE, "integer"),
    },
    "ensuring_argument_is_non_negative_integer": {
        "atom": (TE, "integer"),
        "code": OK,
        "negative": (DE, "not_less_than_zero"),
    },
    "ensuring_argument_is_arity": {
        "atom": (TE, "integer"),
        "code": OK,
        "negative": (DE, "not_less_than_zero"),
    },
    "ensuring_argument_is_numeric": {
        "atom": (TE, "number"),
        "code": OK,
        "real": OK,
        "compound": (TE, "number"),
    },
    "ensuring_argument_is_struct": {
        "atom": OK,
        "var": (TE, "callable"),
        "code": (TE, "callable"),
        "compound": OK,
        "list": OK,
    },
    "ensuring_argument_is_callable": {
        "atom": OK,
        "var": (TE, "callable"),
        "real": (TE, "callable"),
        "compound": OK,
        "clause": OK,
    },
    "ensuring_argument_is_compound": {
        "atom": (TE, "compound"),
        "code": (TE, "compound"),
        "compound": OK,
        "list": OK,
    },
    "ensuring_argument_is_constant": {
        "atom": OK,
        "code": OK,
        "real": OK,
        "var": (TE, "atomic"),
        "compound": (TE, "atomic"),
    },
    "ensuring_argument_is_variable": {
        "var": OK,
        "atom": (TE, "variable"),
        "compound": (TE, "variable"),
    },
    "ensuring_argument_is_instantiated": {
        "var": (IE, ""),
        "atom": OK,
        "partial_list": OK,
    },
    "ensuring_argument_is_ground": {
        "var": (IE, ""),
        "partial_list": (IE, ""),
        "compound": OK,
        "clause": OK,
    },
    "ensuring_argument_is_char": {
        "atom": OK,
        "specifier": (TE, "character"),
        "code": (TE, "character"),
    },
    "ensuring_argument_is_char_code": {
        "code": OK,
        "negative": (RE, "character_code"),
        "atom": (TE, "integer"),
    },
    "ensuring_argument_is_specifier": {
        "specifier": OK,
        "atom": (DE, "operator_specifier"),
        "code": (DE, "operator_specifier"),
    },
    "ensuring_argument_is_list": {
        "list": OK,
        "partial_list": OK,
        "atom": (TE, "list"),
        "compound": (TE, "list"),
    },
    "ensuring_argument_is_well_formed_indicator": {
        "indicator": OK,
        "var": (IE, ""),
        "atom": (TE, "predicate_indicator"),
        "compound": (TE, "predicate_indicator"),
    },
    "ensuring_argument_is_well_formed_clause": {
        "clause": OK,
        "atom": OK,
        "var": (IE, ""),
        "code": (TE, "callable"),
    },
}


def _cases():
    for check, outcomes in EXPECTATIONS.items():
        for sample, outcome in outcomes.items():
            yield pytest.param(check, sample, outcome, id=f"{check}-{sample}")


def _describe(error: LogicError) -> tuple[str, str]:
    struct_ = error.error_struct.get_arg_at(0)
    if struct_.is_atom:
        return str(struct_), ""
    return struct_.functor, str(struct_.get_arg_at(0))


@pytest.mark.parametrize("check, sample, outcome", list(_cases()))
def test_ensuring_argument_checks(capturer, check, sample, outcome):
    request = capturer.request(SAMPLES[sample])
    ensure = getattr(primitives, check)
    if outcome is OK:
        assert ensure(request, 0) == request
    else:
        with pytest.raises(LogicError) as info:
            ensure(request, 0)
        assert _describe(info.value) == outcome


@pytest.mark.parametrize("check", sorted(EXPECTATIONS))
def test_ensuring_argument_checks_reject_out_of_range_index(capturer, check):
    request = capturer.request(atom("a"))
    with pytest.raises(Exception):  # noqa: B017 - an IndexOutOfBoundsException from the JVM
        getattr(primitives, check)(request, 1)


def test_ensuring_errors_have_specific_types(capturer):
    with pytest.raises(TypeError):
        ensuring_argument_is_atom(capturer.request(integer(1)), 0)
    with pytest.raises(InstantiationError):
        primitives.ensuring_argument_is_instantiated(capturer.request(var("X")), 0)
    with pytest.raises(DomainError):
        primitives.ensuring_argument_is_specifier(capturer.request(atom("a")), 0)
    with pytest.raises(RepresentationError):
        primitives.ensuring_argument_is_char_code(capturer.request(integer(-1)), 0)


def test_ensuring_error_message_mentions_signature_and_index(capturer):
    request = capturer.request(atom("a"), atom("b"))
    with pytest.raises(TypeError) as info:
        ensuring_argument_is_integer(request, 1)
    message = str(info.value.error_struct.get_arg_at(1))
    assert "capture/2" in message
    assert "1-th argument" in message


@pytest.mark.parametrize(
    "arguments, ok",
    [
        ((), True),
        ((atom("a"),), True),
        ((atom("a"), integer(1), parse_term("f(X)")), True),
        ((var("X"),), False),
        ((atom("a"), var("X")), False),
    ],
)
def test_ensuring_all_arguments_are_instantiated(capturer, arguments, ok):
    request = capturer.request(*arguments)
    if ok:
        assert ensuring_all_arguments_are_instantiated(request) == request
    else:
        with pytest.raises(InstantiationError):
            ensuring_all_arguments_are_instantiated(request)


def test_ensuring_term_is_char_code(capturer):
    request = capturer.request()
    assert ensuring_term_is_char_code(request, integer(97)) == request
    for term in [integer(-1), atom("a"), var("X")]:
        with pytest.raises(RepresentationError):
            ensuring_term_is_char_code(request, term)


def test_ensuring_term_is_well_formed_list(capturer):
    request = capturer.request()
    assert ensuring_term_is_well_formed_list(request, logic_list(atom("a"))) == request
    assert ensuring_term_is_well_formed_list(request, logic_list()) == request
    for term in [parse_term("[a|_]"), parse_term("[a|b]"), atom("a")]:
        with pytest.raises(DomainError):
            ensuring_term_is_well_formed_list(request, term)


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt 0.31.16's PrimitiveWrapper.isCharacterCode is inverted (true for non-codes)",
)
@pytest.mark.parametrize("code, expected", [(65, True), (0, True), (-1, False), (0x110000, False)])
def test_is_character_code(code, expected):
    assert is_character_code(integer(code)) is expected


def test_check_term_is_recursively_callable(capturer):
    request = capturer.request()
    assert check_term_is_recursively_callable(request, parse_term("(a, b ; c -> d)")) is None
    error = check_term_is_recursively_callable(request, parse_term("(a, 1)"))
    assert isinstance(error, TypeError)
    assert str(error.error_struct.get_arg_at(0)) == "type_error(callable, 1)"


@pytest.mark.parametrize("operation", [OPERATION_MODIFY, OPERATION_ACCESS])
def test_ensuring_procedure_has_permission(capturer, operation):
    request = capturer.request()
    assert ensuring_procedure_has_permission(request, signature("mine", 1), operation) == request


def test_ensuring_procedure_has_permission_rejects_library_procedures(capturer):
    request = capturer.request()
    with pytest.raises(PermissionError) as info:
        ensuring_procedure_has_permission(request, signature("write", 1), OPERATION_MODIFY)
    assert "private_procedure" in str(info.value.error_struct)
    with pytest.raises(PermissionError):
        ensuring_procedure_has_permission(request, signature(CAPTURE, 0), OPERATION_MODIFY)


def test_ensuring_clause_procedure_has_permission(capturer):
    request = capturer.request()
    mine = fact(struct("mine", atom("a")))
    assert ensuring_clause_procedure_has_permission(request, mine, OPERATION_MODIFY) == request
    with pytest.raises(PermissionError):
        ensuring_clause_procedure_has_permission(
            request, fact(struct("write", atom("a"))), OPERATION_MODIFY
        )


@pytest.mark.parametrize(
    "reply, cause", [(not_implemented, "NotImplementedError"), (not_supported, "IllegalState")]
)
def test_not_implemented_and_not_supported_raise_system_errors(capturer, reply, cause):
    with pytest.raises(JvmSystemError) as info:
        reply(capturer.request(), "some message")
    assert cause in str(info.value.error_struct)
    assert "some message" in str(info.value.error_struct)


@pytest.mark.xfail(
    strict=True,
    reason="tuprolog/solve/exception/error/system/_definitions.py binds SystemError to SyntaxError",
)
def test_not_implemented_raises_tuprolog_system_error(capturer):
    from tuprolog.solve.exception.error import SystemError

    with pytest.raises(SystemError):
        not_implemented(capturer.request(), "some message")


# --- end to end: checks raised within primitives become logic errors in the solver ---


@pytest.fixture(scope="module")
def successor_solver():
    def implementation(request):
        primitives.ensuring_argument_is_instantiated(request, 0)
        ensuring_argument_is_integer(request, 0)
        yield request.reply_with(
            mgu(request.arguments[1], integer(python_int(request.arguments[0]) + 1))
        )

    return solver_with_primitive("succ_of", 2, implementation)


def test_checked_primitive_succeeds(successor_solver):
    assert bindings(solve_all(successor_solver, "succ_of(41, X)"), "X") == ["42"]


@pytest.mark.parametrize(
    "goal, error",
    [
        ("succ_of(X, Y)", "instantiation_error"),
        ("succ_of(a, Y)", "type_error(integer, a)"),
        ("succ_of(1.5, Y)", "type_error(integer, 1.5)"),
    ],
)
def test_checked_primitive_halts_with_error(successor_solver, goal, error):
    solutions = solve_all(successor_solver, goal)
    assert len(solutions) == 1
    assert str(error_of(solutions[0]).get_arg_at(0)) == error


def test_checked_primitive_errors_are_catchable(successor_solver):
    goal = "catch(succ_of(a, Y), error(type_error(T, C), _), (R = caught))"
    solutions = solve_all(successor_solver, goal)
    assert bindings(solutions, "R") == ["caught"]
    assert bindings(solutions, "T") == ["integer"]


def test_errors_raised_by_non_generator_primitives_are_logic_errors():
    def implementation(request):
        ensuring_argument_is_atom(request, 0)
        return [request.reply_success()]

    solver = solver_with_primitive("only_atoms", 1, implementation)
    assert solve_all(solver, "only_atoms(a)")[0].is_yes
    assert str(error_of(solve_all(solver, "only_atoms(1)")[0]).get_arg_at(0)) == (
        "type_error(atom, 1)"
    )
