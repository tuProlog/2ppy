"""Tests for the names re-exported by `tuprolog.core` (definitions, impl, exception)."""

import jpype
import pytest

from tuprolog import core
from tuprolog.core import (
    FAIL,
    FALSE,
    TRUE,
    AbstractTermComparator,
    AbstractTermConvertible,
    AbstractTermVisitor,
    TermComparator,
    TermConvertible,
    TermFormatter,
    TermVisitor,
    atom,
    block,
    cons,
    directive,
    empty_block,
    empty_logic_list,
    fact,
    indicator,
    integer,
    logic_list,
    logic_tuple,
    pretty_expressions_formatter,
    real,
    rule,
    struct,
    var,
)
from tuprolog.core.exception import (
    SubstitutionApplicationException,
    SubstitutionException,
    TuPrologException,
)
from tuprolog.core.impl import DefaultTermFormatter
from tuprolog.jvmutils import jlist

Collections = jpype.JClass("java.util.Collections")


@pytest.mark.parametrize(
    "name",
    [
        "Applicable",
        "Atom",
        "Block",
        "Clause",
        "Cons",
        "Constant",
        "Directive",
        "Empty",
        "EmptyBlock",
        "EmptyList",
        "Fact",
        "Formatter",
        "Indicator",
        "Integer",
        "List",
        "Numeric",
        "Real",
        "Recursive",
        "Rule",
        "Scope",
        "Struct",
        "Substitution",
        "Term",
        "TermComparator",
        "TermConvertible",
        "TermFormatter",
        "Terms",
        "TermVisitor",
        "Truth",
        "Tuple",
        "Var",
        "Variabled",
    ],
)
def test_jvm_types_are_reexported(name):
    jvm_type = getattr(core, name)
    assert isinstance(jvm_type, jpype.JClass)
    assert jvm_type == jpype.JClass("it.unibo.tuprolog.core." + name)


def test_truth_constants():
    assert TRUE.is_true
    assert str(TRUE) == "true"
    assert str(FALSE) == "false"
    assert FAIL.is_fail
    assert str(FAIL) == "fail"
    assert TRUE != FALSE


def test_exceptions_are_reexported():
    for name, exc in [
        ("TuPrologException", TuPrologException),
        ("SubstitutionException", SubstitutionException),
        ("SubstitutionApplicationException", SubstitutionApplicationException),
    ]:
        assert exc == jpype.JClass("it.unibo.tuprolog.core.exception." + name)
    assert issubclass(SubstitutionException, TuPrologException)
    assert issubclass(SubstitutionApplicationException, SubstitutionException)
    assert issubclass(TuPrologException, Exception)


def test_exceptions_can_be_caught_as_python_exceptions():
    with pytest.raises(Exception, match="boom"):
        raise TuPrologException("boom")


def test_default_term_formatter():
    formatter = DefaultTermFormatter()
    assert isinstance(formatter, TermFormatter)
    assert formatter.format(struct("f", atom("a"))) == "f(a)"


def test_pretty_term_formatter():
    formatter = pretty_expressions_formatter()
    assert formatter.format(struct("+", atom("a"), struct("*", atom("b"), atom("c")))) == (
        "a + b * c"
    )


# --- AbstractTermComparator -----------------------------------------------------------------------


class _ByLength(AbstractTermComparator):
    def compare(self, first, second):
        return len(str(first)) - len(str(second))


def test_abstract_term_comparator_used_by_jvm():
    items = jlist([struct("ff", atom("a")), atom("a"), struct("f", atom("a"), atom("a"))])
    Collections.sort(items, _ByLength())
    assert list(items) == [atom("a"), struct("ff", atom("a")), struct("f", atom("a"), atom("a"))]


def test_abstract_term_comparator_is_a_term_comparator():
    assert isinstance(jpype.JObject(_ByLength(), TermComparator), TermComparator)


def test_abstract_term_comparator_equality_is_identity():
    comparator = _ByLength()
    assert comparator.equals(comparator)
    assert not comparator.equals(_ByLength())


def test_abstract_term_comparator_compare_is_abstract():
    with pytest.raises(NotImplementedError):
        AbstractTermComparator().compare(atom("a"), atom("b"))


# --- AbstractTermConvertible ----------------------------------------------------------------------


def test_abstract_term_convertible():
    class Point(AbstractTermConvertible):
        def toTerm(self):
            return struct("point", integer(1), integer(2))

    converted = jpype.JObject(Point(), TermConvertible)
    assert converted.toTerm() == struct("point", integer(1), integer(2))


def test_abstract_term_convertible_to_term_is_abstract():
    with pytest.raises(NotImplementedError):
        AbstractTermConvertible().toTerm()


# --- AbstractTermVisitor --------------------------------------------------------------------------


class _DefaultVisitor(AbstractTermVisitor):
    def defaultValue(self, term):
        return "default"


ALL_TERMS = [
    atom("a"),
    var("X"),
    integer(1),
    real(1.5),
    TRUE,
    FAIL,
    struct("f", atom("a")),
    logic_list(atom("a")),
    empty_logic_list(),
    cons(atom("a"), var("T")),
    logic_tuple(atom("a"), atom("b")),
    block(atom("a")),
    empty_block(),
    indicator("f", 1),
    rule(struct("p", var("X")), atom("a")),
    fact(struct("p", var("X"))),
    directive(atom("a")),
]


@pytest.mark.parametrize("term", ALL_TERMS, ids=str)
def test_abstract_term_visitor_defaults_to_default_value(term):
    assert term.accept(_DefaultVisitor()) == "default"


@pytest.mark.parametrize("term", ALL_TERMS, ids=str)
def test_abstract_term_visitor_without_default_value_fails(term):
    with pytest.raises(NotImplementedError):
        term.accept(AbstractTermVisitor())


class _KindVisitor(_DefaultVisitor):
    def visitVar(self, term):
        return "var"

    def visitNumeric(self, term):
        return "numeric"

    def visitAtom(self, term):
        return "atom"

    def visitStruct(self, term):
        return "struct"

    def visitCollection(self, term):
        return "collection"

    def visitClause(self, term):
        return "clause"


@pytest.mark.parametrize(
    "term, kind",
    [
        (var("X"), "var"),
        (integer(1), "numeric"),
        (real(1.5), "numeric"),
        (atom("a"), "atom"),
        (TRUE, "atom"),
        (empty_logic_list(), "collection"),
        (empty_block(), "collection"),
        (struct("f", atom("a")), "struct"),
        (indicator("f", 1), "struct"),
        (logic_list(atom("a")), "collection"),
        (logic_tuple(atom("a"), atom("b")), "collection"),
        (block(atom("a")), "collection"),
        (rule(struct("p", var("X")), atom("a")), "clause"),
        (fact(atom("p")), "clause"),
        (directive(atom("a")), "clause"),
    ],
    ids=str,
)
def test_abstract_term_visitor_dispatches_through_the_hierarchy(term, kind):
    assert term.accept(_KindVisitor()) == kind


def test_abstract_term_visitor_is_a_term_visitor():
    assert isinstance(jpype.JObject(_DefaultVisitor(), TermVisitor), TermVisitor)
