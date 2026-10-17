from itertools import chain

from jpype import JImplementationFor, JOverride

from tuprolog import logger
from tuprolog.jvmutils import jiterable
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


@JImplementationFor("it.unibo.tuprolog.solve.Solver")
class _KtSolver:
    def __jclass_init__(self):
        pass

    @JOverride
    def solve(self, goal, options=None):
        if options is None:
            return self._solve(goal)
        elif options.is_eager:
            return self.solveList(goal, options)
        else:
            return self._solve(goal, options)

    @JOverride
    def solve_once(self, goal, options=None):
        if options is None:
            return self.solveOnce(goal)
        else:
            return self.solveOnce(goal, options)


@JImplementationFor("it.unibo.tuprolog.solve.MutableSolver")
class _KtMutableSolver:
    def __jclass_init__(self):
        pass

    def load_static_clauses(self, *clauses):
        return iterable_or_varargs(clauses, lambda cs: self.loadStaticClauses(jiterable(list(cs))))

    def load_dynamic_clauses(self, *clauses):
        return iterable_or_varargs(clauses, lambda cs: self.loadDynamicClauses(jiterable(list(cs))))

    @property
    def standard_output(self):
        return self.getStandardOutput()

    @standard_output.setter
    def standard_output(self, channel):
        return self.setStandardOutput(channel)

    @property
    def standard_input(self):
        return self.getStandardInput()

    @standard_input.setter
    def standard_input(self, channel):
        return self.setStandardInput(channel)

    @property
    def standard_error(self):
        return self.getStandardError()

    @standard_error.setter
    def standard_error(self, channel):
        return self.setStandardError(channel)

    @property
    def warnings(self):
        return self.getWarnings()

    @warnings.setter
    def warnings(self, channel):
        return self.setWarnings(channel)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.*")
