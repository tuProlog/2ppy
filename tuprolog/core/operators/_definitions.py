import it.unibo.tuprolog.core.operators as _operators  # type: ignore
import jpype.imports  # noqa: F401

from tuprolog import logger

__all__ = [
    "DEFAULT_OPERATORS",
    "EMPTY_OPERATORS",
    "FX",
    "FY",
    "STANDARD_OPERATORS",
    "XF",
    "XFX",
    "XFY",
    "YF",
    "YFX",
    "Operator",
    "OperatorSet",
    "Specifier",
]


Operator = _operators.Operator
"""An operator declaration, letting a functor be written in prefix (e.g. `- 1`), infix (e.g.
`1 + 2`) or postfix notation, rather than as `functor(args)`.

An operator has a `functor` (e.g. `"+"`), a `specifier` (a `Specifier`, its position and
associativity, e.g. `YFX`), and a `priority`, from 1 to 1200: the lower, the tighter it binds (e.g.
`*` has priority 400 and `+` 500, so `1 + 2 * 3` is `1 + (2 * 3)`). Prolog declares operators with
the directive `:- op(Priority, Specifier, Functor).`

Build operators with `tuprolog.core.operators.operator`, or `Operator(functor, specifier,
priority)`. Members: `functor`, `specifier`, `priority`, `to_term()` (the term
`op(Priority, Specifier, Functor)`). Two operators are equal when their functor and specifier are,
regardless of their priority.

Examples:
    >>> from tuprolog.core.operators import *
    >>> op = operator("++", XFX, 700)
    >>> op, op.functor, op.priority, op.to_term()
    (Operator(700, XFX, '++'), '++', 700, op(700, xfx, '++'))

Note:
    2P-Kt's `it.unibo.tuprolog.core.operators.Operator`.
"""


OperatorSet = _operators.OperatorSet
"""An immutable set of operators, telling parsers and formatters which functors to read and write as
expressions.

Python protocols: it is a set of `Operator`s (`len`, `in`, iteration); `s1 + s2` adds operators
(those of `s2` replacing those of `s1` with the same functor and specifier), and `s1 - s2` removes
them (both also accept a single `Operator`).

Build operator sets with `tuprolog.core.operators.operator_set`, or use `DEFAULT_OPERATORS`,
`STANDARD_OPERATORS` and `EMPTY_OPERATORS`.

Examples:
    >>> from tuprolog.core.operators import *
    >>> custom = operator_set(operator("++", XFX, 700))
    >>> len(custom), operator("++", XFX, 700) in custom
    (1, True)
    >>> len(DEFAULT_OPERATORS + custom) == len(DEFAULT_OPERATORS) + 1
    True

Note:
    2P-Kt's `it.unibo.tuprolog.core.operators.OperatorSet`.
"""


Specifier = _operators.Specifier
"""The position and associativity of an operator, an enumeration.

`f` stands for the operator and `x`/`y` for its arguments: `x` is an argument of lower priority than
the operator, `y` one of lower or equal priority, so `y` marks the side the operator associates to.

| Prefix | Postfix | Infix | Associativity |
| ------ | ------- | ----- | ------------- |
| `FX`   | `XF`    | `XFX` | none          |
|        | `YF`    | `YFX` | left          |
| `FY`   |         | `XFY` | right         |

For instance, `-` is `YFX`, so `1 - 2 - 3` is `(1 - 2) - 3`. Members: `is_prefix`, `is_infix`,
`is_postfix`, `to_term()` (the atom, e.g. `xfx`), `values()` (all the specifiers).

Examples:
    >>> XFX.is_infix, FY.is_prefix, XFX.to_term()
    (True, True, xfx)

Note:
    2P-Kt's `it.unibo.tuprolog.core.operators.Specifier`.
"""


EMPTY_OPERATORS: OperatorSet = OperatorSet.EMPTY
"""The empty operator set: terms are parsed and written in canonical form only."""


DEFAULT_OPERATORS: OperatorSet = OperatorSet.DEFAULT
"""The default operator set, the same as `STANDARD_OPERATORS`, used by parsers and formatters unless
told otherwise.
"""


STANDARD_OPERATORS: OperatorSet = OperatorSet.STANDARD
"""The operators of ISO Prolog, e.g. `:-`, `,`, `;`, `->`, `=`, `is`, `<`, `+`, `-`, `*`, `/`,
`mod`.

Examples:
    >>> from tuprolog.core.operators import *
    >>> len(STANDARD_OPERATORS), operator("+", YFX, 500) in STANDARD_OPERATORS
    (40, True)
"""


XF: Specifier = Specifier.XF
"""The specifier of postfix, non-associative operators."""


YF: Specifier = Specifier.YF
"""The specifier of postfix, left-associative operators."""


FX: Specifier = Specifier.FX
"""The specifier of prefix, non-associative operators, e.g. `:-` in directives."""


FY: Specifier = Specifier.FY
"""The specifier of prefix, right-associative operators, e.g. `\\+` and unary `-`."""


XFX: Specifier = Specifier.XFX
"""The specifier of infix, non-associative operators, e.g. `=` and `is`."""


XFY: Specifier = Specifier.XFY
"""The specifier of infix, right-associative operators, e.g. `,` and `^`."""


YFX: Specifier = Specifier.YFX
"""The specifier of infix, left-associative operators, e.g. `+` and `*`."""


logger.debug("Loaded JVM classes from it.unibo.tuprolog.core.operators.*")
