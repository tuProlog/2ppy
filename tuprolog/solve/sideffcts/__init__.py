from functools import reduce

from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.sideffects import SideEffect
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.sideffects import SideEffectFactory
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.sideffects import SideEffectsBuilder

# noinspection PyUnresolvedReferences
from tuprolog.core import Clause, Term
# noinspection PyUnresolvedReferences
from tuprolog.core.operators import Operator, OperatorSet
# noinspection PyUnresolvedReferences
from tuprolog.solve.library import Library, AliasedLibrary, Libraries, libraries as new_libraries
# noinspection PyUnresolvedReferences
from tuprolog.solve.channel import InputChannel, OutputChannel
from tuprolog.pyutils import iterable_or_varargs, dict_or_keyword_args
from tuprolog.jvmutils import jlist, jmap

from typing import Mapping, Union, Iterable, Any


def _forward_iterable_or_varargs(callable, args, *callable_args):
    return iterable_or_varargs(args, lambda xs: callable(jlist(xs), *callable_args))


def _forward_dict_or_keywords(callable, dict, kwargs, *callable_args):
    return dict_or_keyword_args(dict, kwargs, lambda ds: callable(jmap(ds), *callable_args))


def reset_static_kb(*clauses: Union[Clause, Iterable[Clause]]) -> SideEffect.ResetStaticKb:
    return _forward_iterable_or_varargs(SideEffect.ResetStaticKb, clauses)


def add_static_clauses(*clauses: Union[Clause, Iterable[Clause]]) -> SideEffect.AddStaticClauses:
    return _forward_iterable_or_varargs(SideEffect.AddStaticClauses, clauses)


def remove_static_clauses(*clauses: Union[Clause, Iterable[Clause]]) -> SideEffect.RemoveStaticClauses:
    return _forward_iterable_or_varargs(SideEffect.RemoveStaticClauses, clauses)


def reset_dynamic_kb(*clauses: Union[Clause, Iterable[Clause]]) -> SideEffect.ResetDynamicKb:
    return _forward_iterable_or_varargs(SideEffect.ResetDynamicKb, clauses)


def add_dynamic_clauses(*clauses: Union[Clause, Iterable[Clause]]) -> SideEffect.AddDynamicClauses:
    return _forward_iterable_or_varargs(SideEffect.AddDynamicClauses, clauses)


def remove_dynamic_clauses(*clauses: Union[Clause, Iterable[Clause]]) -> SideEffect.RemoveDynamicClauses:
    return _forward_iterable_or_varargs(SideEffect.RemoveDynamicClauses, clauses)


def set_flags(flags: Mapping[str, Term] = {}, **kwargs: Term) -> SideEffect.SetFlags:
    return _forward_dict_or_keywords(SideEffect.SetFlags, flags, kwargs)


def reset_flags(flags: Mapping[str, Term] = {}, **kwargs: Term) -> SideEffect.ResetFlags:
    return _forward_dict_or_keywords(SideEffect.ResetFlags, flags, kwargs)


def clear_flags(*flag_names: str) -> SideEffect.ClearFlags:
    return _forward_iterable_or_varargs(SideEffect.ClearFlags, flag_names)


def load_library(alias: str, library: Library) -> SideEffect.LoadLibrary:
    return SideEffect.LoadLibrary(alias, library)


def unload_libraries(*aliases: str) -> SideEffect.UnloadLibraries:
    return _forward_iterable_or_varargs(SideEffect.UnloadLibraries, aliases)


def update_library(alias: str, library: Library) -> SideEffect.UpdateLibrary:
    return SideEffect.UpdateLibrary(alias, library)


def add_libraries(*libraries: Union[Libraries, AliasedLibrary]) -> SideEffect.AddLibraries:
    return SideEffect.AddLibraries(new_libraries(libraries))


def reset_libraries(*libraries: Union[Libraries, AliasedLibrary]) -> SideEffect.ResetLibraries:
    return SideEffect.ResetLibraries(new_libraries(libraries))


def set_operators(*operators: Union[Operator, Iterable[Operator]]) -> SideEffect.SetOperators:
    return _forward_iterable_or_varargs(SideEffect.SetOperators, operators)


def reset_operators(*operators: Union[Operator, Iterable[Operator]]) -> SideEffect.ResetOperators:
    return _forward_iterable_or_varargs(SideEffect.ResetOperators, operators)


def remove_operators(*operators: Union[Operator, Iterable[Operator]]) -> SideEffect.RemoveOperators:
    return _forward_iterable_or_varargs(SideEffect.RemoveOperators, operators)


def open_input_channels(
        channels: Mapping[str, InputChannel] = {},
        **kwargs: InputChannel
) -> SideEffect.OpenInputChannels:
    return _forward_dict_or_keywords(SideEffect.OpenInputChannels, channels, kwargs)


def reset_input_channels(
        channels: Mapping[str, InputChannel] = {},
        **kwargs: InputChannel
) -> SideEffect.ResetInputChannels:
    return _forward_dict_or_keywords(SideEffect.ResetInputChannels, channels, kwargs)


def close_input_channels(*names: Union[str, Iterable[str]]) -> SideEffect.CloseInputChannels:
    return _forward_iterable_or_varargs(SideEffect.CloseInputChannels, names)


def open_output_channels(
        channels: Mapping[str, OutputChannel] = {},
        **kwargs: OutputChannel
) -> SideEffect.OpenOutputChannels:
    return _forward_dict_or_keywords(SideEffect.OpenOutputChannels, channels, kwargs)


def reset_output_channels(
        channels: Mapping[str, OutputChannel] = {},
        **kwargs: OutputChannel
) -> SideEffect.ResetOutputChannels:
    return _forward_dict_or_keywords(SideEffect.ResetOutputChannels, channels, kwargs)


def close_output_channels(*names: Union[str, Iterable[str]]) -> SideEffect.CloseOutputChannels:
    return _forward_iterable_or_varargs(SideEffect.CloseOutputChannels, names)


def set_persistent_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SideEffect.SetPersistentData:
    return _forward_dict_or_keywords(SideEffect.SetPersistentData, data, kwargs, False)


def reset_persistent_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SideEffect.SetPersistentData:
    return _forward_dict_or_keywords(SideEffect.SetPersistentData, data, kwargs, True)


def set_durable_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SideEffect.SetDurableData:
    return _forward_dict_or_keywords(SideEffect.SetDurableData, data, kwargs, False)


def reset_durable_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SideEffect.SetDurableData:
    return _forward_dict_or_keywords(SideEffect.SetDurableData, data, kwargs, True)


def set_ephemeral_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SideEffect.SetEphemeralData:
    return _forward_dict_or_keywords(SideEffect.SetEphemeralData, data, kwargs, False)


def reset_ephemeral_data(
        data: Mapping[str, Any] = {},
        **kwargs: Any
) -> SideEffect.SetEphemeralData:
    return _forward_dict_or_keywords(SideEffect.SetEphemeralData, data, kwargs, True)


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.sideffects.*")
