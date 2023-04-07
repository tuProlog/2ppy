# 2PPy (tuProlog in Python)

Experimental porting of [2P-Kt](https://github.com/tuProlog/2p-kt) on Python, via [JPype](https://jpype.readthedocs.io).

> This is a __work in progress__. 2PPy is not ready for general availability, yet.

## Introduction

Object-oriented and modular ecosystem for symbolic AI and logic programming, currently featuring:

* a module for logic terms and clauses representation, namely `tuprolog.core`,

* a module for logic unification, namely `tuprolog.unify`,

* a module for in-memory indexing and storing logic theories, as well as other sorts of collections of logic clauses, namely `tuprolog.theory`,

* a module providing generic API for resolution of logic queries, namely `tuprolog.solve`, currently implementing a Prolog solver

* two parsing modules: one aimed at parsing terms, namely `tuprolog.core.parsing`, and the other aimed at parsing theories, namely `tuprolog.theory.parsing`,

* two serialisation-related modules: one aimed at (de)serialising terms and clauses, namely `tuprolog.core.serialize`, and the 
other aimed at  (de)serialising terms theories, namely `tuprolog.theory.serialize`,

* a module for using Prolog via a command-line interface, namely `tuprolog.repl`,

* a module that implement probabilistic logic programming and solving, namely `tuprolog.solve.problog`.

## How to use 2ppy

### Use 2ppy as a library

1. Install Python 3 (look into the `.pyproject.toml` to know the exact versions supported)
    * If your system has 64-bit processor, install the Python 3 64-bit distribution, and viceversa
    * Ensure PIP works fine
    * It's suggested to use a [virtual environment](https://docs.python.org/3/library/venv.html) to install the dependencies locally
    * It's suggested to use [Pyenv](https://github.com/pyenv/pyenv) to easily handle multiple Python versions on the same machine

1. If you have installed some prior development version of 2PPy (e.g. `tuppy` or `tuprolog`), uninstall them via
    ```bash
    pip uninstall tuppy tuprolog
    ```
    On __Mac OS__ this may not work as expected.
    Consider running the following command instead:
    ```bash
    python3 -m pip uninstall tuppy tuprolog
    ```
1. Install 2PPy from Pypi by running:
    ```bash
    pip install 2ppy
    ```
    On __Mac OS__ this may not work as expected.
    Consider running the following command instead:
    ```bash
    python3 -m pip install 2ppy
    ```
1. Import `tuprolog.*` modules in your Python scripts
1. *Note for the expert users:* 2ppy downloads its own [Java Virtual Machine](https://en.wikipedia.org/wiki/Java_virtual_machine) in order to call Java bytecode from python. If you install the package with sdist, it's downloaded during install. If you use the binary wheels packaging, it's download on first import of the `tuprolog` package.

### How to develop 2PPy

1. Restore Python dev dependencies via PIP, by running:
    ```bash
    pip install -r requirements.txt
    ```
    On __Mac OS__ this may not work as expected.
    Consider running the following command instead:
    ```bash
    python3 -m pip -r requirements.txt
    ```
1. Write the code inside `tuprolog` and the unit tests inside `test`
1. Execute tests with `python -m pytest -p no:faulthandler`
1. Build the package with `python -m build`
1. Install the package locally with `python setup.py install`
1. Print the package version, computed from git tags with `python -m setuptools_git_versioning`

### How to use 2PPy as an executable

1. Python shell mode: WIP
1. Logic solver [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop): WIP
