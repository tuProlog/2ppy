from typing import Sized, Callable
from tuprolog import logger
import jpype
from ._ktmath import big_integer, BigInteger, python_integer, python_decimal
from tuprolog.jvmutils import jiterable, kfunction, kpair, ksequence
from tuprolog.pyutils import iterable_or_varargs


@jpype.JImplementationFor("it.unibo.tuprolog.core.Term")
class _KtTerm:
    def __jclass_init__(cls):
        pass

    def __getitem__(self, item, *items):
        return self.get(item, *items)

    @jpype.JOverride()
    def equals(self, other, use_var_complete_name: bool = True):
        return self.equals_(other, use_var_complete_name)

    def fresh_copy(self, scope=None):
        if scope is None:
            return self.freshCopy()
        else:
            return self.freshCopy(scope)


@jpype.JImplementationFor("it.unibo.tuprolog.core.Struct")
class _KtStruct:
    def __jclass_init__(cls):
        pass

    def insert_at(self, index, argument):
        return self.addFirst(index, argument)

    def set_args(self, *args):
        return iterable_or_varargs(args, lambda xs: self.setArgs(jiterable(args)))


@jpype.JImplementationFor("it.unibo.tuprolog.core.Numeric")
class _KtNumeric:
    def __jclass_init__(cls):
        pass

    @property
    def int_value(self):
        return python_integer(self.getIntValue())

    @property
    def decimal_value(self):
        return python_decimal(self.getDecimalValue())

    def to_int(self):
        return self.int_value

    def to_float(self):
        return float(self.decimal_value)


@jpype.JImplementationFor("it.unibo.tuprolog.core.Integer")
class _KtInteger:
    def __jclass_init__(cls):
        pass

    @property
    def value(self):
        return self.int_value


@jpype.JImplementationFor("it.unibo.tuprolog.core.Real")
class _KtReal:
    def __jclass_init__(cls):
        pass

    @property
    def value(self):
        return self.decimal_value


@jpype.JImplementationFor("it.unibo.tuprolog.core.Recursive")
class _KtRecursive:
    def __jclass_init__(cls):
        Sized.register(cls)

    @property
    def lazily_unfolded(self):
        return self.getUnfoldedSequence()

    @property
    def unfolded(self):
        return self.getUnfoldedList()

    @property
    def __len__(self):
        return self.getSize()

    def to_iterable(self):
        return self.toSequence()


@jpype.JImplementationFor("it.unibo.tuprolog.core.Clause")
class _KtClause:
    def __jclass_init__(cls):
        pass

    def set_head_args(self, *args):
        return iterable_or_varargs(args, lambda xs: self.setHeadArgs(jiterable(args)))

    def insert_head_arg(self, index, argument):
        return self.setHeadArg(index, argument)

    def set_body_items(self, *args):
        return iterable_or_varargs(args, lambda xs: self.setBodyItems(jiterable(args)))


@jpype.JImplementationFor("it.unibo.tuprolog.core.Substitution")
class _KtSubstitution:
    def __jclass_init__(cls):
        pass

    def __add__(self, other):
        return self.plus(other)

    def __sub__(self, other):
        return self.minus(other)

    @jpype.JOverride
    def filter(self, filter):
        if isinstance(filter, Callable):
            return self.filter_(kfunction(1)(filter))
        else:
            return self.filter_(filter)


@jpype.JImplementationFor("it.unibo.tuprolog.core.Scope")
class _KtScope:
    def __jclass_init__(cls):
        pass

    def __contains__(self, item):
        return self.contains(item)

    def __getitem__(self, item):
        return self.get(item)

    def atom(self, string):
        return self.atomOf(string)

    def block(self, *terms):
        return iterable_or_varargs(terms, lambda ts: self.blockOf(jiterable(ts)))

    def clause(self, head=None, *body):
        return iterable_or_varargs(body, lambda bs: self.clauseOf(head, jiterable(bs)))

    def cons(self, head, tail=None):
        if tail is None:
            return self.listOf(head)
        else:
            return self.consOf(head, tail)

    def directive(self, *goals):
        return iterable_or_varargs(goals, lambda gs: self.directiveOf(jiterable(gs)))

    def fact(self, head):
        return self.factOf(head)

    def indicator(self, name, arity):
        return self.indicatorOf(name, arity)

    def integer(self, value):
        return self.intOf(big_integer(value))

    def real(self, value):
        return self.intOf(big_integer(value))

    def numeric(self, value):
        if isinstance(value, str):
            return self.numOf(value)
        if isinstance(value, int) or isinstance(value, BigInteger):
            return self.intOf(value)
        return self.realOf(value)

    def rule(self, head, *body):
        return iterable_or_varargs(body, lambda bs: self.ruleOf(head, jiterable(bs)))

    def struct(self, functor, *args):
        return iterable_or_varargs(args, lambda xs: self.structOf(functor, jiterable(xs)))

    def truth(self, value):
        return self.truthOf(value)

    def var(self, name):
        return self.varOf(name)

    def list(self, *items):
        return iterable_or_varargs(items, lambda xs: self.listOf(jiterable(xs)))

    def list_from(self, items, last=None):
        return self.listFrom(jiterable(items), last)

    def tuple(self, first, second, *others):
        return iterable_or_varargs(others, lambda os: self.tupleOf(jiterable([first, second] + list(os))))


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.core.*")
