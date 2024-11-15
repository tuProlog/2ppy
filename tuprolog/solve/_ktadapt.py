import sys
if sys.version_info < (3, 10):
    from collections import Mapping  # for Python 3.9 and earlier
else:
    from collections.abc import Mapping  # for Python 3.10 and later
from itertools import chain

from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype

from tuprolog.pyutils import iterable_or_varargs


@jpype.JImplementationFor("it.unibo.tuprolog.solve.SolverFactory")
class _KtSolverFactory:
    def __jclass_init__(self):
        pass


@jpype.JImplementationFor("it.unibo.tuprolog.solve.SolveOptions")
class _KtSolveOptions:

    _static_keys = {'lazy', 'is_lazy', 'eager', 'is_eager', 'timeout', 'limit'}

    def __jclass_init__(self):
        Mapping.register(self)

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


@jpype.JImplementationFor("it.unibo.tuprolog.solve.ExecutionContextAware")
class _KtExecutionContextAware:
    def __jclass_init__(self):
        pass

    @property
    def libraries(self):
        return self.getLibraries()

    @property
    def flags(self):
        return self.getFlags()

    @property
    def static_kb(self):
        return self.getStaticKb()

    @property
    def dynamic_kb(self):
        return self.getDynamicKb()

    @property
    def operators(self):
        return self.getOperators()

    @property
    def input_channels(self):
        return self.getInputChannles()

    @property
    def output_channels(self):
        return self.getOutputChannles()

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


@jpype.JImplementationFor("it.unibo.tuprolog.solve.Solver")
class _KtSolver:
    def __jclass_init__(self):
        pass

    @jpype.JOverride
    def solve(self, goal, options=None):
        if options is None:
            return self.solve_(goal)
        elif options.is_eager:
            return self.solveList(goal, options)
        else:
            return self.solve_(goal, options)

    @jpype.JOverride
    def solve_once(self, goal, options=None):
        if options is None:
            return self.solveOnce(goal)
        else:
            return self.solveOnce(goal, options)


@jpype.JImplementationFor("it.unibo.tuprolog.solve.MutableSolver")
class _KtMutableSolver:
    def __jclass_init__(self):
        pass

    def load_library(self, library):
        return self.loadLibrary(library)

    def unload_library(self, library):
        return self.unloadLibrary(library)

    def set_libraries(self, libraries):
        return self.setLibraries(libraries)

    def load_static_kb(self, theory):
        return self.loadStaticKb(theory)

    def load_static_clauses(self, *clauses):
        return iterable_or_varargs(clauses, lambda cs: self.loadStaticClauses(cs))

    def append_static_kb(self, theory):
        return self.appendStaticKb(theory)

    def reset_static_kb(self):
        return self.resetStaticKb()

    def load_dynamic_kb(self, theory):
        return self.loadDynamicKb(theory)

    def load_dynamic_clauses(self, *clauses):
        return iterable_or_varargs(clauses, lambda cs: self.loadDynamicClauses(cs))

    def append_dynamic_kb(self, theory):
        return self.appendDynamicKb(theory)

    def reset_dynamic_kb(self):
        return self.resetDynamicKb()

    def assert_a(self, clause):
        return self.assertA(clause)

    def assert_z(self, clause):
        return self.assertZ(clause)

    def retract_all(self, clause):
        return self.retractAll(clause)

    def set_flag(self, *args):
        return self.setFlag(*args)

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


@jpype.JImplementationFor("it.unibo.tuprolog.solve.Solution")
class _KtSolution:
    def __jclass_init__(self):
        pass

    @property
    def is_yes(self):
        return self.isYes()

    @property
    def is_no(self):
        return self.isNo()

    @property
    def is_halt(self):
        return self.isHalt()

    @property
    def substitution(self):
        return self.getSubstitution()

    @property
    def exception(self):
        return self.getExecption()

    @property
    def solved_query(self):
        return self.getSolvedQuery()

    def clean_up(self):
        return self.cleanUp()

    def value_of(self, variable):
        return self.valueOf(variable)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.*")
