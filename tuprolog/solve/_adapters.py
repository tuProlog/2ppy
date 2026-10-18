"""Pythonic adapters for the JVM types of `tuprolog.solve`.

They add, to the JVM types re-exported by `tuprolog.solve`:

- to `SolveOptions`: snake_case properties, and the read-only mapping protocol;
- to `Solver`: `solve` and `solve_once` accepting strings, and the Pythonic `query`;
- to `Solution`: truthiness, `bindings`, item access by variable name, and `to_dict`;
- to `MutableSolver`: clause loading from varargs, and assignable channel properties.
"""

from itertools import chain

from jpype import JImplementationFor, JOverride, JString

from tuprolog import logger
from tuprolog.jvmutils import customize_derived, jiterable
from tuprolog.pyutils import iterable_or_varargs


@JImplementationFor("it.unibo.tuprolog.solve.SolveOptions")
class _KtSolveOptions:
    """Makes `SolveOptions` a read-only mapping from option names to values.

    Its keys are `lazy`, `is_lazy`, `eager`, `is_eager`, `timeout`, `limit`, then the names of
    the custom options.

    Examples:
        >>> from tuprolog.solve import solve_options
        >>> options = solve_options(limit=3, my_option="x")
        >>> list(options)
        ['lazy', 'is_lazy', 'eager', 'is_eager', 'timeout', 'limit', 'my_option']
        >>> options["limit"], options.get("missing", 0), len(options)
        (3, 0, 7)
    """

    _static_keys = ("lazy", "is_lazy", "eager", "is_eager", "timeout", "limit")

    @property
    def is_lazy(self):
        """Whether solutions are computed one at a time, as the caller asks for them."""
        return self.isLazy()

    @property
    def is_eager(self):
        """Whether solutions are all computed before returning (the opposite of `is_lazy`)."""
        return self.isEager()

    @property
    def timeout(self):
        """The maximum duration of the resolution, in milliseconds (`MAX_TIMEOUT` if none)."""
        return self.getTimeout()

    @property
    def limit(self):
        """The maximum number of solutions (`ALL_SOLUTIONS` if none)."""
        return self.getLimit()

    @property
    def options(self):
        """The custom options, interpreted by specific solvers, as a JVM map by name."""
        return self.getCustomOptions()

    def __len__(self):
        """Returns the number of keys: the six standard ones, plus the custom options."""
        return len(_KtSolveOptions._static_keys) + len(self.options)

    def __iter__(self):
        """Iterates over the keys: the standard ones first, then the custom options' names."""
        return chain(_KtSolveOptions._static_keys, (str(key) for key in self.options))

    def __contains__(self, item):
        """Returns whether `item` is a standard key or the name of a custom option."""
        return item in _KtSolveOptions._static_keys or item in self.options

    def __getitem__(self, item):
        """Returns the value of the option named `item`.

        Args:
            item: A standard key (`lazy`, `is_lazy`, `eager`, `is_eager`, `timeout`, `limit`), or
                the name of a custom option.

        Returns:
            The value of the option.

        Raises:
            KeyError: If there is no such option.
        """
        if item in {"lazy", "is_lazy"}:
            return self.is_lazy
        elif item in {"eager", "is_eager"}:
            return self.is_eager
        elif item == "timeout":
            return self.timeout
        elif item == "limit":
            return self.limit
        elif item in self.options:
            return self.options[item]
        raise KeyError(f"No such option: {item}")

    def get(self, item, default=None):
        """Returns the value of the option named `item`, or `default` if there is none."""
        try:
            return self[item]
        except KeyError:
            return default

    def keys(self):
        """Returns the list of keys (see `__iter__`)."""
        return list(self)

    def values(self):
        """Returns the list of option values, in the order of `keys`."""
        return [self[key] for key in self]

    def items(self):
        """Returns the list of `(key, value)` pairs, in the order of `keys`."""
        return [(key, self[key]) for key in self]


def _goal(solver, goal):
    if isinstance(goal, (str, JString)):  # parsed with the solver's current operators
        from tuprolog.core.parsing import TermParser

        return TermParser.withOperators(solver.getOperators()).parse_struct(goal)
    return goal


