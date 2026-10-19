# Examples

Jupyter notebooks showing 2PPy at work. Each page is a notebook with its outputs, which you can
download (button at the top of the page) or find in the
[`examples/` folder](https://github.com/tuProlog/2ppy/tree/master/examples) of the repository.
The test suite runs them all.

| Notebook | Content | Related guides |
|----------|---------|----------------|
| [Terms and unification](01-terms-and-unification.ipynb) | building, parsing, inspecting and converting terms; unification and substitutions | [Build and parse terms](../how-to/build-and-parse-terms.md), [Terms and variables](../explanation/terms-and-variables.md) |
| [Knowledge bases and queries](02-knowledge-bases-and-queries.ipynb) | theories, solvers, queries, lazy solutions, dynamic knowledge bases, built-ins | [Your first logic program](../tutorials/your-first-logic-program.md), [Query solvers](../how-to/query-solvers.md) |
| [Predicates and functions in Python](03-predicates-and-functions-in-python.ipynb) | extending solvers with Python functions, and their errors | [Define predicates in Python](../how-to/define-predicates-in-python.md) |
| [Python objects from Prolog](04-python-objects-from-prolog.ipynb) | OOPLib: creating objects and calling methods from Prolog | [Use Python objects from Prolog](../how-to/use-python-objects-from-prolog.md) |
| [Input and output](05-input-and-output.ipynb) | Python streams as solvers' channels, reading theories from files, IOLib | [Read and write streams](../how-to/read-and-write-streams.md) |
| [Probabilistic logic programming](06-probabilistic-logic-programming.ipynb) | ProbLog programs and the probability of their solutions | [Run probabilistic programs](../how-to/run-probabilistic-programs.md) |
| [The N-queens puzzle](07-n-queens.ipynb) | a classic search problem, solved by backtracking | [Logic programming](../explanation/logic-programming.md) |

## Running the notebooks

Install 2PPy and Jupyter (`pip install 2ppy jupyter`), download a notebook, and open it with
`jupyter lab`. From a clone of the repository, Jupyter is a development dependency:

```bash
uv sync && uv run poe build-jars
uv run jupyter lab examples/
```
