from tuprolog import logger
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.sideffects as _sideffects  # type: ignore


SideEffect = _sideffects.SideEffect


ResetStaticKb = SideEffect.ResetStaticKb


AddStaticClauses = SideEffect.AddStaticClauses


RemoveStaticClauses = SideEffect.RemoveStaticClauses


ResetDynamicKb = SideEffect.ResetDynamicKb


AddDynamicClauses = SideEffect.AddDynamicClauses


RemoveDynamicClauses = SideEffect.RemoveDynamicClauses


SetFlags = SideEffect.SetFlags


ResetFlags = SideEffect.ResetFlags


ClearFlags = SideEffect.ClearFlags


LoadLibrary = SideEffect.LoadLibrary


UnloadLibraries = SideEffect.UnloadLibraries


UpdateLibrary = SideEffect.UpdateLibrary


AddLibraries = SideEffect.AddLibraries


ResetRuntime = SideEffect.ResetRuntime


SetOperators = SideEffect.SetOperators


ResetOperators = SideEffect.ResetOperators


RemoveOperators = SideEffect.RemoveOperators


OpenInputChannels = SideEffect.OpenInputChannels


ResetInputChannels = SideEffect.ResetInputChannels


CloseInputChannels = SideEffect.CloseInputChannels


OpenOutputChannels = SideEffect.OpenOutputChannels


ResetOutputChannels = SideEffect.ResetOutputChannels


CloseOutputChannels = SideEffect.CloseOutputChannels


SetPersistentData = SideEffect.SetPersistentData


SetDurableData = SideEffect.SetDurableData


SetEphemeralData = SideEffect.SetEphemeralData


SideEffectFactory = _sideffects.SideEffectFactory


DEFAULT_SIDE_EFFECT_FACTORY = SideEffectFactory.getDefault()


SideEffectManager = _sideffects.SideEffectManager


SideEffectsBuilder = _sideffects.SideEffectsBuilder


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.sideffects.*")
