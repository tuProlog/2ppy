# Examples

Jupyter notebooks showing how 2PPy works, from terms to probabilistic logic programming.
They are also part of the [documentation](https://tuprolog.github.io/2ppy/examples/), and the test
suite runs them.

| Notebook | Content |
|----------|---------|
| [Terms and unification](01-terms-and-unification.ipynb) | building, parsing, inspecting and converting terms; unification and substitutions |
| [Knowledge bases and queries](02-knowledge-bases-and-queries.ipynb) | theories, solvers, queries, lazy solutions, dynamic knowledge bases, built-ins |
| [Predicates and functions in Python](03-predicates-and-functions-in-python.ipynb) | extending solvers with Python functions, and their errors |
| [Python objects from Prolog](04-python-objects-from-prolog.ipynb) | OOPLib: creating objects and calling methods from Prolog |
| [Input and output](05-input-and-output.ipynb) | Python streams as solvers' channels, reading theories from files, IOLib |
| [Probabilistic logic programming](06-probabilistic-logic-programming.ipynb) | ProbLog programs and the probability of their solutions |
| [The N-queens puzzle](07-n-queens.ipynb) | a classic search problem, solved by backtracking |

To run them, from a clone of the repository:

```bash
uv sync && uv run poe build-jars    # or: pip install 2ppy jupyter
uv run jupyter lab examples/
```
