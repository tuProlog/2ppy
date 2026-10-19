# How the terminal IDE works

The terminal IDE (`2ppy-tui`, see [Use the terminal IDE](../how-to/use-the-terminal-ide.md)) holds
no logic of its own: what it shows, and what each command does, is decided by 2P-Kt's *GUI
core*, a model of an IDE for logic programs that does not depend on any graphical toolkit. The
same core runs behind tuProlog's other IDEs (e.g. 2P-Kt's Swing IDE), which is why they all
behave alike. This page explains how the terminal IDE drives it, following the "write once, wrap
elsewhere" principle of 2PPy (see [Architecture](architecture.md)).

```text
 Textual widgets: PrologTui (tuprolog.tui)       Python, on Textual's event loop
        │ actions (e.g. Solve)        ▲ snapshots of the state, effects
        ▼                             │
 GuiBridge: JvmGuiBridge (tuprolog.tui)          Python <-> JVM conversions
        │                             ▲
        ▼                             │
 GuiFacade (2PPy's Kotlin adapter)               actions in order; callbacks on JVM threads
        │                             ▲
        ▼                             │
 GUI core: GuiController, GuiState (2P-Kt)       pages, documents, solvers, resolutions
        │
        ▼
 2P-Kt's solvers
```

## State, actions and effects

The GUI core works as a loop with three notions:

- the *state* (`GuiState`, immutable): the open *pages*, each with a theory (its own text, for
  scratch pages, or that of a *document*, i.e. a file), a query, the resolution of the query (its
  solutions so far, and whether more may follow), the concluded resolutions, the standard input,
  output and error, the solver's warnings, the problems found in the theory, and what the solver
  holds (operators, flags, libraries, knowledge bases);
- *actions* (`GuiAction`): what the user asks for, e.g. editing a theory, or solving a query;
- *effects* (`GuiEffect`): what the core asks the user interface to do, as it cannot do it
  itself: asking for a file to open, or where to save one; reading or writing a file; asking
  whether to discard unsaved changes; copying to the clipboard; quitting.

The terminal IDE only *renders* each new state, *dispatches* an action for each command of the
user, and *fulfils* each effect, reporting its outcome as another action. For example, pressing
`F5` dispatches `Solve` (for the page shown); the core starts a resolution, and publishes a state
with the page's resolution running (the IDE enables `Stop`), then one with its first solution
(the IDE shows it, and turns `Solve` into `Next`). Saving a new file goes the other way round:
`ctrl+s` dispatches `RequestSave`; the core asks where to save it (an effect: the IDE shows a
dialog), then to write it (another effect: the IDE writes the file), and the IDE reports
`SaveSucceeded`, so that the core marks the document as saved (the IDE removes the `*` from the
page's title).

Commands the core does not know about are the IDE's own, and only change what it shows: e.g.
switching panels, or showing the documentation of a library's predicate.

## From the JVM to the screen

The GUI core is written in Kotlin, with coroutines: it runs on the JVM, inside the Python process
(see [Architecture](architecture.md)). `GuiFacade`, a Kotlin adapter of 2PPy, hides the coroutines
behind plain calls and callbacks: it applies the actions it is given one at a time, in order, and
calls back with each new state and effect, on JVM threads.

`JvmGuiBridge` converts what crosses this boundary. On each callback, it copies the parts of the
state the IDE shows into a *snapshot*: frozen Python dataclasses (`Snapshot`, `Page`,
`Resolution`, ...), which it posts to Textual's event loop. The widgets render snapshots only:
they never touch JVM objects, which belong to other threads, and they can be tested against a
fake bridge, without a JVM. Actions go the other way: the IDE's actions (e.g. `tuprolog.tui.Solve`)
are plain dataclasses too, converted into the core's ones when dispatched.

States may arrive faster than the screen renders them: the facade then skips the intermediate
ones, but never the latest. Effects, instead, are all delivered, in order.

## Editing while solving

Typing in the theory, the query or the standard input changes the widget at once, and dispatches
an action telling the core. Until the core publishes a state acknowledging the edit, the IDE keeps
what the user typed: an older state, published before the edit arrived, must not overwrite it. The
same holds when switching pages: edits still on their way to the core apply to the page they were
made on.

## Pages and solvers

Each page has its own solver, built as the command line asks (its *solver profile*: the dialect,
the libraries, the initial dynamic knowledge base, the unificator, the flags): the theory of the
page is its static knowledge base, and the clauses a query asserts go to its dynamic one, until
`Reset` builds the solver anew. Resolutions have a timeout (by default, that of the command line;
each page may change its own). By default, the resolutions of different pages run concurrently;
`--scheduling single` makes starting one stop the others.

The panels on the solver (operators, flags, libraries, knowledge bases) show what the core
inspects of it. Changing a flag changes the configuration of the page, which takes effect from
the next resolution. Adding an operator only writes an `op/3` directive at the end of the theory:
the solver reads it, as any directive, when loading the theory.

The core also tracks which panels have news the user has not seen: the IDE marks them with `●`,
and tells the core when it shows them.

## Syntax highlighting and documentation

Highlighting and documentation come from 2P-Kt too. Its `PrologSyntaxAnalyzer` (exported by
`tuprolog.gui`) classifies the tokens of a text (variables, functors, numbers, strings,
comments, ...), reading operators as the solver of the page knows them: the IDE colors each kind
with the colors of its theme. The libraries of a solver come with Markdown documentation of their
predicates, functions and operators, and flags with documentation of their own: the IDE previews
it with 2P-Kt's `documentation_preview`, and renders it in full in a dialog.

## The Docker image

The Docker image of each release is the minimum the IDE needs: a slim Python image, and the wheel
of 2PPy installed in it, with its dependencies (JPype, Textual, and `jdk4py`, which bundles the Java
runtime). No build tools are in it: no JDK, no Gradle, no uv. It runs `2ppy-tui` as an
unprivileged user, in `/work`. As the command line can only be given after the image name, every
option can also be given as a `TWOPPY_*` environment variable, which `docker run -e` sets.

## See also

- `tuprolog.gui`, the GUI core, for building other user interfaces on it.
- `tuprolog.tui`, the terminal IDE's API (e.g. `PrologTui`, `JvmGuiBridge`, `parse_command_line`).
- 2P-Kt's [documentation](https://tuprolog.github.io/2p-kt/), for its other IDEs.
