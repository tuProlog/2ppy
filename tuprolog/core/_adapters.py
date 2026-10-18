from collections.abc import Sized

from jpype import JImplementationFor

from tuprolog import logger
from tuprolog.jvmutils import jiterable
from tuprolog.math import (
    BigDecimal,
    BigInteger,
    big_decimal,
    big_integer,
    python_decimal,
    python_integer,
)
from tuprolog.pyutils import iterable_or_varargs, register_single_value_type


@JImplementationFor("it.unibo.tuprolog.core.Term")
class _KtTerm:
    def __jclass_init__(cls):
        # e.g. struct("f", logic_list(...)) has one argument, the list
        register_single_value_type(cls)

    def __getitem__(self, item):
        """Indexes the term: `term[i]` is the `i`-th argument of a structure, `term[substitution]`
        applies a substitution, and `term[a, b, ...]` is `term[a][b]...`.

        Args:
            item: an argument index, a `tuprolog.core.Substitution`, or a tuple of them.

        Returns:
            The argument, or the term with the substitution applied.

        Examples:
            >>> from tuprolog.core import atom, struct, substitution, var
            >>> X = var("X")
            >>> t = struct("f", X, struct("g", "b"))
            >>> t[0], t[1, 0], t[substitution({X: atom("a")})]
            (X_..., b, f(a, g(b)))
        """
        if isinstance(item, tuple):
            # term[i, j, ...] is term[i][j]..., and term[s1, s2, ...] applies many substitutions
            result = self
            for index in item:
                result = result.get(index)
            return result
        return self.get(item)

    def fresh_copy(self, scope=None):
        """Copies the term, replacing each of its variables with a new one (consistently, i.e. the
        occurrences of a variable are replaced by the same new variable).

        Args:
            scope: a `tuprolog.core.Scope` to take the new variables from, by name. If `None`, new
                variables are created.

        Returns:
            The copy.

        Examples:
            >>> from tuprolog.core import struct, var
            >>> X = var("X")
            >>> t = struct("f", X, X)
            >>> copy = t.fresh_copy()
            >>> copy == t, copy.structurally_equals(t), copy[0] == copy[1]
            (False, True, True)
        """
        if scope is None:
            return self.freshCopy()
        else:
            return self.freshCopy(scope)


@JImplementationFor("it.unibo.tuprolog.core.Struct")
class _KtStruct:
    def __jclass_init__(cls):
        pass

    def insert_at(self, index, argument):
        """Returns a copy of the structure with an argument inserted.

        Args:
            index: the position of the new argument (0 for the first).
            argument: the new argument (a term, or a Python value converted by
                `tuprolog.core.to_term`).

        Returns:
            The new structure.

        Examples:
            >>> from tuprolog.core import atom, struct
            >>> struct("f", "a", "b").insert_at(1, atom("z")), struct("f", "a").insert_at(0, 1)
            (f(a, z, b), f(1, a))
        """
        from tuprolog.core import to_term

        return self.insertAt(index, to_term(argument))

    def set_args(self, *args):
        """Returns a copy of the structure with other arguments (and the same functor).

        Args:
            *args: the new arguments (terms, or Python values converted by `tuprolog.core.to_term`),
                either as many arguments or as a single iterable.

        Returns:
            The new structure.

        Examples:
            >>> from tuprolog.core import atom, struct
            >>> struct("f", "a").set_args(atom("x"), "y")
            f(x, y)
        """
        from tuprolog.core import to_term

        return iterable_or_varargs(
            args, lambda xs: self.setArgs(jiterable([to_term(x) for x in xs]))
        )


@JImplementationFor("it.unibo.tuprolog.core.Numeric")
class _KtNumeric:
    def __jclass_init__(cls):
        pass

    @property
    def int_value(self):
        """The value of the number as a Python `int` (reals are truncated towards zero)."""
        return python_integer(self.getIntValue())

    @property
    def decimal_value(self):
        """The value of the number as a `decimal.Decimal`, without loss of precision."""
        return python_decimal(self.getDecimalValue())

    def to_int(self):
        """Converts the number into a Python `int`, truncating reals towards zero.

        Returns:
            The value, as an `int`.

        Examples:
            >>> from tuprolog.core import integer, real
            >>> integer(42).to_int(), real(-2.5).to_int()
            (42, -2)
        """
        return self.int_value

    def to_float(self):
        """Converts the number into a Python `float`, possibly losing precision.

        Returns:
            The value, as a `float` (`inf` when too large).

        Examples:
            >>> from tuprolog.core import integer, real
            >>> integer(3).to_float(), real("0.1").to_float()
            (3.0, 0.1)
        """
        return float(self.decimal_value)


@JImplementationFor("it.unibo.tuprolog.core.Integer")
class _KtInteger:
    def __jclass_init__(cls):
        pass

    @property
    def value(self):
        """The value of the integer, as a Python `int`."""
        return self.int_value


