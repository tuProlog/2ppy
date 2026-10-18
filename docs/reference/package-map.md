# Package map

2PPy's code lives in the `tuprolog` package, which mirrors the modules of 2P-Kt (see
[Relationship with 2P-Kt](../explanation/relationship-with-2p-kt.md)). Each sub-package
re-exports the JVM types of a 2P-Kt module under Pythonic names, and adds factory functions
(`snake_case`, with defaults and conversions of Python values) and Python protocols (iteration,
indexing, `len`, operators). Importing any of them starts the JVM (see
[Architecture](../explanation/architecture.md)).

## Logic data

| Package | Purpose | Main names |
|---|---|---|
| [`tuprolog.core`](../api/tuprolog/core.md) | Terms and clauses: the data model of logic programming. | `Term`, `Atom`, `Var`, `Struct`, `Integer`, `Real`, `List`, `Tuple`, `Clause`, `Rule`, `Fact`, `Substitution`, `Scope`; factories `atom`, `var`, `struct`, `integer`, `real`, `numeric`, `logic_list`, `logic_tuple`, `rule`, `fact`, `clause`, `substitution`, `scope`; conversions `to_term`, `to_python`; formatters |
| [`tuprolog.core.parsing`](../api/tuprolog/core/parsing.md) | Parsing terms and clauses from Prolog text. | `parse_term`, `parse_struct`, `parse_clause`, `parse_atom`, `parse_var`, ...; `read_term`, `read_terms`; `TermParser`, `TermReader`, `ParseException` |
| [`tuprolog.core.operators`](../api/tuprolog/core/operators.md) | Operators (prefix, infix, postfix functors such as `+` or `:-`), which drive parsing and formatting. | `Operator`, `OperatorSet`, `Specifier`; `operator`, `operator_set`, `specifier`; `DEFAULT_OPERATORS`, `STANDARD_OPERATORS`, `XFX`, `XFY`, `YFX`, `FX`, `FY`, `XF`, `YF` |
| [`tuprolog.core.exception`](../api/tuprolog/core/exception.md) | Exceptions of the term model. | `TuPrologException`, `SubstitutionException` |
| [`tuprolog.core.impl`](../api/tuprolog/core/impl.md) | Concrete implementations, for advanced uses. | `DefaultTermFormatter` |
| [`tuprolog.math`](../api/tuprolog/math.md) | Arbitrary-precision numbers backing numeric terms. | `BigInteger`, `BigDecimal`; `big_integer`, `big_decimal`, `python_integer`, `python_decimal` |
| [`tuprolog.unify`](../api/tuprolog/unify.md) | Unification of terms. | `Unificator`; `mgu`, `unify`, `match`; `strict_unificator`, `naive_unificator`, `cached_unificator`, `unificator` |
| [`tuprolog.unify.exception`](../api/tuprolog/unify/exception.md) | Unification failures. | `NoUnifyException`, `OccurCheckException` |
| [`tuprolog.theory`](../api/tuprolog/theory.md) | Theories: ordered, indexed collections of clauses (knowledge bases). | `Theory`, `MutableTheory`, `RetractResult`; `theory`, `mutable_theory` |
| [`tuprolog.theory.parsing`](../api/tuprolog/theory/parsing.md) | Parsing theories from Prolog source code. | `parse_theory`, `parse_clauses`, `read_theory`, `read_clauses`; `ClausesParser`, `ClausesReader` |
| [`tuprolog.collections`](../api/tuprolog/collections.md) | Other indexed collections of clauses: multisets and queues. | `ClauseMultiSet`, `ClauseQueue` (and mutable variants); `clause_multi_set`, `clause_queue` |

## Solving

