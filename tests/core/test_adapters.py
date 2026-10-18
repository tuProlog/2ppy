"""Tests for the Python protocols added to JVM types by `tuprolog.core._adapters`."""

from collections.abc import Sized
from decimal import Decimal

import jpype
import pytest

from tuprolog.core import (
    Integer,
    Real,
    Scope,
    Substitution,
    atom,
    block,
    clause,
    cons,
    directive,
    empty_logic_list,
    fact,
    failed,
    indicator,
    integer,
    logic_list,
    logic_tuple,
    numeric,
    real,
    rule,
    scope,
    struct,
    substitution,
    truth,
    var,
)
from tuprolog.jvmutils import protect_iterable
from tuprolog.math import big_decimal, big_integer

IndexOutOfBoundsException = jpype.JClass("java.lang.IndexOutOfBoundsException")


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


# --- Term -----------------------------------------------------------------------------------------


def test_term_getitem_index(a, X):
    term = struct("f", a, X, integer(1))
    assert term[0] == a
    assert term[1] == X
    assert term[2] == integer(1)


def test_term_getitem_out_of_bounds(a):
    term = struct("f", a)
    with pytest.raises(IndexError):
        term[1]
    with pytest.raises(IndexError):
        atom("a")[0]


def test_term_getitem_nested(a, b, X):
    term = struct("f", struct("g", a, struct("h", b)), X)
    assert term[0, 0] == a
    assert term[0, 1, 0] == b
    assert term[1] == X
    assert term[0, 1] == term[0][1]


def test_term_getitem_with_substitution_applies_it(a, X, Y):
    term = struct("f", X, Y)
    assert term[substitution({X: a})] == struct("f", a, Y)


def test_term_getitem_with_many_substitutions(a, b, X, Y):
    term = struct("f", X, Y)
    assert term[substitution({X: a}), substitution({Y: b})] == struct("f", a, b)


def test_term_python_iteration_over_struct_args(a, X):
    assert list(struct("f", a, X)) == [a, X]
    assert list(atom("a")) == []


@pytest.mark.parametrize("scoped", [False, True])
def test_term_fresh_copy(scoped, a, X):
    term = struct("f", a, X, X)
    copy = term.fresh_copy(scope()) if scoped else term.fresh_copy()
    assert copy != term
    assert copy.structurally_equals(term)
    assert copy[1] == copy[2]
    assert copy[1] != X


def test_term_fresh_copy_reuses_scope_variables(X):
    s = scope()
    term = struct("f", X)
    assert term.fresh_copy(s) == term.fresh_copy(s)


def test_term_fresh_copy_of_ground_term(a):
    assert struct("f", a).fresh_copy() == struct("f", a)


def test_term_equality_and_hashing(a, X):
    assert struct("f", a, X) == struct("f", a, X)
    assert hash(struct("f", a, X)) == hash(struct("f", a, X))
    assert struct("f", a) != struct("g", a)
    assert len({atom("a"), atom("a"), atom("b")}) == 2
    assert {struct("f", X): 1}[struct("f", X)] == 1


def test_term_ordering(a, b, X):
    # 2P-Kt's standard order: variables < numbers < atoms < compound terms
    terms = [struct("f", a), b, integer(1), X, a]
    assert sorted(terms) == [X, integer(1), a, b, struct("f", a)]
    assert a < b
    assert b > a
    assert a <= atom("a")
    assert a >= atom("a")
    assert integer(1) < integer(2)
    assert real(1.5) < real(2.5)
    assert struct("f", a) < struct("f", a, a)


def test_term_repr_and_str(a):
    term = struct("f", a, logic_list(a))
    assert str(term) == "f(a, [a])"
    assert repr(term) == "f(a, [a])"


def test_term_snake_case_properties(a, X):
    term = struct("f", a, X)
    assert term.is_struct
    assert not term.is_ground
    assert not term.is_atom
    assert list(term.variables) == [X]
    assert term.cast_to_struct() == term
    assert term.as_var() is None


# --- Struct ---------------------------------------------------------------------------------------


def test_struct_insert_at(a, b, c):
    term = struct("f", a, c)
    assert term.insert_at(1, b) == struct("f", a, b, c)
    assert term.insert_at(0, b) == struct("f", b, a, c)


def test_struct_insert_at_out_of_bounds(a, b):
    with pytest.raises(IndexError):
        struct("f", a).insert_at(5, b)


def test_struct_set_args_varargs(a, b, X):
    assert struct("f", X).set_args(a, b) == struct("f", a, b)