@JImplementationFor("it.unibo.tuprolog.solve.Solver")
@customize_derived("solve", "solve_once")
class _KtSolver:
    """Lets `Solver`s solve goals given as strings, and adds the Pythonic `query`."""

    @JOverride
    def solve(self, goal, options=None):
        """Solves a goal, returning all its solutions.

        Args:
            goal: The goal, a `tuprolog.core.Struct`, or a string parsed with the solver's
                current operators.
            options: How to solve (see `tuprolog.solve.solve_options`); by default, lazily, with
                neither timeout nor limit.

        Returns:
            The `Solution`s: a lazy JVM sequence (iterable once) if `options` is lazy, or a list
            if it is eager. Every solution but the last is a *yes*; the last one may also be a
            *no* (no more solutions) or a *halt* (an error, or the timeout, stopped resolution).
            The sequence is infinite if the goal has infinitely many solutions and no limit.

        Examples:
            >>> from tuprolog.solve.prolog import prolog_solver
            >>> solutions = prolog_solver().solve("member(X, [1, 2])")
            >>> [(solution.is_yes, solution.to_dict()) for solution in solutions]
            [(True, {'X': 1}), (True, {'X': 2}), (False, {})]
        """
        goal = _goal(self, goal)
        if options is None:
            return self._solve(goal)
        elif options.is_eager:
            return list(self.solveList(goal, options))
        else:
            return self._solve(goal, options)

    @JOverride
    def solve_once(self, goal, options=None):
        """Solves a goal, returning its first solution only.

        Args:
            goal: The goal, a `tuprolog.core.Struct`, or a string parsed with the solver's
                current operators.
            options: How to solve (see `tuprolog.solve.solve_options`); its limit is ignored.

        Returns:
            The first `Solution`: a *yes*, a *no*, or a *halt*.

        Examples:
            >>> from tuprolog.solve.prolog import prolog_solver
            >>> prolog_solver().solve_once("atom_length(abc, N)")["N"]
            3
        """
        goal = _goal(self, goal)
        if options is None:
            return self.solveOnce(goal)
        else:
            return self.solveOnce(goal, options)

    def query(self, goal, *, limit=None, timeout=None):
        """Solves a goal the Pythonic way, yielding the variable bindings of its solutions.

        Solutions are computed lazily, one per iteration step; *no* solutions are skipped, so a
        goal that does not hold yields nothing, and a goal that holds without binding variables
        yields one empty dict per solution.

        Args:
            goal: The goal, a `tuprolog.core.Struct`, or a string parsed with the solver's
                current operators.
            limit: The maximum number of solutions; no limit if `None`.
            timeout: The maximum duration of the resolution, in milliseconds; none if `None`.

        Yields:
            For each *yes* solution, the values bound to the goal's named variables, as a dict
            of Python values where possible (see `Solution.to_dict`).

        Raises:
            tuprolog.solve.exception.ResolutionException: The exception of a *halt* solution,
                e.g. a logic error, or a `TimeOutException` when the timeout expires.

        Examples:
            >>> from tuprolog.solve.prolog import prolog_solver
            >>> solver = prolog_solver()
            >>> list(solver.query("append(X, Y, [1, 2])", limit=2))
            [{'X': [], 'Y': [1, 2]}, {'X': [1], 'Y': [2]}]
            >>> list(solver.query("1 > 2"))
            []
        """
        from tuprolog.solve import solve_options

        options = solve_options(lazy=True, **_present(limit=limit, timeout=timeout))
        for solution in self.solve(goal, options):
            if solution.is_halt:
                raise solution.exception
            if solution.is_yes:
                yield solution.to_dict()