| Package | Purpose | Main names |
|---|---|---|
| [`tuprolog.solve`](../api/tuprolog/solve.md) | The solver API, independent of the resolution strategy. | `Solver`, `MutableSolver`, `Solution`, `SolveOptions`, `Signature`, `ExecutionContext`; `solve_options`, `signature`, `yes_solution`, `no_solution`, `halt_solution` |
| [`tuprolog.solve.prolog`](../api/tuprolog/solve/prolog.md) | Prolog solvers (SLD resolution, as in ISO Prolog). | `prolog_solver` |
| [`tuprolog.solve.problog`](../api/tuprolog/solve/problog.md) | ProbLog solvers (probabilistic logic programming). | `problog_solver`, `PROBLOG_OPERATORS` |
| [`tuprolog.solve.plp`](../api/tuprolog/solve/plp.md) | Probabilistic utilities: probabilities of solutions, the probabilistic option. | `probability`, `set_probability`, `probabilistic`, `is_probabilistic`, `binary_decision_diagram` |
| [`tuprolog.solve.flags`](../api/tuprolog/solve/flags.md) | Prolog flags, i.e. named settings of solvers. | `FlagStore`, `Flag`, `NotableFlag`, `Unknown`, `MaxArity`, `DoubleQuotes`, ...; `flag_store`, `flag`; `DEFAULT_FLAG_STORE` |
| [`tuprolog.solve.channel`](../api/tuprolog/solve/channel.md) | Input and output channels of solvers (standard input, output, error, warnings). | `InputChannel`, `OutputChannel`, `InputStore`, `OutputStore`; `input_channel`, `output_channel`, `std_in`, `std_out`, `std_err`, `warn` |
| [`tuprolog.solve.library`](../api/tuprolog/solve/library.md) | Libraries: bundles of predicates, functions, clauses and operators; runtimes, i.e. sets of libraries. | `Library`, `Runtime`, `Pluggable`; `library`, `libraries`, `aliased` |
| [`tuprolog.solve.library.exception`](../api/tuprolog/solve/library/exception.md) | Errors of loading libraries. | `AlreadyLoadedLibraryException`, `NoSuchALibraryException` |
| [`tuprolog.solve.primitive`](../api/tuprolog/solve/primitive.md) | Primitives: predicates implemented in Python (or Kotlin). | `predicate`, `primitive`, `Primitive`, `AbstractPrimitive`, `SolveRequest`, `SolveResponse`; argument checks `ensuring_*` |
| [`tuprolog.solve.function`](../api/tuprolog/solve/function.md) | Logic functions, evaluated in arithmetic expressions. | `function`, `logic_function`, `LogicFunction`, `AbstractLogicFunction`, `ComputeRequest`, `ComputeResponse` |
| [`tuprolog.solve.libs`](../api/tuprolog/solve/libs.md) | Ready-made libraries: streams and I/O, Python objects. | `IOLib`, `OOPLib`, `oop_lib`, `SAFE_MODULES` |
| [`tuprolog.solve.stdlib`](../api/tuprolog/solve/stdlib.md) | The standard library loaded by default (see [Standard predicates](standard-predicates.md)). | `CommonBuiltins`, `CommonPrimitives`, `CommonRules`, `CommonFunctions`; sub-modules `primitive`, `rule`, `function` |
| [`tuprolog.solve.sideffects`](../api/tuprolog/solve/sideffects.md) | Side effects: the changes primitives make to solvers (e.g. adding clauses, setting flags). | `SideEffect` and its kinds; factories such as `add_dynamic_clauses`, `set_flags`, `load_library` |
| [`tuprolog.solve.data`](../api/tuprolog/solve/data.md) | Custom data attached to the state of solvers. | `CustomDataStore`; `custom_data`, `custom_data_store` |
| [`tuprolog.solve.exception`](../api/tuprolog/solve/exception.md) | Exceptions raised while solving: errors, halts, timeouts, warnings. | `ResolutionException`, `LogicError`, `HaltException`, `TimeOutException` |
| [`tuprolog.solve.exception.error`](../api/tuprolog/solve/exception/error.md) | ISO Prolog errors, one sub-package per family (`type`, `domain`, `existence`, `instantiation`, `permission`, `representation`, `evaluation`, `syntax`, `system`, `message`). | `TypeError`, `DomainError`, ...; factories such as `type_error_for_argument`, `existence_error` |
| [`tuprolog.solve.exception.warning`](../api/tuprolog/solve/exception/warning.md) | Warnings issued while solving. | `MissingPredicate`, `InitializationIssue` |

## Python integration and tools

| Package | Purpose | Main names |
|---|---|---|
| [`tuprolog`](../api/tuprolog.md) | The root package: starts the JVM on import. | `__version__`, `Info`, `JVM_VERSION`, `logger` |
| [`tuprolog.errors`](../api/tuprolog/errors.md) | Python exception classes classifying 2P-Kt's exceptions (see [Exceptions](exceptions.md)). | `TuPrologError`, `ParsingError`, `PrologError`, `PrologTypeError`, ... |
| [`tuprolog.jvmutils`](../api/tuprolog/jvmutils.md) | Bridging Python and JVM values: collections, iterables, functions. | `jlist`, `jmap`, `jiterable`, `ksequence`, `kfunction`, `jimplements`, `customize_derived` |
| [`tuprolog.jvmioutils`](../api/tuprolog/jvmioutils.md) | Bridging Python streams and JVM ones. | `ensure_input_stream`, `ensure_output_stream`, `ensure_reader`, `ensure_writer`, `open_file`, `PythonByteChannel` |
| [`tuprolog.pyutils`](../api/tuprolog/pyutils.md) | Pure-Python helpers. | `iterable_or_varargs`, `dict_or_keyword_args` |
| [`tuprolog.utils`](../api/tuprolog/utils.md) | General-purpose JVM interfaces of 2P-Kt's types. | `Castable`, `Taggable` |
| [`tuprolog.repl`](../api/tuprolog/repl.md) | Interactive shells: `python -m tuprolog.repl.prolog` and `python -m tuprolog.repl.problog`. | `PrologREPL` |

`python -m tuprolog` opens a Python shell with the whole API imported.
