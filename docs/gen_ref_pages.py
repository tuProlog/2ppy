"""Generates a page of the API reference for each public module of the tuprolog package.

Run by the mkdocs-gen-files plugin (see mkdocs.yml): modules are found on the file system, without
importing them (importing tuprolog starts the JVM).
"""

from pathlib import Path

import mkdocs_gen_files

ROOT = Path(__file__).parent.parent
PACKAGE = ROOT / "tuprolog"
# modules whose import has side effects beyond defining names (they run interactive loops)
ENTRY_POINTS = {("tuprolog", "__main__")}

nav = mkdocs_gen_files.Nav()

for path in sorted(PACKAGE.rglob("*.py")):
    parts = path.relative_to(ROOT).with_suffix("").parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    if parts in ENTRY_POINTS or any(part.startswith("_") for part in parts):
        continue
    if "libs" in parts and path.parent == PACKAGE / "libs":  # JVM bootstrap, not API
        continue
    page = Path("reference", *parts).with_suffix(".md")
    with mkdocs_gen_files.open(page, "w") as file:
        file.write(f"::: {'.'.join(parts)}\n")
    mkdocs_gen_files.set_edit_path(page, path.relative_to(ROOT))
    nav[parts] = page.relative_to("reference").as_posix()

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as file:
    file.writelines(nav.build_literate_nav())
