"""The factory functions of side effects, re-exported by `tuprolog.solve.sideffects`."""

from collections.abc import Callable, Iterable, Mapping
from typing import Any

from tuprolog.core import Clause, Term
from tuprolog.core.operators import Operator
from tuprolog.jvmutils import jlist, jmap
from tuprolog.pyutils import dict_or_keyword_args, iterable_or_varargs
from tuprolog.solve.channel import InputChannel, OutputChannel
from tuprolog.solve.library import Library, aliased
from tuprolog.solve.library import libraries as new_libraries

from ._definitions import (
    AddDynamicClauses,
    AddLibraries,
    AddStaticClauses,
    ClearFlags,
    CloseInputChannels,
    CloseOutputChannels,
    LoadLibrary,
    OpenInputChannels,
    OpenOutputChannels,
    RemoveDynamicClauses,
    RemoveOperators,
    RemoveStaticClauses,
    ResetDynamicKb,
    ResetFlags,
    ResetInputChannels,
    ResetOperators,
    ResetOutputChannels,
    ResetRuntime,
    ResetStaticKb,
    SetDurableData,
    SetEphemeralData,
    SetFlags,
    SetOperators,
    SetPersistentData,
    UnloadLibraries,
    UpdateLibrary,
)

__all__ = [
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


def _forward_iterable_or_varargs(callable: Callable, args: Any, *callable_args: Any) -> Any:
    return iterable_or_varargs(args, lambda xs: callable(jlist(xs), *callable_args))


def _forward_dict_or_keywords(
    callable: Callable, dict: Any, kwargs: Any, *callable_args: Any
) -> Any:
    return dict_or_keyword_args(dict, kwargs, lambda ds: callable(jmap(ds), *callable_args))


def reset_static_kb(*clauses: Clause | Iterable[Clause]) -> ResetStaticKb:
    """Creates the side effect replacing the static knowledge base with the given clauses.

    Args:
        *clauses: The clauses (`tuprolog.core.Clause`), as varargs or as a single iterable.

    Returns:
        The `ResetStaticKb` side effect.
    """
    return _forward_iterable_or_varargs(ResetStaticKb, clauses)


def add_static_clauses(
    *clauses: Clause | Iterable[Clause], on_top: bool = False
) -> AddStaticClauses:
    """Creates the side effect adding clauses to the static knowledge base.

    Args:
        *clauses: The clauses (`tuprolog.core.Clause`), as varargs or as a single iterable.
        on_top: Whether to add them before the existing clauses, rather than after.

    Returns:
        The `AddStaticClauses` side effect.
    """
    return _forward_iterable_or_varargs(AddStaticClauses, clauses, on_top)


def remove_static_clauses(*clauses: Clause | Iterable[Clause]) -> RemoveStaticClauses:
    """Creates the side effect removing clauses from the static knowledge base.

    Args:
        *clauses: The clauses (`tuprolog.core.Clause`), as varargs or as a single iterable.

    Returns:
        The `RemoveStaticClauses` side effect.
    """
    return _forward_iterable_or_varargs(RemoveStaticClauses, clauses)


def reset_dynamic_kb(*clauses: Clause | Iterable[Clause]) -> ResetDynamicKb:
    """Creates the side effect replacing the dynamic knowledge base with the given clauses.

    Args:
        *clauses: The clauses (`tuprolog.core.Clause`), as varargs or as a single iterable.

    Returns:
        The `ResetDynamicKb` side effect.
    """
    return _forward_iterable_or_varargs(ResetDynamicKb, clauses)


def add_dynamic_clauses(
    *clauses: Clause | Iterable[Clause], on_top: bool = False
) -> AddDynamicClauses:
    """Creates the side effect adding clauses to the dynamic knowledge base, as `assertz/1` does.

    Args:
        *clauses: The clauses (`tuprolog.core.Clause`), as varargs or as a single iterable.
        on_top: Whether to add them before the existing clauses (as `asserta/1` does), rather
            than after.

    Returns:
        The `AddDynamicClauses` side effect.

    Examples:
        >>> from tuprolog.core import atom, fact
        >>> add_dynamic_clauses(fact(atom("a")), on_top=True)
        AddDynamicClauses(clauses=[a :- true], onTop=true)
    """
    return _forward_iterable_or_varargs(AddDynamicClauses, clauses, on_top)


def remove_dynamic_clauses(*clauses: Clause | Iterable[Clause]) -> RemoveDynamicClauses:
    """Creates the side effect removing clauses from the dynamic knowledge base.

    Args:
        *clauses: The clauses (`tuprolog.core.Clause`), as varargs or as a single iterable.

    Returns:
        The `RemoveDynamicClauses` side effect.
    """
    return _forward_iterable_or_varargs(RemoveDynamicClauses, clauses)


def set_flags(flags: Mapping[str, Term] = {}, **kwargs: Term) -> SetFlags:
    """Creates the side effect setting flags, keeping the other ones.

    Args:
        flags: The flags' values (terms), by name.
        **kwargs: More flags' values, by name.

    Returns:
        The `SetFlags` side effect.

    Examples:
        >>> from tuprolog.core import atom
        >>> set_flags(unknown=atom("fail"))
        SetFlags(flags={unknown=fail})
    """
    return _forward_dict_or_keywords(SetFlags, flags, kwargs)


def reset_flags(flags: Mapping[str, Term] = {}, **kwargs: Term) -> ResetFlags:
    """Creates the side effect replacing all the flags with the given ones.

    Args:
        flags: The flags' values (terms), by name.
        **kwargs: More flags' values, by name.

    Returns:
        The `ResetFlags` side effect.
    """
    return _forward_dict_or_keywords(ResetFlags, flags, kwargs)


def clear_flags(*flag_names: str) -> ClearFlags:
    """Creates the side effect removing the flags with the given names.

    Args:
        *flag_names: The names of the flags.

    Returns:
        The `ClearFlags` side effect.

    Examples:
        >>> clear_flags("my_flag", "other_flag")
        ClearFlags(names=[my_flag, other_flag])
    """
    return _forward_iterable_or_varargs(ClearFlags, flag_names)


def load_library(alias: str, library: Library) -> LoadLibrary:
    """Creates the side effect loading a library, under the given alias.

    Args:
        alias: The alias of the library, e.g. `my.lib`.
        library: The library (see `tuprolog.solve.library`).

    Returns:
        The `LoadLibrary` side effect.
    """
    return LoadLibrary(aliased(alias, library))


def unload_libraries(*aliases: str) -> UnloadLibraries:
    """Creates the side effect unloading the libraries with the given aliases.

    Args:
        *aliases: The aliases of the libraries, as varargs or as a single iterable.

    Returns:
        The `UnloadLibraries` side effect.
    """
    return _forward_iterable_or_varargs(UnloadLibraries, aliases)


def update_library(alias: str, library: Library) -> UpdateLibrary:
    """Creates the side effect replacing the loaded library with the given alias.

    Args:
        alias: The alias of the library to replace.
        library: The new library, loaded under `alias`.

    Returns:
        The `UpdateLibrary` side effect.
    """
    return UpdateLibrary(aliased(alias, library))


def add_libraries(*libraries: Library) -> AddLibraries:
    """Creates the side effect loading the given libraries.

    Args:
        *libraries: The libraries (see `tuprolog.solve.library`).

    Returns:
        The `AddLibraries` side effect.
    """
    return AddLibraries(new_libraries(libraries))


def reset_libraries(*libraries: Library) -> ResetRuntime:
    """Creates the side effect replacing all the loaded libraries with the given ones.

    Args:
        *libraries: The libraries (see `tuprolog.solve.library`).

    Returns:
        The `ResetRuntime` side effect.
    """
    return ResetRuntime(new_libraries(libraries))


def set_operators(*operators: Operator | Iterable[Operator]) -> SetOperators:
    """Creates the side effect adding operators, as `op/3` does.

    Args:
        *operators: The operators (`tuprolog.core.operators.Operator`), as varargs or as a single
            iterable.

    Returns:
        The `SetOperators` side effect.
    """
    return _forward_iterable_or_varargs(SetOperators, operators)


def reset_operators(*operators: Operator | Iterable[Operator]) -> ResetOperators:
    """Creates the side effect meant to replace all the operators with the given ones.

    Args:
        *operators: The operators (`tuprolog.core.operators.Operator`), as varargs or as a single
            iterable.

    Returns:
        The `ResetOperators` side effect.

    Note:
        In 2P-Kt 3.0, the side effect adds the operators to the existing ones instead.
    """
    return _forward_iterable_or_varargs(ResetOperators, operators)


def remove_operators(*operators: Operator | Iterable[Operator]) -> RemoveOperators:
    """Creates the side effect removing operators.

    Args:
        *operators: The operators (`tuprolog.core.operators.Operator`), as varargs or as a single
            iterable.

    Returns:
        The `RemoveOperators` side effect.
    """
    return _forward_iterable_or_varargs(RemoveOperators, operators)


def open_input_channels(
    channels: Mapping[str, InputChannel] = {}, **kwargs: InputChannel
) -> OpenInputChannels:
    """Creates the side effect adding input channels.

    Args:
        channels: The input channels (`tuprolog.solve.channel.InputChannel`), by alias.
        **kwargs: More input channels, by alias.

    Returns:
        The `OpenInputChannels` side effect.
    """
    return _forward_dict_or_keywords(OpenInputChannels, channels, kwargs)


def reset_input_channels(
    channels: Mapping[str, InputChannel] = {}, **kwargs: InputChannel
) -> ResetInputChannels:
    """Creates the side effect replacing all the input channels with the given ones.

    Args:
        channels: The input channels (`tuprolog.solve.channel.InputChannel`), by alias.
        **kwargs: More input channels, by alias.

    Returns:
        The `ResetInputChannels` side effect.
    """
    return _forward_dict_or_keywords(ResetInputChannels, channels, kwargs)


def close_input_channels(*names: str | Iterable[str]) -> CloseInputChannels:
    """Creates the side effect closing and removing the input channels with the given aliases.

    Args:
        *names: The aliases of the channels, as varargs or as a single iterable.

    Returns:
        The `CloseInputChannels` side effect.
    """
    return _forward_iterable_or_varargs(CloseInputChannels, names)


def open_output_channels(
    channels: Mapping[str, OutputChannel] = {}, **kwargs: OutputChannel
) -> OpenOutputChannels:
    """Creates the side effect adding output channels.

    Args:
        channels: The output channels (`tuprolog.solve.channel.OutputChannel`), by alias.
        **kwargs: More output channels, by alias.

    Returns:
        The `OpenOutputChannels` side effect.
    """
    return _forward_dict_or_keywords(OpenOutputChannels, channels, kwargs)


def reset_output_channels(
    channels: Mapping[str, OutputChannel] = {}, **kwargs: OutputChannel
) -> ResetOutputChannels:
    """Creates the side effect replacing all the output channels with the given ones.

    Args:
        channels: The output channels (`tuprolog.solve.channel.OutputChannel`), by alias.
        **kwargs: More output channels, by alias.

    Returns:
        The `ResetOutputChannels` side effect.
    """
    return _forward_dict_or_keywords(ResetOutputChannels, channels, kwargs)


def close_output_channels(*names: str | Iterable[str]) -> CloseOutputChannels:
    """Creates the side effect closing and removing the output channels with the given aliases.

    Args:
        *names: The aliases of the channels, as varargs or as a single iterable.

    Returns:
        The `CloseOutputChannels` side effect.
    """
    return _forward_iterable_or_varargs(CloseOutputChannels, names)


def set_persistent_data(data: Mapping[str, Any] = {}, **kwargs: Any) -> SetPersistentData:
    """Creates the side effect adding values to the persistent custom data.

    The persistent custom data lives as long as the solver (see `tuprolog.solve.data`); the given
    values replace those with the same keys.

    Args:
        data: The values, by key.
        **kwargs: More values, by key.

    Returns:
        The `SetPersistentData` side effect.
    """
    return _forward_dict_or_keywords(SetPersistentData, data, kwargs, False)


def reset_persistent_data(data: Mapping[str, Any] = {}, **kwargs: Any) -> SetPersistentData:
    """Creates the side effect replacing the persistent custom data with the given values.

    The persistent custom data lives as long as the solver (see `tuprolog.solve.data`).

    Args:
        data: The values, by key.
        **kwargs: More values, by key.

    Returns:
        The `SetPersistentData` side effect.

    Examples:
        >>> reset_persistent_data(counter=0)
        SetPersistentData(data={counter=0}, reset=true)
    """
    return _forward_dict_or_keywords(SetPersistentData, data, kwargs, True)


def set_durable_data(data: Mapping[str, Any] = {}, **kwargs: Any) -> SetDurableData:
    """Creates the side effect adding values to the durable custom data.

    The durable custom data lives during a query (see `tuprolog.solve.data`); the given
    values replace those with the same keys.

    Args:
        data: The values, by key.
        **kwargs: More values, by key.

    Returns:
        The `SetDurableData` side effect.
    """
    return _forward_dict_or_keywords(SetDurableData, data, kwargs, False)


def reset_durable_data(data: Mapping[str, Any] = {}, **kwargs: Any) -> SetDurableData:
    """Creates the side effect replacing the durable custom data with the given values.

    The durable custom data lives during a query (see `tuprolog.solve.data`).

    Args:
        data: The values, by key.
        **kwargs: More values, by key.

    Returns:
        The `SetDurableData` side effect.
    """
    return _forward_dict_or_keywords(SetDurableData, data, kwargs, True)


def set_ephemeral_data(data: Mapping[str, Any] = {}, **kwargs: Any) -> SetEphemeralData:
    """Creates the side effect adding values to the ephemeral custom data.

    The ephemeral custom data is the first to be discarded (see `tuprolog.solve.data`); the given
    values replace those with the same keys.

    Args:
        data: The values, by key.
        **kwargs: More values, by key.

    Returns:
        The `SetEphemeralData` side effect.
    """
    return _forward_dict_or_keywords(SetEphemeralData, data, kwargs, False)


def reset_ephemeral_data(data: Mapping[str, Any] = {}, **kwargs: Any) -> SetEphemeralData:
    """Creates the side effect replacing the ephemeral custom data with the given values.

    The ephemeral custom data is the first to be discarded (see `tuprolog.solve.data`).

    Args:
        data: The values, by key.
        **kwargs: More values, by key.

    Returns:
        The `SetEphemeralData` side effect.
    """
    return _forward_dict_or_keywords(SetEphemeralData, data, kwargs, True)
