"""The JVM types of side effects, re-exported by `tuprolog.solve.sideffects`."""

import it.unibo.tuprolog.solve.sideffects as _sideffects  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "DEFAULT_SIDE_EFFECT_FACTORY",
    "AddDynamicClauses",
    "AddLibraries",
    "AddStaticClauses",
    "ClearFlags",
    "CloseInputChannels",
    "CloseOutputChannels",
    "LoadLibrary",
    "OpenInputChannels",
    "OpenOutputChannels",
    "RemoveDynamicClauses",
    "RemoveOperators",
    "RemoveStaticClauses",
    "ResetDynamicKb",
    "ResetFlags",
    "ResetInputChannels",
    "ResetOperators",
    "ResetOutputChannels",
    "ResetRuntime",
    "ResetStaticKb",
    "SetDurableData",
    "SetEphemeralData",
    "SetFlags",
    "SetOperators",
    "SetPersistentData",
    "SideEffect",
    "SideEffectFactory",
    "SideEffectManager",
    "SideEffectsBuilder",
    "UnloadLibraries",
    "UpdateLibrary",
]


SideEffect = _sideffects.SideEffect
"""A change to the state of a solver, returned by a primitive along with a response.

The base class of all side effects, nested in it (e.g. `SideEffect.AddDynamicClauses`, also
re-exported by `tuprolog.solve.sideffects`). Its method `apply_to(context)` returns the
`tuprolog.solve.ExecutionContext` resulting from applying the side effect.
"""


ResetStaticKb = SideEffect.ResetStaticKb
"""The side effect replacing the static knowledge base with `clauses`.

Created by `reset_static_kb`.
"""


AddStaticClauses = SideEffect.AddStaticClauses
"""The side effect adding `clauses` to the static knowledge base, first if `on_top`.

Created by `add_static_clauses`.
"""


RemoveStaticClauses = SideEffect.RemoveStaticClauses
"""The side effect removing `clauses` from the static knowledge base.

Created by `remove_static_clauses`.
"""


ResetDynamicKb = SideEffect.ResetDynamicKb
"""The side effect replacing the dynamic knowledge base with `clauses`.

Created by `reset_dynamic_kb`.
"""


AddDynamicClauses = SideEffect.AddDynamicClauses
"""The side effect adding `clauses` to the dynamic knowledge base, first if `on_top`.

Created by `add_dynamic_clauses`.
"""


RemoveDynamicClauses = SideEffect.RemoveDynamicClauses
"""The side effect removing `clauses` from the dynamic knowledge base.

Created by `remove_dynamic_clauses`.
"""


SetFlags = SideEffect.SetFlags
"""The side effect setting `flags` (a map from names to terms), keeping the other flags.

Created by `set_flags`.
"""


ResetFlags = SideEffect.ResetFlags
"""The side effect replacing all the flags with `flags`.

Created by `reset_flags`.
"""


ClearFlags = SideEffect.ClearFlags
"""The side effect removing the flags with the given `names`.

Created by `clear_flags`.
"""


LoadLibrary = SideEffect.LoadLibrary
"""The side effect loading `library` into the solver.

Created by `load_library`.
"""


UnloadLibraries = SideEffect.UnloadLibraries
"""The side effect unloading the libraries with the given `aliases`.

Created by `unload_libraries`.
"""


UpdateLibrary = SideEffect.UpdateLibrary
"""The side effect replacing the loaded library with the alias of `library`.

Created by `update_library`.
"""


AddLibraries = SideEffect.AddLibraries
"""The side effect loading the `libraries` of a runtime into the solver.

Created by `add_libraries`.
"""


ResetRuntime = SideEffect.ResetRuntime
"""The side effect replacing all the loaded libraries with `libraries`.

Created by `reset_libraries`.
"""


SetOperators = SideEffect.SetOperators
"""The side effect adding `operators`, overriding those with the same symbol and notation.

Created by `set_operators`.
"""


ResetOperators = SideEffect.ResetOperators
"""The side effect meant to replace all the operators with `operators`.

Created by `reset_operators`.

Note:
    In 2P-Kt 3.0, it adds `operators` to the existing ones instead, like `SetOperators`.
"""


RemoveOperators = SideEffect.RemoveOperators
"""The side effect removing `operators`.

Created by `remove_operators`.
"""


OpenInputChannels = SideEffect.OpenInputChannels
"""The side effect adding input channels, by alias.

Created by `open_input_channels`.
"""


ResetInputChannels = SideEffect.ResetInputChannels
"""The side effect replacing all the input channels.

Created by `reset_input_channels`.
"""


CloseInputChannels = SideEffect.CloseInputChannels
"""The side effect closing and removing the input channels with the given `names`.

Created by `close_input_channels`.
"""


OpenOutputChannels = SideEffect.OpenOutputChannels
"""The side effect adding output channels, by alias.

Created by `open_output_channels`.
"""


ResetOutputChannels = SideEffect.ResetOutputChannels
"""The side effect replacing all the output channels.

Created by `reset_output_channels`.
"""


CloseOutputChannels = SideEffect.CloseOutputChannels
"""The side effect closing and removing the output channels with the given `names`.

Created by `close_output_channels`.
"""


SetPersistentData = SideEffect.SetPersistentData
"""The side effect adding `data` to the persistent custom data, or replacing it if `reset`.

Created by `set_persistent_data`.
"""


SetDurableData = SideEffect.SetDurableData
"""The side effect adding `data` to the durable custom data, or replacing it if `reset`.

Created by `set_durable_data`.
"""


SetEphemeralData = SideEffect.SetEphemeralData
"""The side effect adding `data` to the ephemeral custom data, or replacing it if `reset`.

Created by `set_ephemeral_data`.
"""


SideEffectFactory = _sideffects.SideEffectFactory
"""2P-Kt's factory of side effects, with one method per side effect (e.g. `add_dynamic_clauses`).

The functions of `tuprolog.solve.sideffects` are a more Pythonic alternative.
"""


DEFAULT_SIDE_EFFECT_FACTORY = SideEffectFactory.getDefault()
"""2P-Kt's default `SideEffectFactory`."""


SideEffectManager = _sideffects.SideEffectManager
"""A manager of the changes primitives make to the flow of resolution, i.e. the effects of cuts.

Primitives may attach one to their responses, to make resolution behave as if a cut (`!/0`) had
been executed, i.e. discarding pending alternatives.
"""


SideEffectsBuilder = _sideffects.SideEffectsBuilder
"""2P-Kt's builder of lists of side effects: a `SideEffectFactory` collecting what it creates.

Its `build()` method returns the side effects created so far, in order.
"""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.sideffects.*")
