# Read and write streams

2PPy accepts Python streams (`io.IOBase`: files, `sys.stdin`, `io.StringIO`, `io.BytesIO`, ...)
wherever 2P-Kt reads or writes: parsers read programs from them, and solvers read their input from
and write their output to them. Binary streams are UTF-8 encoded.

## Load a program from a file

`tuprolog.theory.parsing.read_theory` parses the clauses of a file, given as an open stream or as a
path:

```pycon
>>> import os
>>> import tempfile
>>> from tuprolog.theory.parsing import read_theory
>>> directory = tempfile.TemporaryDirectory()
>>> path = os.path.join(directory.name, "kb.pl")
>>> with open(path, "w") as file:
...     _ = file.write("parent(abe, homer).\nparent(homer, bart).\n")
>>> with open(path) as file:
...     kb = read_theory(file)
>>> len(kb), len(read_theory(path))
(2, 2)
>>> directory.cleanup()

```

`parse_theory` parses a string instead; `read_clauses` and `parse_clauses` give the clauses one at a
time. Strings passed to `read_*` functions are file paths, not Prolog text.

## Capture what a program writes

Solvers write on Python's current `sys.stdout` by default. Pass `std_out` (and `std_err`) to
redirect their output, e.g. to an `io.StringIO`:

```pycon
>>> import io
>>> from tuprolog.solve.prolog import prolog_solver
>>> output = io.StringIO()
>>> solver = prolog_solver(std_out=output)
>>> solver.solve_once("write(hello), nl, write([1, 2])").is_yes
True
>>> output.getvalue()
'hello\n[1, 2]'

```

Or pass any callable, wrapped by `tuprolog.solve.channel.output_channel`, which receives each piece
of text written:

```pycon
>>> from tuprolog.solve.channel import output_channel
>>> pieces = []
>>> solver = prolog_solver(std_out=output_channel(pieces.append))
>>> solver.solve_once("write(a), write(b), nl").is_yes
True
>>> pieces
['a', 'b', '\n']

```

!!! note
    Pass channels when creating the solver: assigning `solver.standard_output` (or
    `standard_input`, `standard_error`) afterwards has no effect, due to a 2P-Kt bug.

## Feed a program's input

`std_in` sets what `read/1`, `get_char/1` & co. read; here with IOLib, the library of ISO Prolog
stream predicates:

```pycon
>>> from tuprolog.solve.libs import IOLib
>>> solver = prolog_solver(libraries=IOLib, std_in=io.StringIO("likes(bart, skate). abc"))
>>> list(solver.query("read(Term), get_char(C)"))
[{'Term': likes(bart, skate), 'C': 'a'}]

```

## Collect warnings

Solvers report warnings, e.g. calls to undefined predicates, on the `warning` channel (Python's
`sys.stderr` by default). Collect them with a callable:

```pycon
>>> warnings = []
>>> solver = prolog_solver(warning=output_channel(lambda w: warnings.append(w.message)))
>>> solver.solve_once("undefined_predicate").is_no
True
>>> warnings
['No such a predicate: undefined_predicate/0']

```

## Use streams from Prolog

IOLib offers ISO Prolog's stream predicates: `open/3,4` and `close/1` (files, by path or URL),
`current_input/1`, `current_output/1`, `set_input/1`, `set_output/1`, character I/O
(`get_char/1,2`, `peek_char/1,2`, `put_char/1,2`, ...), term I/O (`read/1,2`, `write/2`,
`writeq/1,2`, `write_term/2,3`, ...), and `consult/1` to load the clauses of a file. See the
[IOLib reference](../reference/iolib.md):

```pycon
>>> output = io.StringIO()
>>> solver = prolog_solver(libraries=IOLib, std_out=output)
>>> solver.solve_once("current_output(S), writeq(S, 'hello world'), nl(S)").is_yes
True
>>> output.getvalue()
"'hello world'\n"

```

## Pass Python streams to JVM methods

JVM methods expecting streams (`java.io.InputStream`, `OutputStream`), readers or writers accept
Python streams as well: 2PPy converts them (see `tuprolog.jvmioutils`).

## See also

- Example notebook: [Input and output](../examples/05-input-and-output.ipynb).
- API: `tuprolog.theory.parsing` ([reference](../api/tuprolog/theory/parsing.md)),
  `tuprolog.solve.channel` ([reference](../api/tuprolog/solve/channel.md)),
  `tuprolog.solve.libs` ([reference](../api/tuprolog/solve/libs.md)),
  `tuprolog.jvmioutils` ([reference](../api/tuprolog/jvmioutils.md)).
- 2P-Kt's [I/O library](https://tuprolog.github.io/2p-kt/reference/io-lib/).
