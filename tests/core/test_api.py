"""Tests for the Pythonic factory functions in `tuprolog.core._api`."""

from decimal import Decimal

import jpype
import pytest

from tuprolog.core import (
    EMPTY_UNIFIER,
    FAILED_SUBSTITUTION,
    FALSE,
    TRUE,
    Atom,
    Block,
    Clause,
    Cons,
    Directive,
    EmptyBlock,
    EmptyList,
    Fact,
    Indicator,
    Integer,
    List,
    Real,
    Rule,
    Scope,
    Struct,
    Substitution,
    Term,
    Truth,
    Tuple,
    Var,
    atom,
    block,
    clause,
    cons,
    directive,
    empty_block,
    empty_logic_list,
    fact,
    failed,
    indicator,
    integer,
    logic_list,
    logic_list_from,
    logic_tuple,
    numeric,
    real,
    rule,
    scope,
    struct,
    substitution,
    truth,
    unifier,
    var,
    variables,
)
from tuprolog.core.parsing import parse_term
from tuprolog.math import big_decimal, big_integer

IllegalArgumentException = jpype.JClass("java.lang.IllegalArgumentException")


@pytest.fixture
def a():
    return atom("a")


@pytest.fixture
def b():
    return atom("b")


@pytest.fixture
def c():
    return atom("c")


@pytest.fixture
def X():
    return var("X")


@pytest.fixture
def Y():
    return var("Y")


# --- atom -----------------------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["a", "hello_world", "A b", "", "[]", "{}", "+", "'quoted'"])
def test_atom(name):
    term = atom(name)
    assert isinstance(term, Atom)
    assert term.value == name
    assert term.functor == name
    assert term.arity == 0
    assert term.is_atom


def test_atom_equality_and_hash():
    assert atom("a") == atom("a")
    assert hash(atom("a")) == hash(atom("a"))
    assert atom("a") != atom("b")


def test_atom_rejects_non_strings():
    with pytest.raises(TypeError):
        atom(1)


# --- var ------------------------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["X", "Foo", "_", "_Hidden", "x"])
def test_var(name):
    term = var(name)
    assert isinstance(term, Var)
    assert term.name == name
    assert term.is_var


def test_vars_with_the_same_name_are_distinct():
    assert var("X") != var("X")
    assert var("X").structurally_equals(var("X"))


def test_var_is_equal_to_itself(X):
    assert X == X.fresh_copy(scope(X))
    assert hash(X) == hash(X)


def test_anonymous_var():
    assert var("_").is_anonymous


# --- truth ----------------------------------------------------------------------------------------


def test_truth():
    assert truth(True) == TRUE
    assert truth(False) == FALSE
    assert isinstance(truth(True), Truth)
    assert truth(True).is_true
    assert not truth(False).is_true


# --- integer --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value", [0, 1, -1, 42, 2**31, -(2**31) - 1, 2**63, -(2**63) - 1, 2**100, -(2**100)]
)
def test_integer_from_int(value):
    term = integer(value)
    assert isinstance(term, Integer)
    assert str(term) == str(value)
    assert term.int_value == value


@pytest.mark.parametrize("value", ["0", "12", "-12", str(2**100)])
def test_integer_from_string(value):
    assert integer(value) == integer(int(value))


def test_integer_from_big_integer():
    assert integer(big_integer(42)) == integer(42)


def test_integer_from_bool():
    assert integer(True) == integer(1)
    assert integer(False) == integer(0)


@pytest.mark.parametrize("value", [1.5, None, [1]])
def test_integer_rejects_non_integers(value):
    with pytest.raises(TypeError):
        integer(value)


def test_integer_rejects_malformed_strings():
    with pytest.raises(Exception, match="NumberFormatException"):
        integer("abc")


# --- real -----------------------------------------------------------------------------------------


@pytest.mark.parametrize("value", [0.5, 1.5, -2.25, 1e-3, 0.1, 1 / 3, 1e-320, 2.5e300])
def test_real_from_float(value):
    # the shortest repr of the float, not its binary expansion (e.g. 0.1, not 0.1000...0555...)
    term = real(value)
    assert isinstance(term, Real)
    assert term.decimal_value == Decimal(repr(value))
    assert term.to_float() == value


@pytest.mark.parametrize("value", ["1.5", "-0.25", "3.14159265358979323846264338327950288"])
def test_real_from_string_and_decimal(value):
    assert real(value) == real(Decimal(value))
    assert real(value).decimal_value == Decimal(value)


def test_real_from_big_decimal():
    assert real(big_decimal("1.25")) == real("1.25")


