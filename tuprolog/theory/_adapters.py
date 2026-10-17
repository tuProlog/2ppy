from typing import Sized
from jpype import JImplementationFor, JOverride
from tuprolog import logger
from tuprolog.core import indicator as new_indicator
from tuprolog.jvmutils import jiterable
from tuprolog.pyutils import iterable_or_varargs


@JImplementationFor("it.unibo.tuprolog.theory.Theory")
class _KtTheory:
    def __jclass_init__(cls):
        Sized.register(cls)

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

    @JOverride
    def retract(self, clause, *clauses):
        if len(clauses) == 0:
            return self.retract_(clause)
        return iterable_or_varargs((clause,) + clauses, lambda cs: self.retract_(jiterable(cs)))

    def retract_all(self, clause):
        return self.retractAll(clause)

    @JOverride
    def abolish(self, name, arity=None, indicator=None):
        if name is not None:
            if arity is not None:
                return self.abolish_(new_indicator(name, arity))
            else:
                return self.abolish_(name)
        elif indicator is not None:
            return self.abolish_(indicator)
        raise ValueError("You should provide at least either a name-arity couple or an indicator")

    @JOverride
    def equals(self, other, use_var_complete_name=True):
        return self.equals_(other, use_var_complete_name)

    def __eq__(self, other):
        return self.equals(other, use_var_complete_name=True)

    def to_string(self, as_prolog_text=False):
        return self.toString(as_prolog_text)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.theory.*")
