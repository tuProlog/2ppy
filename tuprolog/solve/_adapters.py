from itertools import chain

from jpype import JImplementationFor, JOverride, JString

from tuprolog import logger
from tuprolog.jvmutils import customize_derived, jiterable
from tuprolog.pyutils import iterable_or_varargs


@JImplementationFor("it.unibo.tuprolog.solve.SolveOptions")
class _KtSolveOptions:
    _static_keys = ("lazy", "is_lazy", "eager", "is_eager", "timeout", "limit")

    @property
    def is_lazy(self):
        return self.isLazy()

    @property
    def is_eager(self):
        return self.isEager()

    @property
    def timeout(self):
        return self.getTimeout()

    @property
    def limit(self):
        return self.getLimit()

    @property
    def options(self):
        return self.getCustomOptions()

    def __len__(self):
        return len(_KtSolveOptions._static_keys) + len(self.options)

    def __iter__(self):
        return chain(_KtSolveOptions._static_keys, (str(key) for key in self.options))

    def __contains__(self, item):
        return item in _KtSolveOptions._static_keys or item in self.options

    def __getitem__(self, item):
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
        try:
            return self[item]
        except KeyError:
            return default

    def keys(self):
        return list(self)

    def values(self):
        return [self[key] for key in self]

    def items(self):
        return [(key, self[key]) for key in self]


def _goal(solver, goal):
    if isinstance(goal, (str, JString)):  # parsed with the solver's current operators
        from tuprolog.core.parsing import TermParser

        return TermParser.withOperators(solver.getOperators()).parse_struct(goal)
    return goal


@JImplementationFor("it.unibo.tuprolog.solve.Solver")
@customize_derived("solve", "solve_once")
class _KtSolver:
    @JOverride
    def solve(self, goal, options=None):
        """Solves a goal (a struct, or a string parsed with the solver's operators)."""
        goal = _goal(self, goal)
        if options is None:
            return self._solve(goal)
        elif options.is_eager:
            return list(self.solveList(goal, options))
        else:
            return self._solve(goal, options)

    @JOverride
    def solve_once(self, goal, options=None):
        goal = _goal(self, goal)
        if options is None:
            return self.solveOnce(goal)
        else:
            return self.solveOnce(goal, options)

    def query(self, goal, *, limit=None, timeout=None):
        """Yields the bindings of each solution of `goal` as a dict of Python values (see
        `Solution.to_dict`), and raises the exception of a solution that halts."""
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
    def __bool__(self):
        return bool(self.isYes())

    @property
    def bindings(self):
        """The terms bound to the query's named variables, by variable name."""
        if not self.isYes():
            return {}
        return {
            str(var.getName()): term
            for var, term in self.getSubstitution().items()
            if not var.isAnonymous()
        }

    def __getitem__(self, name):
        return self.bindings[name]

    def __contains__(self, name):
        return name in self.bindings

    def to_dict(self):
        """The values bound to the query's named variables, by variable name, as Python values
        where possible (see `tuprolog.core.to_python`)."""
        from tuprolog.core import to_python

        return {name: to_python(term) for name, term in self.bindings.items()}

    def raise_error(self):
        """Raises the exception of a halted solution, or returns the solution as it is."""
        if self.isHalt():
            raise self.getException()
        return self


@JImplementationFor("it.unibo.tuprolog.solve.MutableSolver")
@customize_derived("standard_output", "standard_input", "standard_error", "warnings")
class _KtMutableSolver:
    def load_static_clauses(self, *clauses):
        return iterable_or_varargs(clauses, lambda cs: self.loadStaticClauses(jiterable(list(cs))))

    def load_dynamic_clauses(self, *clauses):
        return iterable_or_varargs(clauses, lambda cs: self.loadDynamicClauses(jiterable(list(cs))))

    @property
    def standard_output(self):
        return self.getStandardOutput()

    @standard_output.setter
    def standard_output(self, channel):
        from tuprolog.solve import channel as _channel

        self.setStandardOutput(_channel.ensure_output_channel(channel, _channel.std_out))

    @property
    def standard_input(self):
        return self.getStandardInput()

    @standard_input.setter
    def standard_input(self, channel):
        from tuprolog.solve import channel as _channel

        self.setStandardInput(_channel.ensure_input_channel(channel, _channel.std_in))

    @property
    def standard_error(self):
        return self.getStandardError()

    @standard_error.setter
    def standard_error(self, channel):
        from tuprolog.solve import channel as _channel

        self.setStandardError(_channel.ensure_output_channel(channel, _channel.std_err))

    @property
    def warnings(self):
        return self.getWarnings()

    @warnings.setter
    def warnings(self, channel):
        from tuprolog.solve import channel as _channel

        self.setWarnings(_channel.ensure_output_channel(channel, _channel.warn))


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.*")