def test_real_from_int():
    assert real(3) == real(3.0)
    assert real(3).is_real


def test_real_ignores_trailing_zeros():
    assert real("1.10") == real("1.1")


@pytest.mark.parametrize("value", [10.0, 100.0, 1e10, -1000.0, "100", Decimal("1E+2")])
def test_integral_reals_are_formatted_in_parsable_way(value):
    term = real(value)
    assert parse_term(str(term)) == term
    assert "E" not in str(term)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_real_rejects_non_finite_floats(value):
    with pytest.raises(Exception, match="NumberFormatException"):
        real(value)


# --- numeric --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (3, Integer),
        (-(2**80), Integer),
        (3.5, Real),
        (Decimal("2.5"), Real),
        ("3", Integer),
        ("-3", Integer),
        ("3.5", Real),
    ],
)
def test_numeric(value, expected):
    term = numeric(value)
    assert isinstance(term, expected)
    if isinstance(value, str):
        assert term == parse_term(value)


def test_numeric_from_big_numbers():
    assert numeric(big_integer(3)) == integer(3)
    assert numeric(big_decimal("3.5")) == real("3.5")


def test_numeric_rejects_malformed_strings():
    with pytest.raises(Exception, match="NumberFormatException"):
        numeric("abc")


# --- struct ---------------------------------------------------------------------------------------


def test_struct_with_varargs(a, X):
    term = struct("f", a, X, integer(1))
    assert isinstance(term, Struct)
    assert term.functor == "f"
    assert term.arity == 3
    assert list(term.args) == [a, X, integer(1)]


@pytest.mark.parametrize("collection", [list, tuple, iter])
def test_struct_with_single_iterable(collection, a, b):
    assert struct("f", collection([a, b])) == struct("f", a, b)


def test_struct_with_generator(a, b):
    assert struct("f", (t for t in [a, b])) == struct("f", a, b)


def test_struct_without_args_is_an_atom():
    term = struct("f")
    assert isinstance(term, Atom)
    assert term == atom("f")


def test_struct_with_empty_iterable_is_an_atom():
    assert struct("f", []) == atom("f")


@pytest.mark.parametrize(
    "factory",
    [
        lambda X: struct("g", X),
        lambda X: struct("g", X, X),
        lambda X: logic_list(X, X),
        lambda X: logic_tuple(X, X),
        lambda X: block(X, X),
        lambda X: cons(X, X),
        lambda X: X,
        lambda X: atom("x"),
        lambda X: integer(1),
    ],
)
def test_struct_with_single_term_argument_has_arity_1(factory, X):
    argument = factory(X)
    term = struct("f", argument)
    assert term.arity == 1
    assert term[0] == argument


def test_struct_with_single_string_argument_is_not_split():
    assert struct("f", "abc").arity == 1


def test_struct_converts_string_arguments_into_atoms():
    assert struct("f", "abc") == struct("f", atom("abc"))


# --- logic_list -----------------------------------------------------------------------------------


def test_logic_list_with_varargs(a, b, c):
    term = logic_list(a, b, c)
    assert isinstance(term, List)
    assert term.is_list
    assert str(term) == "[a, b, c]"
    assert list(term.to_list()) == [a, b, c]


@pytest.mark.parametrize("collection", [list, tuple, iter])
def test_logic_list_with_single_iterable(collection, a, b):
    assert logic_list(collection([a, b])) == logic_list(a, b)


def test_logic_list_empty():
    term = logic_list()
    assert isinstance(term, EmptyList)
    assert term == empty_logic_list()


def test_logic_list_of_logic_list_is_nested(a, b):
    inner = logic_list(a, b)
    outer = logic_list(inner)
    assert outer.size == 1
    assert str(outer) == "[[a, b]]"


def test_empty_logic_list():
    term = empty_logic_list()
    assert isinstance(term, EmptyList)
    assert str(term) == "[]"
    assert term.is_empty_list


# --- logic_list_from ------------------------------------------------------------------------------


def test_logic_list_from_with_last(a, b, X):
    term = logic_list_from([a, b], X)
    assert term == cons(a, cons(b, X))
    assert not term.is_well_formed


def test_logic_list_from_with_empty_list_as_last(a, b):
    assert logic_list_from([a, b], empty_logic_list()) == logic_list(a, b)


def test_logic_list_from_with_no_last_uses_last_item_as_tail(a, b, c):
    # mirrors 2P-Kt's List.from(items, last = null)
    assert str(logic_list_from([a, b, c])) == "[a, b | c]"


def test_logic_list_from_generator(a, b):
    term = logic_list_from((t for t in [a, b]), empty_logic_list())
    assert term == logic_list(a, b)