def _present(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


@JImplementationFor("it.unibo.tuprolog.solve.Solution")
class _KtSolution:
    """Makes `Solution`s truthy if *yes*, and lets them map variable names to bound terms."""

    def __bool__(self):
        """Returns whether this is a *yes* solution."""
        return bool(self.isYes())

    @property
    def bindings(self):
        """The terms bound to the query's named variables, by variable name.

        Variables left unbound and anonymous variables (`_`) are left out; *no* and *halt*
        solutions have no bindings.
        """
        if not self.isYes():
            return {}
        return {
            str(var.getName()): term
            for var, term in self.getSubstitution().items()
            if not var.isAnonymous()
        }

    def __getitem__(self, name):
        """Returns the term bound to the variable named `name`.

        Raises:
            KeyError: If the query has no such named variable, or this is not a *yes*.
        """
        return self.bindings[name]

    def __contains__(self, name):
        """Returns whether the variable named `name` is among `bindings`."""
        return name in self.bindings

    def to_dict(self):
        """Returns the values bound to the query's named variables, as Python values.

        Returns:
            A dict from variable names to the bound terms, converted to Python values where
            possible (see `tuprolog.core.to_python`): e.g. numbers, strings for atoms, lists for
            logic lists. Empty for *no* and *halt* solutions.

        Examples:
            >>> from tuprolog.solve.prolog import prolog_solver
            >>> prolog_solver().solve_once("X = [1, a], Y = 2.5, Z = f(b)").to_dict()
            {'X': [1, 'a'], 'Y': 2.5, 'Z': f(b)}
        """
        from tuprolog.core import to_python

        return {name: to_python(term) for name, term in self.bindings.items()}

    def raise_error(self):
        """Raises the exception of a *halt* solution, or returns any other solution as it is.

        Returns:
            This solution, if it is a *yes* or a *no*.

        Raises:
            tuprolog.solve.exception.ResolutionException: The exception of a *halt* solution.

        Examples:
            >>> from tuprolog.solve.prolog import prolog_solver
            >>> prolog_solver().solve_once("X is 1 + 1").raise_error()["X"]
            2
        """
        if self.isHalt():
            raise self.getException()
        return self


@JImplementationFor("it.unibo.tuprolog.solve.MutableSolver")
@customize_derived("standard_output", "standard_input", "standard_error", "warnings")
class _KtMutableSolver:
    """Adds varargs clause loading, and assignable channel properties, to `MutableSolver`s."""

    def load_static_clauses(self, *clauses):
        """Replaces the static knowledge base with the given clauses.

        Args:
            *clauses: The clauses (`tuprolog.core.Clause`), as varargs or as a single iterable.
        """
        return iterable_or_varargs(clauses, lambda cs: self.loadStaticClauses(jiterable(list(cs))))

    def load_dynamic_clauses(self, *clauses):
        """Replaces the dynamic knowledge base with the given clauses.

        Args:
            *clauses: The clauses (`tuprolog.core.Clause`), as varargs or as a single iterable.
        """
        return iterable_or_varargs(clauses, lambda cs: self.loadDynamicClauses(jiterable(list(cs))))

    @property
    def standard_output(self):
        """The standard output channel, where predicates like `write/1` write.

        It can be assigned a `tuprolog.solve.channel.OutputChannel`, a Python stream, or a
        callable taking each string written (see `tuprolog.solve.channel.ensure_output_channel`);
        `None` means Python's `sys.stdout`.

        Note:
            Due to a bug of 2P-Kt 3.0.1, assigning this property has no effect: the getter keeps
            returning the previous channel, and predicates like `write/1` keep writing on the
            previous one. Pass the channel when creating the solver instead (e.g.
            `prolog_solver(std_out=...)`).
        """
        return self.getStandardOutput()

    @standard_output.setter
    def standard_output(self, channel):
        from tuprolog.solve import channel as _channel

        self.setStandardOutput(_channel.ensure_output_channel(channel, _channel.std_out))

    @property
    def standard_input(self):
        """The standard input channel, where reading predicates read.

        It can be assigned a `tuprolog.solve.channel.InputChannel`, a Python stream, or a
        callable returning a string at each call, or `None` at the end (see
        `tuprolog.solve.channel.ensure_input_channel`); `None` means Python's `sys.stdin`.

        Note:
            Due to a bug of 2P-Kt 3.0.1, assigning this property has no effect: the getter keeps
            returning the previous channel, and reading predicates keep reading from the
            previous one. Pass the channel when creating the solver instead (e.g.
            `prolog_solver(std_in=...)`).
        """
        return self.getStandardInput()

    @standard_input.setter
    def standard_input(self, channel):
        from tuprolog.solve import channel as _channel

        self.setStandardInput(_channel.ensure_input_channel(channel, _channel.std_in))

    @property
    def standard_error(self):
        """The standard error channel, for error messages.

        It can be assigned a `tuprolog.solve.channel.OutputChannel`, a Python stream, or a
        callable taking each string written; `None` means Python's `sys.stderr`.

        Note:
            Due to a bug of 2P-Kt 3.0.1, assigning this property has no effect: the getter keeps
            returning the previous channel, and errors keep being written on the
            previous one. Pass the channel when creating the solver instead (e.g.
            `prolog_solver(std_err=...)`).
        """
        return self.getStandardError()

    @standard_error.setter
    def standard_error(self, channel):
        from tuprolog.solve import channel as _channel

        self.setStandardError(_channel.ensure_output_channel(channel, _channel.std_err))

    @property
    def warnings(self):
        """The channel of warnings, e.g. those about calls to unknown predicates.

        It can be assigned a `tuprolog.solve.channel.OutputChannel`, a Python stream (on which
        each warning's message is written, one per line), or a callable taking each warning (a
        `tuprolog.solve.exception.Warning`); `None` means Python's `sys.stderr`.

        Examples:
            >>> import io
            >>> from tuprolog.solve.prolog import prolog_solver
            >>> solver = prolog_solver()
            >>> solver.warnings = buffer = io.StringIO()
            >>> solver.solve_once("undefined").is_no
            True
            >>> buffer.getvalue().strip()
            'No such a predicate: undefined/0'
        """
        return self.getWarnings()

    @warnings.setter
    def warnings(self, channel):
        from tuprolog.solve import channel as _channel

        self.setWarnings(_channel.ensure_output_channel(channel, _channel.warn))


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.*")