@pytest.mark.parametrize("collection", [list, tuple, iter])
def test_struct_set_args_single_iterable(collection, a, b, X):
    assert struct("f", X).set_args(collection([a, b])) == struct("f", a, b)


def test_struct_set_args_single_struct(a, X):
    assert struct("f", X).set_args(struct("g", a)) == struct("f", struct("g", a))


def test_struct_set_args_empty(X):
    assert struct("f", X).set_args() == atom("f")


# --- Numeric, Integer, Real -----------------------------------------------------------------------


@pytest.mark.parametrize("value", [0, 1, -1, 2**70, -(2**70)])
def test_integer_python_values(value):
    term = integer(value)
    assert term.value == value
    assert type(term.value) is int
    assert term.int_value == value
    assert type(term.int_value) is int
    assert term.to_int() == value
    assert term.decimal_value == Decimal(value)
    assert term.to_float() == float(value)


@pytest.mark.parametrize("value", ["0.5", "-1.25", "3.141592653589793238462643383279"])
def test_real_python_values(value):
    term = real(value)
    assert term.value == Decimal(value)
    assert isinstance(term.value, Decimal)
    assert term.decimal_value == Decimal(value)
    assert term.to_float() == float(value)
    assert term.int_value == int(Decimal(value))
    assert term.to_int() == int(Decimal(value))


def test_numeric_jvm_getters_are_still_available():
    assert integer(5).getIntValue() == big_integer(5)
    assert real("1.5").getDecimalValue() == big_decimal("1.5")
    assert isinstance(integer(5).getValue(), type(big_integer(5)))


def test_integer_constants():
    assert Integer.ZERO == integer(0)
    assert Integer.ONE == integer(1)
    assert Real.ONE_HALF == real(0.5)


@pytest.mark.parametrize(
    "smaller, greater",
    [
        (integer(1), integer(2)),
        (integer(-(2**80)), integer(2**80)),
        (real("0.1"), real("0.2")),
    ],
)
def test_numeric_comparison(smaller, greater):
    assert smaller < greater
    assert greater > smaller
    assert smaller != greater


def test_numeric_equality_and_hash():
    assert integer(3) == numeric(3)
    assert hash(integer(3)) == hash(numeric("3"))
    assert real("1.10") == real("1.1")
    assert hash(real("1.10")) == hash(real("1.1"))


# --- Recursive (lists, tuples, blocks) ------------------------------------------------------------


@pytest.mark.parametrize(
    "factory, size",
    [
        (lambda a, b: logic_list(a, b), 2),
        (lambda a, b: logic_list(a, b, a), 3),
        (lambda a, b: logic_list(a), 1),
        (lambda a, b: logic_tuple(a, b, a), 3),
        (lambda a, b: block(a, b), 2),
        (lambda a, b: cons(a, b), 2),
    ],
)
def test_recursive_len(factory, size, a, b):
    term = factory(a, b)
    assert isinstance(term, Sized)
    assert len(term) == size
    assert term.size == size


def test_recursive_unfolded(a, b):
    term = logic_list(a, b)
    assert list(term.unfolded) == [a, b, empty_logic_list()]
    assert list(term.lazily_unfolded) == [a, b, empty_logic_list()]


def test_recursive_unfolded_partial_list(a, X):
    term = cons(a, X)
    assert list(term.unfolded) == [a, X]


def test_recursive_unfolded_tuple(a, b, c):
    assert list(logic_tuple(a, b, c).unfolded) == [a, b, c]


def test_recursive_to_iterable(a, b, c):
    assert list(logic_list(a, b, c).to_iterable()) == [a, b, c]
    assert list(logic_tuple(a, b, c).to_iterable()) == [a, b, c]
    assert list(block(a, b, c).to_iterable()) == [a, b, c]


def test_recursive_to_iterable_partial_list_includes_the_tail(a, X):
    assert list(cons(a, X).to_iterable()) == [a, X]


@pytest.mark.xfail(
    strict=True,
    reason="Python iteration over a Recursive term yields the Struct arguments (head and tail), "
    "inconsistently with len(); adding __iter__ would also make iterable_or_varargs split "
    "single list arguments (e.g. struct('f', [a, b]-as-logic-list))",
)
def test_recursive_iteration_is_consistent_with_len(a, b, c):
    term = logic_list(a, b, c)
    assert len(list(term)) == len(term)
    assert list(term) == [a, b, c]


