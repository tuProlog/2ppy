"""Python protocols and Pythonic methods for 2P-Kt's theories (see `tuprolog.theory.Theory`)."""

from collections.abc import Iterable, Sized

from jpype import JClass, JImplementationFor, JOverride

from tuprolog import logger
from tuprolog.core import Term
from tuprolog.core import indicator as new_indicator
from tuprolog.jvmutils import customize_derived, jiterable, jvm_method
from tuprolog.pyutils import iterable_or_varargs

_MutableTheory = JClass("it.unibo.tuprolog.theory.MutableTheory")


@JImplementationFor("it.unibo.tuprolog.theory.Theory")
@customize_derived("retract", "abolish", "equals", "to_string")
class _KtTheory:
    def __jclass_init__(cls):
        Sized.register(cls)

    def __len__(self):
        """The amount of clauses in the theory."""
        return self.getSize()

    def __add__(self, other):
        """The theory with the clauses of `other` (a theory, or a clause) appended."""
        return self.plus(other)

    def __contains__(self, item):
        """Whether `item` (a clause, a head, or an indicator like `f/2`) occurs in the theory."""
        return self.contains(item)

    def __getitem__(self, item):
        """The clauses unifying with a clause, or the rules whose head unifies with a structure,
        or the rules of an indicator, as a lazy iterable."""
        return self.get(item)

    def _assert(self, method, clause, *clauses):
        if len(clauses) == 0 and not isinstance(clause, Iterable):
            return method(clause)
        return iterable_or_varargs((clause,) + clauses, lambda cs: method(jiterable(list(cs))))

    def assert_a(self, clause, *clauses):
        """Adds clauses at the beginning of the theory, as Prolog's `asserta/1` does.

        Args:
            clause: A clause (or a structure, for a fact), or an iterable of them.
            *clauses: Further clauses, keeping their order.

        Returns:
            The resulting theory: a new one for immutable theories, this one for mutable ones.

        Raises:
            IllegalArgumentException: If some clause is not well-formed.
        """
        return self._assert(self.assertA, clause, *clauses)

    def assert_z(self, clause, *clauses):
        """Adds clauses at the end of the theory, as Prolog's `assertz/1` does.

        Args:
            clause: A clause (or a structure, for a fact), or an iterable of them.
            *clauses: Further clauses, keeping their order.

        Returns:
            The resulting theory: a new one for immutable theories, this one for mutable ones.

        Raises:
            IllegalArgumentException: If some clause is not well-formed.
        """
        return self._assert(self.assertZ, clause, *clauses)

    @JOverride
    def retract(self, clause, *clauses):
        """Removes the first clause unifying with each template, as Prolog's `retract/1` does.

        Args:
            clause: A clause template, a head (a structure, standing for any clause with a
                unifying head), or an iterable of clause templates.
            *clauses: Further clause templates.

        Returns:
            A `tuprolog.theory.RetractResult`: a success holding the resulting theory and the
            removed clauses, or a failure if no clause matched.
        """
        if len(clauses) == 0:
            if isinstance(clause, Iterable) and not isinstance(clause, Term):
                # a Python iterable would be ambiguous between the Iterable and Sequence overloads
                return self._retract(jiterable(clause))
            return self._retract(clause)
        return iterable_or_varargs((clause,) + clauses, lambda cs: self._retract(jiterable(cs)))

    def retract_all(self, clause):
        """Removes all the clauses unifying with a template (a clause, or a head).

        Returns:
            A `tuprolog.theory.RetractResult`, holding the resulting theory and the removed
            clauses.
        """
        return self.retractAll(clause)

    @JOverride
    def abolish(self, name=None, arity=None, indicator=None):
        """Removes all the clauses of a predicate, as Prolog's `abolish/1` does.

        The predicate is given either as `name` and `arity`, or as an indicator (e.g. `f/2`,
        see `tuprolog.core.indicator`, or the string `"f/2"`), passed as `indicator` or as `name`.

        Returns:
            The resulting theory: a new one for immutable theories, this one for mutable ones.

        Raises:
            ValueError: If neither a name nor an indicator is given.
            TypeError: If `name` is a string with no arity, given as `arity` or as `"name/arity"`.
        """
        if name is not None:
            if arity is not None:
                return self._abolish(new_indicator(name, arity))
            if isinstance(name, str):
                functor, slash, digits = name.rpartition("/")
                if not (slash and functor and digits.isdigit()):
                    raise TypeError("abolish(name) requires an arity, or a `name/arity` string")
                return self._abolish(new_indicator(functor, int(digits)))
            return self._abolish(name)
        elif indicator is not None:
            return self._abolish(indicator)
        raise ValueError("You should provide at least either a name-arity couple or an indicator")

    @JOverride
    def equals(self, other, use_var_complete_name=True):
        """Whether this theory and `other` have equal clauses, in the same order.

        Args:
            other: The other theory.
            use_var_complete_name: Whether variables are compared by their complete names (True,
                the default), or only by their names.
        """
        return self._equals(other, use_var_complete_name)

    def __eq__(self, other):
        """Whether the theories have equal clauses, in the same order (see `equals`)."""
        return self.equals(other, use_var_complete_name=True)

    def __hash__(self):
        # value-based equality: a mutable theory's hash would change with its clauses
        if isinstance(self, _MutableTheory):
            raise TypeError(f"unhashable type: '{type(self).__name__}'")
        return self.hashCode()

    def to_string(self, as_prolog_text=False):
        """The theory as a string: Prolog source code (a clause per line) if `as_prolog_text`."""
        # toString would resolve to java.lang.Object's, which precedes Theory in the MRO of some
        # classes
        return jvm_method(self, "toString")(as_prolog_text)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.theory.*")
