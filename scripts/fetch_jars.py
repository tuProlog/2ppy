"""Download 2P-Kt and its JVM dependencies (declared in pom.xml) into tuprolog/libs/.

python scripts/fetch_jars.py   # requires Apache Maven (mvn) on the PATH

The JARs are not tracked: they must be fetched before testing or building the package.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

DIR_ROOT = Path(__file__).parents[1]
DIR_JARS = DIR_ROOT / "tuprolog" / "libs"


def main() -> int:
    mvn = shutil.which("mvn")
    if mvn is None:
        print("Apache Maven (mvn) not found on the PATH", file=sys.stderr)
        return 1
    for jar in DIR_JARS.glob("*.jar"):  # drop stale versions
        jar.unlink()
    command = [
        mvn,
        "--batch-mode",
        "--quiet",
        "dependency:copy-dependencies",
        f"-DoutputDirectory={DIR_JARS}",
    ]
    return subprocess.run(command, cwd=DIR_ROOT, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