# --- Clause ---------------------------------------------------------------------------------------


@pytest.fixture
def a_rule(X):
    return rule(struct("p", X, X), struct("q", X), struct("r", X))


def test_clause_set_head_args_varargs(a_rule, a, b):
    result = a_rule.set_head_args(a, b)
    assert result.head == struct("p", a, b)
    assert result.body == a_rule.body


@pytest.mark.parametrize("collection", [list, tuple, iter])
def test_clause_set_head_args_single_iterable(collection, a_rule, a, b):
    assert a_rule.set_head_args(collection([a, b])).head == struct("p", a, b)


def test_clause_set_head_args_single_struct(a_rule, a):
    assert a_rule.set_head_args(struct("g", a)).head == struct("p", struct("g", a))


def test_clause_insert_head_arg(a_rule, a, X):
    assert a_rule.insert_head_arg(0, a).head == struct("p", a, X, X)
    assert a_rule.insert_head_arg(1, a).head == struct("p", X, a, X)


def test_clause_set_body_items_varargs(a_rule, a, b):
    result = a_rule.set_body_items(a, b)
    assert result.head == a_rule.head
    assert result.body == logic_tuple(a, b)


@pytest.mark.parametrize("collection", [list, tuple, iter])
def test_clause_set_body_items_single_iterable(collection, a_rule, a, b):
    assert a_rule.set_body_items(collection([a, b])).body == logic_tuple(a, b)


def test_clause_set_body_items_single_struct(a_rule, a):
    assert a_rule.set_body_items(struct("g", a)).body == struct("g", a)


def test_clause_snake_case_accessors(a_rule, X):
    assert a_rule.head == struct("p", X, X)
    assert a_rule.body_size == 2
    assert a_rule.body_as_tuple == logic_tuple(struct("q", X), struct("r", X))
    assert a_rule.is_rule
    assert fact(atom("f")).is_fact
    assert directive(atom("d")).is_directive


@pytest.mark.xfail(
    strict=True,
    reason="JVM methods returning anonymous java.lang.Iterable implementations (e.g. "
    "Clause.getBodyItems) yield java.lang.Object$Anonymous objects that are neither "
    "Python-iterable nor accepted by protect_iterable (the workaround documented in README)",
)
@pytest.mark.parametrize("wrap", [lambda x: x, protect_iterable], ids=["plain", "protected"])
def test_clause_body_items_is_python_iterable(wrap, a_rule, X):
    assert list(wrap(a_rule.body_items)) == [struct("q", X), struct("r", X)]


# --- Substitution ---------------------------------------------------------------------------------


@pytest.fixture
def sub(a, b, X, Y):
    return substitution({X: a, Y: b})


def test_substitution_add(a, b, X, Y):
    assert substitution({X: a}) + substitution({Y: b}) == substitution({X: a, Y: b})


def test_substitution_add_contradicting_is_failed(a, b, X):
    result = substitution({X: a}) + substitution({X: b})
    assert isinstance(result, Substitution.Fail)


def test_substitution_add_failed(a, X):
    assert (substitution({X: a}) + failed()).is_failed


def test_substitution_sub_substitution(sub, b, X, Y):
    assert sub - substitution({X: atom("whatever")}) == substitution({Y: b})


def test_substitution_sub_variable(sub, b, X, Y):
    assert sub - X == substitution({Y: b})


def test_substitution_sub_iterable(sub, X, Y):
    assert sub - [X, Y] == substitution()


def test_substitution_filter_unary_predicate(sub, a, X):
    assert sub.filter(lambda entry: entry.getKey() == X) == substitution({X: a})
    assert sub.filter(lambda entry: False) == substitution()


def test_substitution_filter_binary_predicate(sub, b, Y):
    assert sub.filter(lambda v, t: v == Y) == substitution({Y: b})
    assert sub.filter(lambda v, t: True) == sub


def test_substitution_filter_variables(sub, a, X):
    assert sub.filter([X]) == substitution({X: a})


def test_substitution_filter_on_failed():
    assert failed().filter(lambda v, t: True).is_failed


def test_substitution_mapping_protocol(sub, a, b, X, Y):
    assert len(sub) == 2
    assert X in sub
    assert var("Z") not in sub
    assert sub[X] == a
    assert set(sub) == {X, Y}
    assert set(sub.keys()) == {X, Y}
    assert sub.get(var("Z")) is None
    assert dict(sub.items()) == {X: a, Y: b}


