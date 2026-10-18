"""The example notebooks (examples/*.ipynb) run without errors."""

from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

EXAMPLES = sorted((Path(__file__).parent.parent / "examples").glob("*.ipynb"))


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda path: path.stem)
def test_example_notebook_runs(path):
    notebook = nbformat.read(path, as_version=4)
    # each notebook runs in its own kernel, i.e. its own process (and JVM)
    NotebookClient(notebook, timeout=600, kernel_name="python3").execute(cwd=str(path.parent))