@JImplementationFor("it.unibo.tuprolog.core.Real")
class _KtReal:
    def __jclass_init__(cls):
        pass

    @property
    def value(self):
        """The value of the real, as a `decimal.Decimal`."""
        return self.decimal_value


@JImplementationFor("it.unibo.tuprolog.core.Recursive")
class _KtRecursive:
    def __jclass_init__(cls):
        Sized.register(cls)

    @property
    def lazily_unfolded(self):
        """The items of the sequence, as a lazy iterable (for lists, including the final tail)."""
        return self.getUnfoldedSequence()

    @property
    def unfolded(self):
        """The items of the sequence, as a list (for lists, including the final tail, e.g. `[]`)."""
        return self.getUnfoldedList()

    def __len__(self):
        """The number of items (for partial lists, including the final tail)."""
        return self.getSize()

    def __iter__(self):
        """Iterates over the items (for partial lists, including the final tail; for well-formed
        lists, excluding the final `[]`).
        """
        return iter(self.toSequence())

    def to_iterable(self):
        """Returns the items, as an iterable (the same items `iter` gives).

        Returns:
            The items, as a lazy iterable.

        Examples:
            >>> from tuprolog.core import logic_list
            >>> list(logic_list(1, 2).to_iterable())
            [1, 2]
        """
        return self.toSequence()


@JImplementationFor("it.unibo.tuprolog.core.Clause")
class _KtClause:
    def __jclass_init__(cls):
        pass

    def set_head_args(self, *args):
        """Returns a copy of the clause, whose head has other arguments (and the same functor).

        Args:
            *args: the new arguments (terms, or Python values converted by `tuprolog.core.to_term`),
                either as many arguments or as a single iterable.

        Returns:
            The new clause.

        Examples:
            >>> from tuprolog.core import atom, rule, struct, var
            >>> X = var("X")
            >>> rule(struct("p", X), struct("q", X)).set_head_args(atom("a"))
            p(a) :- q(X_...)
        """
        return iterable_or_varargs(args, lambda xs: self.setHeadArgs(jiterable(xs)))

    def insert_head_arg(self, index, argument):
        """Returns a copy of the clause, whose head has an argument inserted.

        Args:
            index: the position of the new argument (0 for the first).
            argument: the new argument (a term, or a Python value converted by
                `tuprolog.core.to_term`).

        Returns:
            The new clause.

        Examples:
            >>> from tuprolog.core import atom, fact, struct
            >>> fact(struct("p", "a")).insert_head_arg(0, atom("z"))
            p(z, a) :- true
        """
        return self.insertHeadArg(index, argument)

    def set_body_items(self, *args):
        """Returns a copy of the clause, whose body consists of other goals.

        Args:
            *args: the new goals (terms), either as many arguments or as a single iterable; many
                goals are joined in a conjunction.

        Returns:
            The new clause.

        Examples:
            >>> from tuprolog.core import atom, fact, struct
            >>> fact(struct("p")).set_body_items(atom("q"), atom("r"))
            p :- (q, r)
        """
        return iterable_or_varargs(args, lambda xs: self.setBodyItems(jiterable(xs)))


@JImplementationFor("it.unibo.tuprolog.core.Substitution")
class _KtSubstitution:
    def __jclass_init__(cls):
        pass

    def __add__(self, other):
        """Merges two substitutions: `s1 + s2` has the assignments of both, and fails when they
        assign different values to a variable.

        Examples:
            >>> from tuprolog.core import atom, substitution, var
            >>> X, Y = var("X"), var("Y")
            >>> s = substitution({X: atom("a")})
            >>> len(s + substitution({Y: atom("b")})), (s + substitution({X: atom("b")})).is_failed
            (2, True)
        """
        return self.plus(other)

    def __sub__(self, other):
        """Removes assignments: `s - other` lacks the variables of `other`, a variable, an iterable
        of variables, or a substitution.

        Examples:
            >>> from tuprolog.core import atom, substitution, var
            >>> X, Y = var("X"), var("Y")
            >>> s = substitution({X: atom("a"), Y: atom("b")})
            >>> s - [X]
            {Y_...=b}
        """
        return self.minus(other)