def test_substitution_apply(sub, a, b, X, Y):
    assert sub.apply_to(struct("f", X, Y)) == struct("f", a, b)
    assert sub.apply_to(var("Z")).is_var


def test_substitution_equality_and_hash(sub, a, b, X, Y):
    assert sub == substitution({Y: b, X: a})
    assert hash(sub) == hash(substitution({Y: b, X: a}))


# --- Scope ----------------------------------------------------------------------------------------


@pytest.fixture
def s():
    return scope("X", "Y")


def test_scope_contains(s):
    assert "X" in s
    assert s["X"] in s
    assert "Z" not in s
    assert var("Z") not in s
    # 2P-Kt's Scope.contains(Var) only checks the variable name
    assert var("X") in s


def test_scope_getitem(s):
    assert s["X"].name == "X"
    assert s["X"] == s["X"]
    assert s["Z"] is None


def test_scope_var_creates_or_reuses(s):
    assert s.var("X") == s["X"]
    z = s.var("Z")
    assert z == s["Z"]
    assert "Z" in s


def test_scope_atom(s):
    assert s.atom("a") == atom("a")


def test_scope_truth(s):
    assert s.truth(True) == truth(True)
    assert s.truth(False) == truth(False)


@pytest.mark.parametrize("value", [3, -3, 2**100, "3", big_integer(3)])
def test_scope_integer(s, value):
    assert s.integer(value) == integer(value)


@pytest.mark.parametrize("value", [1.5, "1.5", Decimal("1.5"), big_decimal("1.5")])
def test_scope_real(s, value):
    assert s.real(value) == real("1.5")


@pytest.mark.parametrize(
    "value, expected",
    [
        (3, integer(3)),
        (2**100, integer(2**100)),
        (big_integer(3), integer(3)),
        (3.5, real(3.5)),
        (Decimal("3.5"), real("3.5")),
        ("3", integer(3)),
        ("3.5", real("3.5")),
    ],
)
def test_scope_numeric(s, value, expected):
    assert s.numeric(value) == expected


def test_scope_struct(s):
    assert s.struct("f", s["X"], s["Y"]) == struct("f", s["X"], s["Y"])
    assert s.struct("f", [s["X"], s["Y"]]) == struct("f", s["X"], s["Y"])
    assert s.struct("f") == atom("f")


def test_scope_list(s, a):
    assert s.list(s["X"], a) == logic_list(s["X"], a)
    assert s.list([s["X"], a]) == logic_list(s["X"], a)
    assert s.list() == empty_logic_list()


def test_scope_list_from(s, a):
    assert s.list_from([a], s["X"]) == cons(a, s["X"])
    assert s.list_from([a, empty_logic_list()]) == logic_list(a)


def test_scope_cons(s, a):
    assert s.cons(a) == logic_list(a)
    assert s.cons(a, s["X"]) == cons(a, s["X"])


def test_scope_tuple(s, a, b):
    assert s.tuple(a, b) == logic_tuple(a, b)
    assert s.tuple(a, b, s["X"]) == logic_tuple(a, b, s["X"])
    assert s.tuple(a, b, [a, b]) == logic_tuple(a, b, a, b)


def test_scope_block(s, a, b):
    assert s.block(a, b) == block(a, b)
    assert s.block([a, b]) == block(a, b)


def test_scope_fact(s):
    assert s.fact(struct("p", s["X"])) == fact(struct("p", s["X"]))


def test_scope_indicator(s):
    assert s.indicator("f", 2) == indicator("f", 2)
    assert s.indicator(atom("f"), integer(2)) == indicator("f", 2)


def test_scope_rule(s, a, b):
    head = struct("p", s["X"])
    assert s.rule(head, a) == rule(head, a)
    assert s.rule(head, a, b) == rule(head, a, b)
    assert s.rule(head, [a, b]) == rule(head, a, b)


def test_scope_clause(s, a, b):
    head = struct("p", s["X"])
    assert s.clause(head, a, b) == clause(head, a, b)
    assert s.clause(head, [a, b]) == clause(head, a, b)
    assert s.clause(head) == fact(head)
    assert s.clause(None, a) == directive(a)


def test_scope_directive(s, a, b):
    assert s.directive(a, b) == directive(a, b)
    assert s.directive([a, b]) == directive(a, b)


def test_scope_snake_case_accessors(s):
    assert isinstance(s, Scope)
    assert s.empty_logic_list == empty_logic_list()
    assert {str(k) for k in s.variables} == {"X", "Y"}
