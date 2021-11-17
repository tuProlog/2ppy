from decimal import Decimal
from types import ModuleType
from typing import Set, Tuple as PyTuple, Iterable

from tuprolog import logger
from tuprolog.core import Term, BigInteger, BigDecimal, TermConvertible, scope, Atom, Scope, Var
from tuprolog.jvmutils import jiterable

import sys


_MODULE_NAME = __name__


def _dsl_name(depth):
    return f"tuprolog.dsl.PythonDSL#{depth}"


class PythonDSL(ModuleType):

    def __init__(self, depth=0, parent=None, scope: Scope=scope()):
        super().__init__(_dsl_name(depth))
        self._scope = scope
        self._depth = depth
        self._parent = parent

    def _create_child(self):
        return PythonDSL(self._depth + 1, self)

    @property
    def _name(self):
        return _dsl_name(self._depth)

    def to_term(self, obj):
        if isinstance(obj, Term):
            return obj
        elif isinstance(obj, TermConvertible):
            return obj.to_term()
        elif isinstance(obj, str):
            if len(obj) >= 1 and (obj[0] == '_' or obj[0].isupper()):
                return self._scope.var(obj)
            else:
                return self._scope.atom(obj)
        elif isinstance(obj, int) or isinstance(obj, BigInteger):
            return self._scope.integer(obj)
        elif isinstance(obj, float) or isinstance(obj, Decimal) or isinstance(obj, BigDecimal):
            return self._scope.real(obj)
        elif isinstance(obj, bool):
            return self._scope.truth(obj)
        elif isinstance(obj, Set):
            return self._scope.block((self.to_term(it) for it in obj))
        elif isinstance(obj, PyTuple):
            return self._scope.logic_tuple((self.to_term(it) for it in obj))
        elif isinstance(obj, Iterable):
            return self._scope.list(jiterable((self.to_term(it) for it in obj)))
        else:
            raise ValueError(f"Cannot convert {obj} into {Term}")

    def __getattr__(self, item):
        return self.to_term(item)

    def __enter__(self):
        if _MODULE_NAME in sys.modules:
            del sys.modules[_MODULE_NAME]
        my_name = self._name
        if my_name in sys.modules:
            del sys.modules[my_name]
        child = self._create_child()
        sys.modules[child._name] = child
        Atom.__call__ = lambda this, *args: child._scope.struct(this.value, *args)
        Var.__call__ = lambda this, *args: child._scope.struct(this.name, *args)
        return child

    def __exit__(self, exc_type, exc_val, exc_tb):
        my_name = self._name
        if my_name in sys.modules:
            del sys.modules[my_name]
        parent = self._parent
        if parent is not None:
            sys.modules[parent._name] = parent
            Atom.__call__ = lambda this, *args: parent._scope.struct(this.value, *args)
            Var.__call__ = lambda this, *args: parent._scope.struct(this.name, *args)
        else:
            del Atom.__call__
            del Var.__call__


root_dsl = PythonDSL()

Atom.__call__ = lambda this, *args: root_dsl._scope.struct(this.value, *args)
Var.__call__ = lambda this, *args: root_dsl._scope.struct(this.name, *args)

sys.modules[_MODULE_NAME] = root_dsl

logger.debug("Configure Python DSL adapters for types in it.unibo.tuprolog.*")
