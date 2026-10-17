import pytest

from tuprolog.core import Struct
from tuprolog.solve import Signature, signature
from tuprolog.solve.library import Library
from tuprolog.solve.prolog import prolog_solver
from tuprolog.solve.stdlib import (
    CommonBuiltins,
    CommonFunctions,
    CommonPrimitives,
    CommonRules,
    function,
    magic,
    primitive,
    rule,
)


def exported(module, kind):
    return {
        name: getattr(module, name)
        for name in dir(module)
        if not name.startswith("_")
        and type(getattr(module, name)).__module__ != "builtins"
        and hasattr(getattr(module, name), "signature")
        and kind in type(getattr(module, name)).class_.getName()
    }


PRIMITIVES = exported(primitive, ".stdlib.primitive.")
FUNCTIONS = exported(function, ".stdlib.function.")


def test_common_builtins_is_a_library():
    assert isinstance(CommonBuiltins, Library)
    assert CommonBuiltins.alias == "prolog.lang"


def test_common_builtins_aggregates_the_other_singletons():
    assert set(CommonBuiltins.primitives.keySet()) == set(CommonPrimitives.primitives.keySet())
    assert set(CommonBuiltins.functions.keySet()) == set(CommonFunctions.functions.keySet())
    assert len(CommonBuiltins.clauses) == len(CommonRules.clauses)


def test_default_solver_uses_the_common_builtins():
    (builtins,) = list(prolog_solver().libraries.values())
    assert set(CommonBuiltins.primitives.keySet()) <= set(builtins.primitives.keySet())


def test_every_common_primitive_is_exported():
    signatures = {p.signature for p in PRIMITIVES.values()}
    missing = [s for s in CommonPrimitives.primitives.keySet() if s not in signatures]
    assert missing == []


def test_every_common_function_is_exported():
    signatures = {f.signature for f in FUNCTIONS.values()}
    missing = [s for s in CommonFunctions.functions.keySet() if s not in signatures]
    assert missing == []


@pytest.mark.parametrize("name", sorted(PRIMITIVES))
def test_primitive_singletons(name):
    wrapper = PRIMITIVES[name]
    assert isinstance(wrapper.signature, Signature)
    assert wrapper.signature in CommonPrimitives.primitives.keySet()
    assert wrapper.implementation is not None


@pytest.mark.parametrize(
    "wrapper, expected",
    [
        (primitive.Is, ("is", 2)),
        (primitive.Write, ("write", 1)),
        (primitive.Halt, ("halt", 0)),
        (primitive.Halt1, ("halt", 1)),
        (primitive.UnifiesWith, ("=", 2)),
        (primitive.Univ, ("=..", 2)),
        (primitive.FindAll, ("findall", 3)),
    ],
)
def test_primitive_signatures(wrapper, expected):
    assert wrapper.signature == signature(*expected)


@pytest.mark.parametrize("name", sorted(FUNCTIONS))
def test_function_singletons(name):
    wrapper = FUNCTIONS[name]
    assert isinstance(wrapper.signature, Signature)
    assert wrapper.signature in CommonFunctions.functions.keySet()


@pytest.mark.parametrize(
    "wrapper, expected",
    [
        (function.Addition, ("+", 2)),
        (function.SignReversal, ("-", 1)),
        (function.Subtraction, ("-", 2)),
        (function.SquareRoot, ("sqrt", 1)),
        (function.Exponentiation, ("**", 2)),
    ],
)
def test_function_signatures(wrapper, expected):
    assert wrapper.signature == signature(*expected)


def test_magic_cut():
    assert isinstance(magic.MagicCut, Struct)
    assert str(magic.MagicCut) == "!MagicCut!"


@pytest.mark.parametrize(
    "holder, functor, arity, wrappers",
    [
        (rule.Append, "append", 3, [rule.Append.Base, rule.Append.Recursive]),
        (rule.Member, "member", 2, [rule.Member.Base, rule.Member.Recursive]),
        (
            rule.Semicolon,
            ";",
            2,
            [
                rule.Semicolon.If.Then,
                rule.Semicolon.If.Else,
                rule.Semicolon.Or.Left,
                rule.Semicolon.Or.Right,
            ],
        ),
    ],
)
def test_rule_holders(holder, functor, arity, wrappers):
    assert holder.FUNCTOR == functor
    assert holder.ARITY == arity
    assert holder.SIGNATURE == signature(functor, arity)
    for wrapper in wrappers:
        assert wrapper.signature == holder.SIGNATURE
        assert wrapper.implementation.head.functor == functor


@pytest.mark.parametrize(
    "wrapper, expected",
    [
        (rule.Arrow, ("->", 2)),
        (rule.CurrentPrologFlag, ("current_prolog_flag", 2)),
        (rule.Not, ("not", 1)),
        (rule.Once, ("once", 1)),
        (rule.SetPrologFlag, ("set_prolog_flag", 2)),
    ],
)
def test_rule_singletons(wrapper, expected):
    assert wrapper.signature == signature(*expected)
    assert wrapper.implementation in CommonRules.clauses


def test_every_rule_is_in_common_rules():
    rules = [
        rule.Append.Base,
        rule.Append.Recursive,
        rule.Member.Base,
        rule.Member.Recursive,
        rule.Semicolon.If.Then,
        rule.Semicolon.If.Else,
        rule.Semicolon.Or.Left,
        rule.Semicolon.Or.Right,
        rule.Arrow,
        rule.CurrentPrologFlag,
        rule.Not,
        rule.Once,
        rule.SetPrologFlag,
    ]
    clauses = list(CommonRules.clauses)
    assert all(r.implementation in clauses for r in rules)