def test_logic_list_from_empty():
    assert logic_list_from([]) == empty_logic_list()


# --- cons -----------------------------------------------------------------------------------------


def test_cons_singleton(a):
    term = cons(a)
    assert isinstance(term, Cons)
    assert term == logic_list(a)
    assert term.head == a
    assert term.tail == empty_logic_list()


def test_cons_with_tail(a, X):
    term = cons(a, X)
    assert str(term).startswith("[a | X")
    assert term.head == a
    assert term.tail == X


def test_cons_with_list_tail(a, b):
    assert cons(a, logic_list(b)) == logic_list(a, b)


# --- logic_tuple ----------------------------------------------------------------------------------


def test_logic_tuple_of_two(a, b):
    term = logic_tuple(a, b)
    assert isinstance(term, Tuple)
    assert term.left == a
    assert term.right == b


def test_logic_tuple_varargs(a, b, c):
    assert str(logic_tuple(a, b, c)) == "(a, b, c)"


def test_logic_tuple_with_single_iterable(a, b, c):
    assert logic_tuple(a, b, [c, a]) == logic_tuple(a, b, c, a)


def test_logic_tuple_with_single_struct(a, b, X):
    assert logic_tuple(a, b, struct("g", X)).to_list().size() == 3


def test_logic_tuple_requires_two_items(a):
    with pytest.raises(TypeError):
        logic_tuple(a)


# --- block ----------------------------------------------------------------------------------------


def test_block_with_varargs(a, b):
    term = block(a, b)
    assert isinstance(term, Block)
    assert str(term) == "{a, b}"


@pytest.mark.parametrize("collection", [list, tuple, iter])
def test_block_with_single_iterable(collection, a, b):
    assert block(collection([a, b])) == block(a, b)


def test_block_empty():
    assert isinstance(block(), EmptyBlock)
    assert block() == empty_block()


def test_block_of_block_is_nested(a, b):
    assert str(block(block(a, b))) == "{{a, b}}"


def test_empty_block():
    term = empty_block()
    assert isinstance(term, EmptyBlock)
    assert str(term) == "{}"


# --- clause, rule, fact, directive ----------------------------------------------------------------


def test_clause_with_head_only(X):
    term = clause(struct("p", X))
    assert isinstance(term, Fact)
    assert term.head == struct("p", X)
    assert term.body == TRUE


def test_clause_with_head_and_body(a, b, X):
    term = clause(struct("p", X), a, b)
    assert isinstance(term, Rule)
    assert term.head == struct("p", X)
    assert term.body == logic_tuple(a, b)


@pytest.mark.parametrize("collection", [list, tuple, iter])
def test_clause_with_single_iterable_body(collection, a, b, X):
    assert clause(struct("p", X), collection([a, b])) == clause(struct("p", X), a, b)


def test_clause_with_generator_body(a, b, X):
    assert clause(struct("p", X), (t for t in [a, b])) == clause(struct("p", X), a, b)


def test_clause_without_head_is_a_directive(a):
    term = clause(None, a)
    assert isinstance(term, Directive)
    assert term == directive(a)


def test_clause_without_head_nor_body_is_invalid():
    with pytest.raises(IllegalArgumentException):
        clause()


def test_rule(a, X):
    term = rule(struct("p", X), struct("q", X), a)
    assert isinstance(term, Rule)
    assert term.head == struct("p", X)
    assert term.body == logic_tuple(struct("q", X), a)


def test_rule_with_single_iterable_body(a, b, X):
    assert rule(struct("p", X), [a, b]) == rule(struct("p", X), a, b)


def test_rule_with_generator_body(a, b, X):
    assert rule(struct("p", X), (t for t in [a, b])) == rule(struct("p", X), a, b)


def test_rule_with_single_struct_body(X):
    assert rule(struct("p", X), struct("q", X)).body == struct("q", X)


def test_rule_without_body_is_a_fact(X):
    assert isinstance(rule(struct("p", X)), Fact)


def test_fact(X):
    term = fact(struct("p", X))
    assert isinstance(term, Fact)
    assert term.body == TRUE
    assert term == clause(struct("p", X))


def test_fact_with_atom_head():
    assert str(fact(atom("p"))) == "p :- true"


def test_fact_requires_struct_head(X):
    with pytest.raises(TypeError):
        fact(X)


def test_directive(a, b):
    term = directive(a, b)
    assert isinstance(term, Directive)
    assert term.head is None
    assert str(term) == ":- (a, b)"


@pytest.mark.parametrize("collection", [list, tuple, iter])
def test_directive_with_single_iterable(collection, a, b):
    assert directive(collection([a, b])) == directive(a, b)


