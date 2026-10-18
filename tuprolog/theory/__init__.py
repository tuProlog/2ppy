"""Logic theories, i.e. the knowledge bases of logic programs.

A *theory* is an ordered collection of clauses (see `tuprolog.core.Clause`):

- *facts*, stating what is true, e.g. `parent(abe, homer).`;
- *rules*, stating what is true provided that some conditions hold, e.g.
  `grandparent(X, Z) :- parent(X, Y), parent(Y, Z).` (the *head* holds if the *body* does);
- *directives*, i.e. goals to execute when a theory is loaded, e.g. `:- dynamic(counter/1).`.

A Prolog program is a theory, and solvers (see `tuprolog.solve`) answer queries against two of
them: a *static* knowledge base and a *dynamic* one, which `assert/1` and `retract/1` change.

Theories offer the usual Prolog operations on clauses: adding clauses at the beginning
(`assert_a`) or at the end (`assert_z`) of the theory, removing the first (`retract`) or every
(`retract_all`) clause unifying with a template, removing whole predicates (`abolish`), and
retrieving the clauses whose head may unify with a goal (`theory[goal]`). Clause order matters,
as Prolog tries clauses top-down.

Two independent choices distinguish theories, all sharing the `Theory` interface:

- *immutable* theories (`Theory`, built by `theory`) are persistent data structures: their
  operations return new theories, leaving the original one untouched; *mutable* ones
  (`MutableTheory`, built by `mutable_theory`) change in place, which is cheaper when clauses are
  asserted and retracted often;
- *indexed* theories (the default) store clauses in a structure indexed by functor, arity and
  first argument, making lookups fast at the cost of slower updates; *listed* ones (created by the
  JVM factories, e.g. `Theory.listedOf`) are plain lists of clauses.

Theories are mostly created by parsing Prolog text, see `tuprolog.theory.parsing`.

Examples:
    >>> from tuprolog.core import indicator, struct, var
    >>> from tuprolog.theory.parsing import parse_theory
    >>> kb = parse_theory("parent(abe, homer). parent(homer, bart).")
    >>> len(kb)
    2
    >>> list(kb[struct("parent", var("X"), "bart")])
    [parent(homer, bart) :- true]
    >>> indicator("parent", 2) in kb
    True
    >>> print(kb.assert_z(struct("parent", "bart", "maggie")).to_string(as_prolog_text=True))
    parent(abe, homer) :- true.
    parent(homer, bart) :- true.
    parent(bart, maggie) :- true.
    <BLANKLINE>

See Also:
    `tuprolog.collections`, for other collections of clauses; 2P-Kt's
    [clause database](https://tuprolog.github.io/2p-kt/explanation/clause-db-and-rete/)
    explanation.
"""

import tuprolog.theory._adapters as _

from ._api import *
from ._definitions import *

__all__ = ["MutableTheory", "RetractResult", "Theory", "mutable_theory", "theory"]
