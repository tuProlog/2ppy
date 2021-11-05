from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.solve.SolverFactory")
class _KtSolverFactory:
    def __jclass_init__(self):
        pass


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