def test_directive_with_generator(a, b):
    assert directive(t for t in [a, b]) == directive(a, b)


def test_directive_requires_a_goal():
    with pytest.raises(IllegalArgumentException):
        directive()


# --- indicator ------------------------------------------------------------------------------------


def test_indicator_from_python_values():
    term = indicator("f", 2)
    assert isinstance(term, Indicator)
    assert str(term) == "f/2"
    assert term.indicated_name == "f"
    assert term.indicated_arity == 2


def test_indicator_from_terms():
    assert indicator(atom("f"), integer(2)) == indicator("f", 2)


def test_indicator_from_variables(X, Y):
    term = indicator(X, Y)
    assert not term.is_well_formed


@pytest.mark.parametrize("name, arity", [("f", integer(2)), (atom("f"), 2)])
def test_indicator_from_mixed_values(name, arity):
    assert indicator(name, arity) == indicator("f", 2)


# --- variables and scope --------------------------------------------------------------------------


def test_variables():
    A, B = variables("A", "B")
    assert A.name == "A"
    assert B.name == "B"
    assert A != B


def test_variables_single():
    (A,) = variables("A")
    assert isinstance(A, Var)


def test_variables_with_same_name_are_distinct():
    A1, A2 = variables("A", "A")
    assert A1 != A2


def test_variables_requires_names():
    with pytest.raises(ValueError):
        variables()


def test_scope_empty():
    s = scope()
    assert isinstance(s, Scope)
    assert len(s.variables) == 0


def test_scope_from_names():
    s = scope("X", "Y")
    assert {str(k) for k in s.variables} == {"X", "Y"}
    assert s["X"] == s["X"]
    assert s["X"].name == "X"


def test_scope_from_variables(X, Y):
    s = scope(X, Y)
    assert s["X"] == X
    assert s["Y"] == Y


def test_scope_from_mixed(X):
    s = scope(X, "Y")
    assert s["X"] == X
    assert s["Y"].name == "Y"


# --- substitutions --------------------------------------------------------------------------------


def test_substitution(a, b, X, Y):
    sub = substitution({X: a, Y: b})
    assert isinstance(sub, Substitution)
    assert sub.is_success
    assert len(sub) == 2
    assert sub[X] == a
    assert sub[Y] == b


@pytest.mark.parametrize("arg", [None, {}])
def test_substitution_empty(arg):
    sub = substitution(arg)
    assert len(sub) == 0
    assert sub.is_success
    assert sub == EMPTY_UNIFIER


def test_substitution_normalises_chains(a, X, Y):
    assert substitution({X: Y, Y: a}) == substitution({X: a, Y: a})


def test_unifier(a, X):
    sub = unifier({X: a})
    assert isinstance(sub, Substitution.Unifier)
    assert sub[X] == a


@pytest.mark.parametrize("arg", [None, {}])
def test_unifier_empty(arg):
    assert unifier(arg) == EMPTY_UNIFIER


def test_failed():
    sub = failed()
    assert isinstance(sub, Substitution.Fail)
    assert sub.is_failed
    assert not sub.is_success
    assert sub == FAILED_SUBSTITUTION


def test_constants():
    assert isinstance(EMPTY_UNIFIER, Substitution.Unifier)
    assert len(EMPTY_UNIFIER) == 0
    assert isinstance(FAILED_SUBSTITUTION, Substitution.Fail)


# --- all factories return JVM terms ---------------------------------------------------------------


@pytest.mark.parametrize(
    "term",
    [
        atom("a"),
        var("X"),
        truth(True),
        integer(1),
        real(1.5),
        numeric(1),
        struct("f", atom("a")),
        logic_list(atom("a")),
        empty_logic_list(),
        cons(atom("a")),
        logic_tuple(atom("a"), atom("b")),
        block(atom("a")),
        empty_block(),
        clause(atom("a")),
        rule(atom("a"), atom("b")),
        fact(atom("a")),
        directive(atom("a")),
        indicator("f", 1),
    ],
    ids=str,
)
def test_factories_return_terms(term):
    assert isinstance(term, Term)
    assert isinstance(term, jpype.JObject)


def test_clause_type_hierarchy(X):
    assert isinstance(rule(struct("p", X), atom("a")), Clause)
    assert isinstance(fact(struct("p", X)), Clause)
    assert isinstance(directive(atom("a")), Clause)


def test_substitutions_convert_python_values():
    from tuprolog.core import integer, substitution, unifier, var

    X = var("X")
    assert substitution({X: 1})[X] == integer(1)
    assert unifier({X: "a"})[X] == atom("a")
