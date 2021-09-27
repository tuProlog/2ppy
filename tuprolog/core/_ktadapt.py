from tuprolog import logger

import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.core.Term")
class _KtTerm:
    def __jclass_init__(self):
        pass

    def __getitem__(self, item, *items):
        return self.get(item, *items)

    @property
    def variables(self):
        return self.getVariables()


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
    def arity(self):
        return self.getArity()


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
