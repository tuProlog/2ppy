# Use the terminal IDE

2PPy comes with *2ppy TUI*, a terminal IDE (a *text user interface*, TUI) for Prolog, built with
[Textual](https://textual.textualize.io/). It runs in any terminal, also over SSH, and mirrors
2P-Kt's Swing IDE: the same pages, controls and panels. You can run it in your own Python
environment, or with Docker, without installing anything else. [How the terminal IDE
works](../explanation/terminal-ide.md) explains what happens behind its screen.

## Install and start it locally

The terminal IDE is part of the `2ppy` package: it needs Python 3.10 or later, and nothing else
(no Java installation: the package bundles a Java runtime). Either install it as a command of its
own, in an environment of its own:

```bash
uv tool install 2ppy        # or: pipx install 2ppy
2ppy-tui
```

or run it without installing it:

```bash
uvx --from 2ppy 2ppy-tui
```

or install `2ppy` in the environment of your project, then start the IDE from there:

```bash
pip install 2ppy            # or: uv add 2ppy
2ppy-tui                    # or: python -m tuprolog.tui
```

The IDE starts with an empty scratch page. Starting takes a few seconds: the first time
`tuprolog` is imported, the Java virtual machine starts in the background. Quit with `ctrl+q`.

Any modern terminal works (e.g. Windows Terminal, iTerm2, GNOME Terminal, the terminal of VS
Code); the older macOS Terminal shows fewer colors. The mouse works too: click tabs and buttons,
and scroll the panels.

## Start it with Docker

Each release of 2PPy also comes as a Docker image, for amd64 and arm64 machines, on GitHub
Packages: `ghcr.io/tuprolog/2ppy`, tagged with the version of 2PPy (`:<version>`) and `:latest`.
It holds Python and 2PPy only, and starts the terminal IDE:

```bash
docker run -it --rm ghcr.io/tuprolog/2ppy
```

`-it` gives the IDE a terminal (without it, it cannot start), and `--rm` deletes the container on
exit. Arguments after the image name are those of `2ppy-tui` (see the next section), and so are
environment variables.

The IDE runs in the `/work` directory of the container: to open and save files of your machine,
mount a directory there. For example, to edit `family.pl` from the current directory:

```bash
docker run -it --rm -v "$PWD:/work" ghcr.io/tuprolog/2ppy family.pl
```

The IDE runs as a user with id 1000. On Linux, if your user has another id, run the container
with yours, so that it can save files in the mounted directory:

```bash
docker run -it --rm -v "$PWD:/work" --user "$(id -u):$(id -g)" ghcr.io/tuprolog/2ppy family.pl
```

The image can also run Python, with 2PPy installed:

```bash
docker run -it --rm --entrypoint python ghcr.io/tuprolog/2ppy
```

## Configure it from the command line

`2ppy-tui --help` lists every option. Files given as arguments open a page each (their text is the
static knowledge base of the page's solver; missing files are created on save); the other options
set the initial pages, and how every solver is built:

| Option | Effect |
|--------|--------|
| `FILE ...` | open each file in a page |
| `-t`, `--theory TEXT` | open a scratch page with this theory |
| `-q`, `--query QUERY` | the query of the initial pages |
| `-s`, `--solve [one\|ten\|hundred\|all]` | solve the query at startup, asking for 1 (default), 10, 100 or all solutions |
| `--stdin TEXT`, `--stdin-file FILE` | the standard input of the initial pages |
| `--dialect prolog\|problog` | the logic language: ProbLog solutions show their probability |
| `-d`, `--dynamic-kb FILE` | clauses for the dynamic knowledge base of every solver (also after a reset; repeatable) |
| `-l`, `--library SPEC` | load a library: `io`, `oop` (Python objects), `oop-jvm` (JVM objects), or `MODULE:NAME` / `FILE.py:NAME` naming a library, or a function returning one (repeatable) |
| `--no-default-libraries` | load only the `--library` ones (by default, `io` and `oop`) |
| `--oop-allow-all-imports`, `--oop-allow-private` | let the `oop` library import any module, or reach private attributes |
| `--no-builtins` | solvers without the standard library |
| `--unificator SPEC` | `MODULE:NAME` / `FILE.py:NAME` of a unificator, or of a function returning one |
| `-f`, `--flag NAME=VALUE` | set a flag of every solver, e.g. `unknown=fail` (repeatable) |
| `--timeout SECONDS` | the default timeout of resolutions (default: 5) |
| `--scheduling concurrent\|single` | whether resolutions of different pages run concurrently, or starting one stops the others |

For example:

```bash
2ppy-tui family.pl -q "ancestor(abe, X)" --solve ten
2ppy-tui --dialect problog -t "0.3::rain. wet :- rain." -q wet --solve
2ppy-tui --dynamic-kb facts.pl --library mylibs:geometry --flag unknown=fail
```

### With environment variables

Each option can also be set by an environment variable: `TWOPPY_` followed by its long name in
upper case, with `_` for `-` (e.g. `TWOPPY_QUERY` for `--query`, `TWOPPY_DYNAMIC_KB` for
`--dynamic-kb`). Its value is:

- that of the option, for options with one (e.g. `TWOPPY_SOLVE=ten`);
- `true` (or `1`, `yes`, `on`), for options without one (e.g. `TWOPPY_NO_BUILTINS=true`);
- space-separated values, quoted as in a shell, for repeatable ones (e.g.
  `TWOPPY_FLAG="unknown=fail occurs_check=true"`).

`TWOPPY_FILES` lists the files to open, and empty variables are ignored. Command-line arguments
come after the variables: they override single values (e.g. a query), and add to repeated ones
(e.g. flags, files). This is handy with Docker, e.g. to start with a theory, and solve a query:

```bash
docker run -it --rm -e TWOPPY_THEORY="p(1). p(2)." -e TWOPPY_QUERY="p(X)" -e TWOPPY_SOLVE=all \
    ghcr.io/tuprolog/2ppy
```

## Edit and query

The IDE shows *pages*, as tabs. Each page has:

- a theory, at the top: the clauses queries are solved against;
- a query (after `?-`), with the buttons solving it (`Solve`, `Solve 10`, `Solve 100`,
  `Solve all`), stopping a resolution (`Stop`), and resetting the solver (`Reset`, discarding the
  clauses queries added), and the timeout of the page's resolutions (e.g. `500ms`, `2s 500ms`,
  `1m 30s`, or `none`; Enter, or leaving the field, applies it);
- panels, as tabs at the bottom (a `●` marks those with news):

| Panel | Shows |
|-------|-------|
| Solutions | the concluded resolutions, then the current one (`Clear solutions` forgets the former) |
| Stdin | the standard input queries read from (editable) |
| Stdout, Stderr | the standard output and error queries write to |
| Warnings | the solver's warnings (e.g. calls to unknown predicates) |
| Diagnostics | the problems found in the theory (e.g. syntax errors): Enter on one moves the editor's cursor there |
| Operators | the operators the solver knows: priority, specifier, name (`Add operator` declares one at the end of the theory, as `:- op(700, xfx, ===).`) |
| Flags | the solver's flags: Enter on one changes its value (from the next resolution on) |
| Libraries | the solver's libraries, with their predicates, operators and functions (Enter on one shows its documentation) |
| Static KB, Dynamic KB | the solver's static and dynamic knowledge bases (e.g. the clauses `assertz` added) |

Below the flags and the libraries, a line previews the documentation of the highlighted one;
`F1` (or the `Documentation` button) shows it in full.

The theory, the query and the knowledge bases are colored by syntax (variables, functors,
numbers, strings, comments, ...), as the operators the solver knows read them.

Solving asks for 1, 10, 100 or all solutions: if more may follow, the buttons become `Next`,
`Next 10`, `Next 100` and `Next all`. Pressing Enter in the query solves it, as `Solve` (or
`Next`) does.

## Work with files

*Scratch* pages have their own text, lost on exit: the IDE starts with one. Other pages edit files:
create one with `ctrl+n`, open one with `ctrl+o`, save it with `ctrl+s` (or elsewhere, with
`ctrl+e`), and reload it from disk with `ctrl+r`. Paths are relative to the directory the IDE was
started in (`/work`, with Docker). A `*` after a page's title marks unsaved changes: closing the
page (`ctrl+w`), reloading it, or quitting (`ctrl+q`) asks what to do with them.

## Keys

| Key | Command |
|-----|---------|
| `F5`, `F6`, `F7` | solve (or ask for the next) 1, 10, 100 solutions |
| `F8` | stop the resolution |
| `F9` | reset the solver |
| `F1` | the documentation of the highlighted flag, library, or library symbol |
| `ctrl+t` | new scratch page |
| `ctrl+n` | new file |
| `ctrl+o` | open a file |
| `ctrl+s`, `ctrl+e` | save, save as |
| `ctrl+r` | reload the file |
| `ctrl+w` | close the page |
| `ctrl+q` | quit |
| arrow keys | move among controls (buttons, tabs, ...), unless the focused one uses them (editors, the query, tables) |
| `tab`, `shift+tab` | move among controls |
| `ctrl+p` | the command palette (e.g. to change the color theme) |
