"""Install or remove this repo's local Git hooks (never tracked: they live in .git/hooks).

python scripts/githooks.py install|uninstall [HOOK...]   # default: all hooks
python scripts/githooks.py check-msg|check-ai FILE       # used by commit-msg

Several hooks may share one Git hook file (e.g. commit-msg); each is a tagged line in it.
"""

from __future__ import annotations

import io
import re
import stat
import subprocess
import sys
from pathlib import Path

MARKER = "# project-githook"
# name -> (Git hook file, command)
HOOKS = {
    "pre-commit": ("pre-commit", "uv run poe static-checks"),
    "no-ai-signature": ("commit-msg", 'uv run python scripts/githooks.py check-ai "$1"'),
    "conventional-commits": ("commit-msg", 'uv run python scripts/githooks.py check-msg "$1"'),
    "pre-push": ("pre-push", "uv run poe static-checks && uv run poe test"),
}
TAG = re.compile(r"# githook:(\S+)$", re.MULTILINE)
TYPES = "build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test"
CONVENTIONAL = re.compile(rf"^({TYPES})(\([^()\s][^()]*\))?!?: \S")
# Messages git writes itself (merges, reverts, autosquash) are let through.
EXEMPT = re.compile(r"^(Merge |Revert \"|fixup! |squash! |amend! )")
# AI assistants' trailers and footers; a plain mention of a tool in the text is fine.
AI = r"claude|anthropic|codex|openai|chatgpt|gpt-?\d|copilot|gemini|cursor|aider|devin"
AI_SIGNATURE = re.compile(
    rf"^\s*(co-authored-by|signed-off-by|assisted-by|generated-by):.*\b({AI})\b"
    rf"|generated (with|by)\b.*\b({AI})\b"
    r"|noreply@(anthropic|openai)\.com",
    re.IGNORECASE,
)
SCISSORS = "# ------------------------ >8 ------------------------"


def hooks_dir() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--git-path", "hooks"], check=True, capture_output=True, text=True
    )
    return Path(out.stdout.strip())


def is_ours(path: Path) -> bool:
    return path.exists() and MARKER in path.read_text(encoding="utf-8", errors="replace")


def installed(path: Path) -> set[str]:
    return set(TAG.findall(path.read_text(encoding="utf-8"))) if is_ours(path) else set()


def write(path: Path, names: set[str]) -> None:
    if not names:
        path.unlink(missing_ok=True)
        return
    lines = [f"{cmd} || exit 1  # githook:{n}" for n, (_, cmd) in HOOKS.items() if n in names]
    path.write_text("\n".join(["#!/bin/sh", MARKER, *lines, ""]), encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install(names: list[str]) -> int:
    folder = hooks_dir()
    folder.mkdir(parents=True, exist_ok=True)
    failed = 0
    for name in names:
        path = folder / HOOKS[name][0]
        if path.exists() and not is_ours(path):
            print(f"{name}: skipped, {path} exists and was not installed by this script")
            failed = 1
            continue
        write(path, installed(path) | {name})
        print(f"{name}: installed")
    return failed


def uninstall(names: list[str]) -> int:
    folder = hooks_dir()
    for name in names:
        path = folder / HOOKS[name][0]
        if name in installed(path):
            write(path, installed(path) - {name})
            print(f"{name}: removed")
        else:
            print(f"{name}: not installed")
    return 0


def message(file: str) -> list[str]:
    text = Path(file).read_text(encoding="utf-8").split(SCISSORS)[0]  # drop `commit -v` diff
    return [s for s in text.splitlines() if not s.startswith("#")]


def check_ai(file: str) -> int:
    signed = [s for s in message(file) if AI_SIGNATURE.search(s)]
    if signed:
        print(
            "commit-msg: remove the AI assistant signature:", *signed, sep="\n  ", file=sys.stderr
        )
    return 1 if signed else 0


def check_msg(file: str) -> int:
    subject = next((s for s in message(file) if s.strip()), "")
    if CONVENTIONAL.match(subject) or EXEMPT.match(subject):
        return 0
    print(
        f"commit-msg: not a Conventional Commit: {subject!r}\n"
        f"expected '<type>[(scope)][!]: <description>', type one of {TYPES.replace('|', ', ')}",
        file=sys.stderr,
    )
    return 1


def main(argv: list[str]) -> int:
    if isinstance(sys.stderr, io.TextIOWrapper):  # e.g. cp1252 consoles can't print emoji
        sys.stderr.reconfigure(errors="backslashreplace")
    if len(argv) == 2 and argv[0] in ("check-msg", "check-ai"):
        return (check_msg if argv[0] == "check-msg" else check_ai)(argv[1])
    if not argv or argv[0] not in ("install", "uninstall"):
        print(__doc__, file=sys.stderr)
        return 2
    names = argv[1:] or list(HOOKS)
    unknown = sorted(set(names) - set(HOOKS))
    if unknown:
        print(f"unknown hooks: {', '.join(unknown)}; available: {', '.join(HOOKS)}")
        return 2
    return (install if argv[0] == "install" else uninstall)(names)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
