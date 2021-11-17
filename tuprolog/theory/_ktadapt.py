from tuprolog import logger
import jpype
from tuprolog.core import indicator as new_indicator
from tuprolog.jvmutils import jiterable, protect_iterable
from tuprolog.pyutils import iterable_or_varargs
from typing import Sized


@jpype.JImplementationFor("it.unibo.tuprolog.theory.Theory")
class _KtTheory:
    def __jclass_init__(cls):
        Sized.register(cls)

    @property
    def is_mutable(self):
        return self.isMutable()

    def to_mutable_theory(self):
        return self.toMutableTheory()

    def to_immutable_theory(self):
        return self.toImmutableTheory()

    @jpype.JOverride
    def getClauses(self):
        return protect_iterable(self.getClauses_())

    @property
    def clauses(self):
        return self.getClauses()

    @jpype.JOverride
    def getRules(self):
        return protect_iterable(self.getRules_())

    @property
    def rules(self):
        return self.getRules()

    @jpype.JOverride
    def getDirectives(self):
        return protect_iterable(self.getDirectives_())

    @property
    def directives(self):
        return self.getDirectives()

    def __len__(self):
        return self.getSize()

    def __add__(self, other):
        return self.plus(other)

    def __contains__(self, item):
        return self.contains(item)

    def __getitem__(self, item):
        return self.get(item)

    def _assert(self, method, clause, *clauses):
        if len(clauses) == 0:
            return method(clause)
        return iterable_or_varargs((clause,) + clauses, lambda cs: method(jiterable(cs)))

    def assert_a(self, clause, *clauses):
        self._assert(self.assertA, clause, *clauses)

    def assert_z(self, clause, *clauses):
        self._assert(self.assertZ, clause, *clauses)

    @jpype.JOverride
    def retract(self, clause, *clauses):
        if len(clauses) == 0:
            return self.retract_(clause)
        return iterable_or_varargs((clause,) + clauses, lambda cs: self.retract_(jiterable(cs)))

    def retract_all(self, clause):
        return self.retractAll(clause)

    @jpype.JOverride
    def abolish(self, name, arity=None, indicator=None):
        if name is not None:
            if arity is not None:
                return self.abolish_(new_indicator(name, arity))
            else:
                return self.abolish_(name)
        elif indicator is not None:
            return self.abolish_(indicator)
        raise ValueError("You should provide at least either a name-arity couple or an indicator")

    @jpype.JOverride
    def equals(self, other, use_var_complete_name=True):
        return self.equals_(other, use_var_complete_name)

    def __eq__(self, other):
        return self.equals(other, use_var_complete_name=True)

    def to_string(self, as_prolog_text=False):
        return self.toString(as_prolog_text)


@jpype.JImplementationFor("it.unibo.tuprolog.theory.RetractResult")
class _KtRetractResult:
    def __jclass_init__(cls):
        pass

    @property
    def is_success(self):
        return self.isSuccess()

    @property
    def is_failure(self):
        return self.isFailure()

    @property
    def theory(self):
        return self.getTheory()

    @property
    def clauses(self):
        return self.getClauses()

    @property
    def first_clause(self):
        return self.getFirstClause()


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.theory.*")
