from tuprolog import logger

import jpype

from tuprolog.pyutils import iterable_or_varargs


@jpype.JImplementationFor("it.unibo.tuprolog.core.Term")
class _KtTerm:
    def __jclass_init__(self):
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
        return self.is_integer()

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


@jpype.JImplementationFor("it.unibo.tuprolog.core.operators.Operator")
class _KtOperator:
    def __jclass_init__(self):
        pass

    @property
    def functor(self):
        return self.getFunctor()

    @property
    def specifier(self):
        return self.getSpecifier()

    @property
    def priority(self):
        return self.getPriority()


@jpype.JImplementationFor("it.unibo.tuprolog.core.Struct")
class _KtStruct:
    def __jclass_init__(self):
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
        return iterable_or_varargs(args, lambda xs: self.setArgs(args))


@jpype.JImplementationFor("it.unibo.tuprolog.core.Var")
class _KtConstant:
    def __jclass_init__(self):
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
    def __jclass_init__(self):
        pass

    @property
    def value(self):
        return self.getValue()


@jpype.JImplementationFor("it.unibo.tuprolog.core.Numeric")
class _KtNumeric:
    def __jclass_init__(self):
        pass

    @property
    def int_value(self):
        return self.getIntValue()

    @property
    def decimal_value(self):
        return self.getDecimalValue()


@jpype.JImplementationFor("it.unibo.tuprolog.core.Clause")
class _KtClause:
    def __jclass_init__(self):
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


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.core.*")
