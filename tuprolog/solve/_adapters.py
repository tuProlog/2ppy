from itertools import chain
from jpype import JImplementationFor, JOverride
from tuprolog import logger
from tuprolog.pyutils import iterable_or_varargs


@JImplementationFor("it.unibo.tuprolog.solve.SolveOptions")
class _KtSolveOptions:

    _static_keys = {'lazy', 'is_lazy', 'eager', 'is_eager', 'timeout', 'limit'}

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
        return self.getOptions()

    def __len__(self):
        return 4 + len(self.options)

    def __iter__(self):
        return chain(_KtSolveOptions._static_keys, self.options)

    def __contains__(self, item):
        return item in _KtSolveOptions._static_keys

    def __getitem__(self, item, default=None):
        if item in {'lazy', 'is_lazy'}:
            return self.is_lazy
        elif item in {'eager', 'is_eager'}:
            return self.is_eager
        elif item == 'timeout':
            return self.timeout
        elif item == 'limit':
            return self.limit
        elif item in self.options:
            return self.options[item]
        elif default is not None:
            return default
        return KeyError(f"No such option: {item}")


@JImplementationFor("it.unibo.tuprolog.solve.Solver")
class _KtSolver:
    def __jclass_init__(self):
        pass

    @JOverride
    def solve(self, goal, options=None):
        if options is None:
            return self.solve_(goal)
        elif options.is_eager:
            return self.solveList(goal, options)
        else:
            return self.solve_(goal, options)

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
        return iterable_or_varargs(clauses, lambda cs: self.loadStaticClauses(cs))

    def load_dynamic_clauses(self, *clauses):
        return iterable_or_varargs(clauses, lambda cs: self.loadDynamicClauses(cs))

    @property
    def standard_output(self):
        return self.getStandardOutput()

    @property
    def standard_input(self):
        return self.getStandardInput()

    @property
    def standard_error(self):
        return self.getStandardError()

    @property
    def warnings(self):
        return self.getWarnings()

    @standard_input.setter
    def standard_input(self, channel):
        return self.setStandardInput(channel)

    @standard_output.setter
    def standard_output(self, channel):
        return self.setStandardOutput(channel)

    @standard_error.setter
    def standard_error(self, channel):
        return self.setStandardError(channel)

    @warnings.setter
    def warnings(self, channel):
        return self.setWarnings(channel)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.*")
