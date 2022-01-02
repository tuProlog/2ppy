from decimal import Decimal
from tuprolog import logger
import jpype
from ._ktmath import big_integer, big_decimal, BigInteger, BigDecimal
from tuprolog.utils import *
from typing import Sized, Callable
from tuprolog.jvmutils import jiterable
from tuprolog.pyutils import iterable_or_varargs
from tuprolog.jvmutils import kfunction
from ._ktmath import *


@jpype.JImplementationFor("it.unibo.tuprolog.core.Term")
class _KtTerm:
    def __jclass_init__(cls):
        pass

    def __getitem__(self, item, *items):
        return self.get(item, *items)

    @property
    def variables(self):
        return self.getVariables()

    def structurally_equals(self, other):
        return self.structurallyEquals(other)

    @jpype.JOverride()
    def equals(self, other, use_var_complete_name: bool = True):
        return self.equals_(other, use_var_complete_name)

    @property
    def is_var(self):
        return self.isVar()

    @property
    def is_ground(self):
        return self.isGround()

    @property
    def is_struct(self):
        return self.isStruct()

    @property
    def is_truth(self):
        return self.isTruth()

    @property
    def is_recursive(self):
        return self.isRecursive()

    @property
    def is_atom(self):
        return self.isAtom()

    @property
    def is_constant(self):
        return self.isConstant()

    @property
    def is_number(self):
        return self.isNumber()

    @property
    def is_integer(self):
        return self.isInteger()

    @property
    def is_real(self):
        return self.isReal()

    @property
    def is_list(self):
        return self.isList()

    @property
    def is_tuple(self):
        return self.isTuple()

    @property
    def is_block(self):
        return self.isBlock()

    @property
    def is_clause(self):
        return self.isClause()

    @property
    def is_rule(self):
        return self.isRule()

    @property
    def is_fact(self):
        return self.isFact()

    @property
    def is_directive(self):
        return self.isDirective()

    @property
    def is_cons(self):
        return self.isCons()

    @property
    def is_empty_list(self):
        return self.isEmptyList()

    @property
    def is_true(self):
        return self.isTrue()

    @property
    def is_fail(self):
        return self.isFail()

    @property
    def is_indicator(self):
        return self.isIndicator()

    def fresh_copy(self, scope=None):
        if scope is None:
            return self.freshCopy()
        else:
            return self.freshCopy(scope)


@jpype.JImplementationFor("it.unibo.tuprolog.core.Struct")
class _KtStruct:
    def __jclass_init__(cls):
        pass

    @property
    def functor(self):
        return self.getFunctor()

    @property
    def args(self):
        return self.getArgs()

    @property
    def argsSequence(self):
        return self.getArgsSequence()

    @property
    def arity(self):
        return self.getArity()

    @property
    def is_functor_well_formed(self):
        return self.isFunctorWellFormed()

    @property
    def indicator(self):
        return self.getIndicator()

    def get_arg_at(self, index):
        return self.getArgAt(index)

    def add_last(self, argument):
        return self.addLast(argument)

    def add_first(self, argument):
        return self.addFirst(argument)

    def insert_at(self, index, argument):
        return self.addFirst(index, argument)

    def set_functor(self, functor):
        return self.setFunctor(functor)

    def set_args(self, *args):
        return iterable_or_varargs(args, lambda xs: self.setArgs(jiterable(args)))


@jpype.JImplementationFor("it.unibo.tuprolog.core.Var")
class _KtVar:
    def __jclass_init__(cls):
        pass

    @property
    def is_anonymous(self):
        return self.isAnonymous()

    @property
    def name(self):
        return self.getName()

    @property
    def id(self):
        return self.getId()

    @property
    def complete_name(self):
        return self.getCompleteName()

    @property
    def is_name_well_formed(self):
        return self.isNameWellFormed()


@jpype.JImplementationFor("it.unibo.tuprolog.core.Constant")
class _KtConstant:
    def __jclass_init__(cls):
        pass

    @property
    def value(self):
        return self.getValue()


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

    def to_list(self):
        return self.toList()

    def to_array(self):
        return self.toArray()