@JImplementationFor("it.unibo.tuprolog.core.Scope")
class _KtScope:
    def __jclass_init__(cls):
        pass

    def __contains__(self, item):
        """Tells whether the scope created (or started with) a variable named `item`."""
        return self.contains(item)

    def __getitem__(self, item):
        """Returns the variable of the scope named `item`, or `None` if there is none (without
        creating it)."""
        return self.get(item)

    def atom(self, string):
        """Creates an atom (see `tuprolog.core.atom`).

        Args:
            string: the name of the atom.

        Returns:
            The atom.
        """
        return self.atomOf(string)

    def block(self, *terms):
        """Creates a block (see `tuprolog.core.block`).

        Args:
            *terms: the terms in the block, either as many arguments or as a single iterable.

        Returns:
            The block.
        """
        return iterable_or_varargs(terms, lambda ts: self.blockOf(jiterable(ts)))

    # clauseOf, directiveOf and ruleOf only have vararg overloads
    def clause(self, head=None, *body):
        """Creates a clause (see `tuprolog.core.clause`).

        Args:
            head: the head, or `None` for a directive.
            *body: the goals of the body, either as many arguments or as a single iterable.

        Returns:
            The clause.
        """
        return iterable_or_varargs(body, lambda bs: self.clauseOf(head, *bs))

    def cons(self, head, tail=None):
        """Creates a list cell `[head | tail]` (see `tuprolog.core.cons`).

        Args:
            head: the first item.
            tail: the rest of the list. If `None`, the list `[head]`.

        Returns:
            The list.
        """
        if tail is None:
            return self.logicListOf(head)
        else:
            return self.consOf(head, tail)

    def directive(self, *goals):
        """Creates a directive (see `tuprolog.core.directive`).

        Args:
            *goals: the goals, either as many arguments or as a single iterable.

        Returns:
            The directive.
        """
        return iterable_or_varargs(goals, lambda gs: self.directiveOf(*gs))

    def fact(self, head):
        """Creates a fact (see `tuprolog.core.fact`).

        Args:
            head: the head of the fact.

        Returns:
            The fact.
        """
        return self.factOf(head)

    def indicator(self, name, arity):
        """Creates an indicator `name/arity` (see `tuprolog.core.indicator`).

        Args:
            name: the name, as a string or a term.
            arity: the arity, as an int or a term.

        Returns:
            The indicator.
        """
        return self.indicatorOf(name, arity)

    def integer(self, value):
        """Creates an integer (see `tuprolog.core.integer`).

        Args:
            value: the value, as an `int`, a string of digits, or a `tuprolog.math.BigInteger`.

        Returns:
            The integer.
        """
        return self.intOf(big_integer(value))

    def real(self, value):
        """Creates a real (see `tuprolog.core.real`).

        Args:
            value: the value, as a `float`, a `decimal.Decimal`, a string, or a
                `tuprolog.math.BigDecimal`.

        Returns:
            The real.
        """
        if isinstance(value, BigDecimal):
            return self.realOf(value)
        return self.realOf(big_decimal(value))

    def numeric(self, value):
        """Creates a number, integer or real depending on `value` (see `tuprolog.core.numeric`).

        Args:
            value: the value, as an `int`, a `float`, a `decimal.Decimal`, or a string to parse.

        Returns:
            The number.
        """
        if isinstance(value, str):
            return self.numOf(value)
        if isinstance(value, (int, BigInteger)):
            return self.integer(value)
        return self.real(value)

    def rule(self, head, *body):
        """Creates a rule (see `tuprolog.core.rule`).

        Args:
            head: the head.
            *body: the goals of the body, either as many arguments or as a single iterable.

        Returns:
            The rule.
        """
        return iterable_or_varargs(body, lambda bs: self.ruleOf(head, *bs))

    def struct(self, functor, *args):
        """Creates a structure (see `tuprolog.core.struct`), without converting Python values.

        Args:
            functor: the name of the structure.
            *args: the arguments (terms), either as many arguments or as a single iterable.

        Returns:
            The structure.
        """
        return iterable_or_varargs(args, lambda xs: self.structOf(functor, jiterable(xs)))

    def truth(self, value):
        """Creates the atom `true` or `false` (see `tuprolog.core.truth`).

        Args:
            value: the truth value.

        Returns:
            The truth.
        """
        return self.truthOf(value)

    def var(self, name):
        """Returns the variable of the scope named `name`, creating it the first time.

        Args:
            name: the name of the variable (even `"_"` is remembered: call `anonymous()` for new
                anonymous variables).

        Returns:
            The variable.

        Examples:
            >>> from tuprolog.core import scope
            >>> s = scope()
            >>> s.var("X") == s.var("X"), s.anonymous() == s.anonymous()
            (True, False)
        """
        return self.varOf(name)

    def list(self, *items):
        """Creates a well-formed list (see `tuprolog.core.logic_list`), without converting Python
        values.

        Args:
            *items: the items (terms), either as many arguments or as a single iterable.

        Returns:
            The list.
        """
        return iterable_or_varargs(items, lambda xs: self.logicListOf(jiterable(xs)))

    def list_from(self, items, last=None):
        """Creates a list ending with a given tail (see `tuprolog.core.logic_list_from`).

        Args:
            items: the items (terms).
            last: the final tail. If `None`, the last item is the final tail.

        Returns:
            The list.
        """
        return self.logicListFrom(jiterable(items), last)

    def tuple(self, first, second, *others):
        """Creates a tuple, i.e. a conjunction (see `tuprolog.core.logic_tuple`).

        Args:
            first: the first item.
            second: the second item.
            *others: the other items, either as many arguments or as a single iterable.

        Returns:
            The tuple.
        """
        return iterable_or_varargs(
            others, lambda os: self.tupleOf(jiterable([first, second] + list(os)))
        )


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.core.*")
