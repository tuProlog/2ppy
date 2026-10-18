"""Side effects: the changes primitives make to the state of solvers.

*Primitives* (predicates implemented in Python, see `tuprolog.solve.primitive`) never change the
state of the solver running them directly: the state they see (an
`tuprolog.solve.ExecutionContext`) is immutable. Instead, along with each response, they return
*side effects*, i.e. descriptions of changes, which the solver applies in order. This is how,
e.g., `assertz/1` adds clauses to the dynamic knowledge base.

Each side effect changes one part of the state, either replacing it (*reset*) or adding to and
removing from it:

- knowledge bases: `reset_static_kb`, `add_static_clauses`, `remove_static_clauses`, and the same
  for the dynamic knowledge base;
- flags: `set_flags`, `reset_flags`, `clear_flags`;
- libraries: `load_library`, `unload_libraries`, `update_library`, `add_libraries`,
  `reset_libraries`;
- operators: `set_operators`, `reset_operators`, `remove_operators`;
- channels: `open_input_channels`, `reset_input_channels`, `close_input_channels`, and the same
  for output channels;
- custom data (see `tuprolog.solve.data`): `set_persistent_data`, `reset_persistent_data`, and
  the same for durable and ephemeral data.

These functions create instances of the `SideEffect` subclasses of the same names (e.g.
`AddDynamicClauses`); `DEFAULT_SIDE_EFFECT_FACTORY` and `SideEffectsBuilder` are 2P-Kt's own
factories of them.

Examples:
    A primitive `remember/1` adding a fact `seen(X)` to the dynamic knowledge base:

    >>> from tuprolog.core import fact, struct
    >>> from tuprolog.solve.library import library
    >>> from tuprolog.solve.primitive import primitive
    >>> from tuprolog.solve.prolog import prolog_solver
    >>> @primitive
    ... def remember(request):
    ...     seen = fact(struct("seen", request.arguments[0]))
    ...     yield request.reply_success(None, add_dynamic_clauses(seen))
    >>> solver = prolog_solver(libraries=library("my.lib", primitives={"remember/1": remember}))
    >>> solver.solve_once("remember(a), remember(b)").is_yes
    True
    >>> list(solver.query("seen(X)"))
    [{'X': 'a'}, {'X': 'b'}]

See Also:
    - `tuprolog.solve.primitive`, for writing primitives.
    - 2P-Kt's [primitives and functions](
      https://tuprolog.github.io/2p-kt/reference/primitives-and-functions/).
"""

from ._api import *
from ._definitions import *

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
    "add_dynamic_clauses",
    "add_libraries",
    "add_static_clauses",
    "clear_flags",
    "close_input_channels",
    "close_output_channels",
    "load_library",
    "open_input_channels",
    "open_output_channels",
    "remove_dynamic_clauses",
    "remove_operators",
    "remove_static_clauses",
    "reset_durable_data",
    "reset_dynamic_kb",
    "reset_ephemeral_data",
    "reset_flags",
    "reset_input_channels",
    "reset_libraries",
    "reset_operators",
    "reset_output_channels",
    "reset_persistent_data",
    "reset_static_kb",
    "set_durable_data",
    "set_ephemeral_data",
    "set_flags",
    "set_operators",
    "set_persistent_data",
    "unload_libraries",
    "update_library",
]
