# 2PPy (tuProlog in Python)

Experimental porting of [2P-Kt](https://github.com/tuProlog/2p-kt) on Python, via [JPype](https://jpype.readthedocs.io).

> This is a __work in progress__.

## Introduction

Object-oriented and modular ecosystem for symbolic AI and logic programming, currently featuring:

* [a command-line interface, in the form of a REPL](#use-2ppy-as-an-interactive-repl)

* a module for logic terms and clauses representation, namely `tuprolog.core`

* a module for logic unification, namely `tuprolog.unify`

* a module for in-memory indexing and storing logic theories, as well as other sorts of collections of logic clauses, namely `tuprolog.theory`

* a module providing generic API for resolution of logic queries, namely `tuprolog.solve`
    * a module that implements deterministic logic programming and solving, namely `tuprolog.solve.prolog`
    * a module that implements probabilistic logic programming and solving, namely `tuprolog.solve.problog`

* two parsing modules: one aimed at parsing terms, namely `tuprolog.core.parsing`, and the other aimed at parsing theories, namely `tuprolog.theory.parsing`

## How to use 2ppy

### Installing 2ppy

1. Install Python 3 (look into the [`pyproject.toml`](pyproject.toml) to know the exact versions supported)

    * If your system has 64-bit processor, install the Python 3 64-bit distribution, and viceversa
    * Ensure `pip` works fine
    * It's suggested to use a [virtual environment](https://docs.python.org/3/library/venv.html) to install the dependencies locally
    * It's suggested to use [Pyenv](https://github.com/pyenv/pyenv) to easily handle multiple Python versions on the same machine

1. If you have installed some prior development version of 2PPy (e.g. `tuppy` and/or `tuprolog`), uninstall them via
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
    pip install tuprolog
    ```
    On __Mac OS__ this may not work as expected.
    Consider running the following command instead:
    ```bash
    python3 -m pip install tuprolog
    ```
1. *Note #1 for the expert users:* 2ppy downloads its own [Java Virtual Machine](https://en.wikipedia.org/wiki/Java_virtual_machine) in order to call Java bytecode from python. If you install the package with sdist, it's downloaded during install. If you use the binary wheels packaging, it's downloaded on first import of the `tuprolog` package.
2. *Note #2 for the expert users:* The JVM version can be chosen by setting the `JAVA_VERSION` environment variable before downloading the JVM for the first time.

### Use 2ppy as a Python library

1. Import `tuprolog.*` modules in your Python scripts
1. Use the Pythonic API to write, parse or solve your logic programs. You can find some examples in the [api tests folder](test/api).

### Use 2PPy as an interactive REPL

1. Python shell mode: run `python -m tuprolog`
1. Logic solver [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop): 
    1. run `python -m tuprolog.repl.prolog` for Prolog
    1. run `python -m tuprolog.repl.problog` for ProbLog

## How to contribute to 2PPy

1. Install dependencies
    1. Restore Python dev dependencies via `pip`, by running:
        ```bash
        pip install -r requirements.txt
        ```
        On __Mac OS__ this may not work as expected.
        Consider running the following command instead:
        ```bash
        python3 -m pip install -r requirements.txt
        ```
    1. Install [maven](https://maven.apache.org/install.html) and make sure that the `mvn` command is available by adding Maven to your `PATH`. Maven is used to download java dependencies from the [Maven Central Repository for tuProlog](https://mvnrepository.com/artifact/it.unibo.tuprolog).
1. Write the code inside `tuprolog` and the unit tests inside `test`
1. Execute tests with `python -m pytest -p no:faulthandler`
1. Build the package with `python -m build`
1. Install the recently built package locally using wheels with `pip install dist/2ppy-$(python -m setuptools_git_versioning)-*.whl --force-reinstall`
1. Optionally, print the package version, computed from git tags with `python -m setuptools_git_versioning`

### Adopted Git flow

The Git Flow for 2ppy consists of the following:

- The ongoing development happens on the `develop` branch
- The `master` branch is used to display the latest released code
- Independent features are developed on their own branches, and merged into `develop` when ready
- In order to make a new release, the code should be merged on master and a new [git tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging#_annotated_tags) should be created on the release commit, following the [Semantic Versioning](https://semver.org/) semantic.  
  As an example, the following commands can be used to make a new release:
    ```bash
    git checkout master
    git merge develop
    git tag -a 0.1.0 -m "First release"
    git push origin master --follow-tags
    ```

#### CI/CD

The Continuous Integration pipeline will run unit tests against some combinations of operating systems, supported java versions for the JVM and supported python versions.
It will also check the Python style with [flake8](https://flake8.pycqa.org/en/latest/).

The Continuous Delivery pipeline will create a new [Github Release](https://github.com/tuProlog/2ppy/releases) and will deploy the package on [PyPI](https://pypi.org/project/2ppy/).