@jpype.JImplementationFor("it.unibo.tuprolog.core.List")
class _KtList:
    def __jclass_init__(cls):
        pass

    @property
    def is_well_formed(self):
        return self.isWellFormed()

    @property
    def last(self):
        return self.getLast()

    def estimated_length(self):
        return self.getEstimatedLength()


@jpype.JImplementationFor("it.unibo.tuprolog.core.Cons")
class _KtCons:
    def __jclass_init__(cls):
        pass

    @property
    def head(self):
        return self.getHead()

    @property
    def tail(self):
        return self.getTail()


@jpype.JImplementationFor("it.unibo.tuprolog.core.Tuple")
class _KtTuple:
    def __jclass_init__(cls):
        pass

    @property
    def left(self):
        return self.getLeft()

    @property
    def right(self):
        return self.getRight()


@jpype.JImplementationFor("it.unibo.tuprolog.core.Clause")
class _KtClause:
    def __jclass_init__(cls):
        pass

    @property
    def head(self):
        return self.getHead()

    @property
    def body(self):
        return self.getBody()

    @property
    def is_well_formed(self):
        return self.isWellFormed()

    @property
    def body_items(self):
        return self.getBodyItems()

    @property
    def body_size(self):
        return self.getBodySize()

    def get_body_item(self, index):
        return self.getBodyItem(index)

    def set_head(self, head):
        return self.setHead(head)

    def set_body(self, term):
        return self.setBody(term)

    def set_head_functor(self, functor):
        return self.setHeadFunctor(functor)

    def set_head_args(self, *args):
        return iterable_or_varargs(args, lambda xs: self.setHeadArgs(jiterable(args)))

    def insert_head_arg(self, index, argument):
        return self.setHeadArg(index, argument)

    def add_first_head_arg(self, argument):
        return self.addFirstHeadArg(argument)

    def add_last_head_arg(self, argument):
        return self.addLastHeadArg(argument)

    def append_head_arg(self, argument):
        return self.appendHeadArg(argument)

    def set_body_items(self, *args):
        return iterable_or_varargs(args, lambda xs: self.setBodyItems(jiterable(args)))

    def insert_body_item(self, index, item):
        return self.insertBodyItem(index, item)

    def add_first_body_item(self, item):
        return self.addFirstBodyItem(item)

    def add_last_body_item(self, item):
        return self.addLastBodyItem(item)

    def append_body_item(self, item):
        return self.appendBodyItem(item)


@jpype.JImplementationFor("it.unibo.tuprolog.core.Rule")
class _KtRule:
    def __jclass_init__(cls):
        pass

    @property
    def head_args(self):
        return self.getHeadArgs()

    @property
    def head_arity(self):
        return self.getHeadArity()

    def get_head_arg(self, index):
        return self.getHeadArg(index)


@jpype.JImplementationFor("it.unibo.tuprolog.core.TermConvertible")
class _KtTermConvertible:
    def __jclass_init__(cls):
        pass

    def to_term(self):
        return self.toTerm()


@jpype.JImplementationFor("it.unibo.tuprolog.core.Substitution")
class _KtSubstitution:
    def __jclass_init__(cls):
        pass

    @property
    def is_success(self):
        return self.isSuccess()

    @property
    def is_failed(self):
        return self.isFailed()

    def apply_to(self, term):
        return self.applyTo(term)

    def get_original(self, variable):
        return self.getOriginal(variable)

    def get_by_name(self, name):
        return self.getByName(name)

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

    @property
    def variables(self):
        return self.getVariables()

    @property
    def fail(self):
        return self.getFail()

    @property
    def empty_list(self):
        return self.getEmptyList()

    @property
    def empty_block(self):
        return self.getEmptyBlock()

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

    @property
    def anonymous(self):
        return self.getAnonymous()

    @property
    def whatever(self):
        return self.getWhatever()


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.core.*")
