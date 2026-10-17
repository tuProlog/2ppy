from typing import Mapping, Union, Iterable, Any
from tuprolog.core import Clause, Term
from tuprolog.pyutils import iterable_or_varargs, dict_or_keyword_args
from tuprolog.jvmutils import jlist, jmap
from tuprolog.core.operators import Operator
from tuprolog.solve.library import Library, libraries as new_libraries
from tuprolog.solve.channel import InputChannel, OutputChannel
from ._definitions import ResetStaticKb, AddStaticClauses, RemoveStaticClauses, ResetDynamicKb, AddDynamicClauses, \
    RemoveDynamicClauses, SetFlags, ResetFlags, ClearFlags, LoadLibrary, UnloadLibraries, UpdateLibrary, AddLibraries, \
    ResetRuntime, SetOperators, ResetOperators, RemoveOperators, OpenInputChannels, ResetInputChannels, \
    CloseInputChannels, OpenOutputChannels, ResetOutputChannels, CloseOutputChannels, SetPersistentData, SetDurableData, \
    SetEphemeralData


def _forward_iterable_or_varargs(callable, args, *callable_args):
    return iterable_or_varargs(args, lambda xs: callable(jlist(xs), *callable_args))


def _forward_dict_or_keywords(callable, dict, kwargs, *callable_args):
    return dict_or_keyword_args(dict, kwargs, lambda ds: callable(jmap(ds), *callable_args))


def reset_static_kb(*clauses: Union[Clause, Iterable[Clause]]) -> ResetStaticKb:
    return _forward_iterable_or_varargs(ResetStaticKb, clauses)


def add_static_clauses(*clauses: Union[Clause, Iterable[Clause]]) -> AddStaticClauses:
    return _forward_iterable_or_varargs(AddStaticClauses, clauses)


def remove_static_clauses(*clauses: Union[Clause, Iterable[Clause]]) -> RemoveStaticClauses:
    return _forward_iterable_or_varargs(RemoveStaticClauses, clauses)


def reset_dynamic_kb(*clauses: Union[Clause, Iterable[Clause]]) -> ResetDynamicKb:
    return _forward_iterable_or_varargs(ResetDynamicKb, clauses)


def add_dynamic_clauses(*clauses: Union[Clause, Iterable[Clause]]) -> AddDynamicClauses:
    return _forward_iterable_or_varargs(AddDynamicClauses, clauses)


def remove_dynamic_clauses(*clauses: Union[Clause, Iterable[Clause]]) -> RemoveDynamicClauses:
    return _forward_iterable_or_varargs(RemoveDynamicClauses, clauses)


def set_flags(flags: Mapping[str, Term] = {}, **kwargs: Term) -> SetFlags:
    return _forward_dict_or_keywords(SetFlags, flags, kwargs)


def reset_flags(flags: Mapping[str, Term] = {}, **kwargs: Term) -> ResetFlags:
    return _forward_dict_or_keywords(ResetFlags, flags, kwargs)


def clear_flags(*flag_names: str) -> ClearFlags:
    return _forward_iterable_or_varargs(ClearFlags, flag_names)


def load_library(alias: str, library: Library) -> LoadLibrary:
    return LoadLibrary(alias, library)


def unload_libraries(*aliases: str) -> UnloadLibraries:
    return _forward_iterable_or_varargs(UnloadLibraries, aliases)


def update_library(alias: str, library: Library) -> UpdateLibrary:
    return UpdateLibrary(alias, library)


def add_libraries(*libraries: Library) -> AddLibraries:
    return AddLibraries(new_libraries(libraries))


def reset_libraries(*libraries: Library) -> ResetRuntime:
    return ResetRuntime(new_libraries(libraries))


def set_operators(*operators: Union[Operator, Iterable[Operator]]) -> SetOperators:
    return _forward_iterable_or_varargs(SetOperators, operators)


def reset_operators(*operators: Union[Operator, Iterable[Operator]]) -> ResetOperators:
    return _forward_iterable_or_varargs(ResetOperators, operators)


def remove_operators(*operators: Union[Operator, Iterable[Operator]]) -> RemoveOperators:
    return _forward_iterable_or_varargs(RemoveOperators, operators)


def open_input_channels(
        channels: Mapping[str, InputChannel] = {},
        **kwargs: InputChannel
) -> OpenInputChannels:
    return _forward_dict_or_keywords(OpenInputChannels, channels, kwargs)


def reset_input_channels(
        channels: Mapping[str, InputChannel] = {},
        **kwargs: InputChannel
) -> ResetInputChannels:
    return _forward_dict_or_keywords(ResetInputChannels, channels, kwargs)


def close_input_channels(*names: Union[str, Iterable[str]]) -> CloseInputChannels:
    return _forward_iterable_or_varargs(CloseInputChannels, names)


def open_output_channels(
        channels: Mapping[str, OutputChannel] = {},
        **kwargs: OutputChannel
) -> OpenOutputChannels:
    return _forward_dict_or_keywords(OpenOutputChannels, channels, kwargs)


def reset_output_channels(
        channels: Mapping[str, OutputChannel] = {},
        **kwargs: OutputChannel
) -> ResetOutputChannels:
    return _forward_dict_or_keywords(ResetOutputChannels, channels, kwargs)


def close_output_channels(*names: Union[str, Iterable[str]]) -> CloseOutputChannels:
    return _forward_iterable_or_varargs(CloseOutputChannels, names)


def set_persistent_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SetPersistentData:
    return _forward_dict_or_keywords(SetPersistentData, data, kwargs, False)


def reset_persistent_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SetPersistentData:
    return _forward_dict_or_keywords(SetPersistentData, data, kwargs, True)


def set_durable_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SetDurableData:
    return _forward_dict_or_keywords(SetDurableData, data, kwargs, False)


def reset_durable_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SetDurableData:
    return _forward_dict_or_keywords(SetDurableData, data, kwargs, True)


def set_ephemeral_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SetEphemeralData:
    return _forward_dict_or_keywords(SetEphemeralData, data, kwargs, False)


def reset_ephemeral_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SetEphemeralData:
    return _forward_dict_or_keywords(SetEphemeralData, data, kwargs, True)
