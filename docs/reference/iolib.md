# IOLib

`IOLib` ([`tuprolog.solve.libs`](../api/tuprolog/solve/libs.md), alias `prolog.io`) is 2P-Kt's
library of ISO Prolog stream predicates. Solvers do not load it by default: pass it to the solver
factory.

```pycon
>>> import io
>>> from tuprolog.solve.libs import IOLib
>>> from tuprolog.solve.prolog import prolog_solver
>>> output = io.StringIO()
>>> solver = prolog_solver(libraries=IOLib, std_in=io.StringIO("hello(world). 42."), std_out=output)
>>> list(solver.query("read(X), read(Y), writeq('a b'), nl, write_canonical(1 + 2)"))
[{'X': hello(world), 'Y': 42}]
>>> print(output.getvalue())
'a b'
'+'(1, 2)

```

## Streams

A **stream** is a source of characters to read, or a sink to write characters to. Streams are
denoted by stream terms (`'$stream'(...)`), returned by `open/3,4`, or by alias atoms. Every solver
has a *current input* and a *current output* stream: initially its standard input and output
(aliases `user_input` and `user_output`), which are the channels given to the solver factory
(`std_in=`, `std_out=`, e.g. `io.StringIO`s or files), or Python's current `sys.stdin` and
`sys.stdout`.

| Predicate | Meaning |
|---|---|
| `open(Source, Mode, Stream)`, `open(Source, Mode, Stream, Options)` | open a file path or URL; `Mode` is `read`, `write` or `append`; options include `alias(A)` |
| `close(Stream)` | close a stream |
| `current_input(Stream)`, `current_output(Stream)` | the current input and output streams |
| `set_input(Stream)`, `set_output(Stream)` | change them |
| `stream_property(Stream, Property)` | enumerate the properties of streams (`input` or `output`, `alias(A)`, `type(text)`) |
| `at_end_of_stream`, `at_end_of_stream(Stream)` | whether a stream has no more characters |
| `flush_output(Stream)` | flush a stream's buffer |

Predicates without a `Stream` argument use the current input or output.

## Characters

| Predicate | Meaning |
|---|---|
| `get_char/1,2`, `get_code/1,2` | read the next character (as an atom of length 1), or its code; `end_of_file` or `-1` at the end |
| `peek_char/1,2`, `peek_code/1,2` | the same, without consuming the character |
| `put_char/1,2`, `put_code/1,2` | write a character, given as an atom or a code |
| `nl/1` | write a new line (`nl/0`, on the current output, is in the standard library) |

## Terms

| Predicate | Meaning |
|---|---|
| `read/1,2` | read a term, terminated by a full stop; fails at the end of the stream (rather than reading `end_of_file`) |
| `read_term/2,3` | read a term, with options |
| `write/2` | write a term (`write/1`, on the current output, is in the standard library) |
| `writeq/1,2` | write a term, quoting atoms where needed so that it can be read back |
| `write_canonical/1,2` | write a term quoting atoms and ignoring operators |
| `write_term/2,3` | write a term with options: `quoted(Bool)`, `ignore_ops(Bool)`, `numbervars(Bool)` |

## Theories

| Predicate | Meaning |
|---|---|
| `consult(Source)` | load the clauses of a file or URL into the knowledge base |
| `set_theory(Text)` | replace the knowledge base with the clauses in an atom |

## Limitations

- Binary streams are not supported: `get_byte/1,2`, `put_byte/1,2`, `peek_byte/1,2`, `close/2`,
  `char_conversion/2` and `current_char_conversion/2` raise a `system_error`.
- Writing (`open/3,4` with `write` or `append`) is only possible on local files.
- Python streams can be given to the solver as its standard channels; Prolog code cannot open
  Python streams by itself.

## See also

- [Read and write streams](../how-to/read-and-write-streams.md), a practical guide.
- 2P-Kt's [I/O library](https://tuprolog.github.io/2p-kt/reference/io-lib/) reference.
