from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.ResolutionException")
class _KtResolutionException:
    def __jclass_init__(self):
        pass

    @property
    def contexts(self):
        return self.getContexts()

    @property
    def context(self):
        return self.getContext()

    @property
    def logic_stack_trace(self):
        return self.getLogicStackTrace()

    def push_context(self, context):
        return self.pushContext(context)

    def update_last_context(self, context):
        return self.updateLastContext(context)

    def update_context(self, context, index=None):
        if index is None:
            return self.updateContext(context)
        else:
            return self.updateContext(context, index)


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.LogicError")
class _KtLogicError:
    def __jclass_init__(self):
        pass

    @property
    def type(self):
        return self.getType()

    @property
    def extra_data(self):
        return self.getExtraData()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.HaltException")
class _KtHaltException:
    def __jclass_init__(self):
        pass

    @property
    def exit_status(self):
        return self.getExitStatus()


@jpype.JImplementationFor("it.unibo.tuprolog.solve.exception.TimeOutException")
class _KtTimeOutException:
    def __jclass_init__(self):
        pass

    @property
    def exceeded_duration(self):
        return self.getExceededDuration()


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.solve.exception.*")
