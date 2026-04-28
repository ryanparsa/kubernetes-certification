#!/usr/bin/env python3
"""
check_ascii.py -- scan repo for non-ASCII characters.

Usage:
    python3 check_ascii.py           # scan entire repo root
    python3 check_ascii.py [path]    # scan a specific file or directory

Exit code 1 if any violations are found (useful in pre-commit hooks).
"""

import os
import sys
import unicodedata

# Unicode codepoints that are intentional and exempt from the check.
# Box-drawing characters are used in directory tree diagrams in ref/ docs.
ALLOW_LIST: set[int] = {
    0x2500,  # BOX DRAWINGS LIGHT HORIZONTAL
    0x2502,  # BOX DRAWINGS LIGHT VERTICAL
    0x250C,  # BOX DRAWINGS LIGHT DOWN AND RIGHT
    0x2510,  # BOX DRAWINGS LIGHT DOWN AND LEFT
    0x2514,  # BOX DRAWINGS LIGHT UP AND RIGHT
    0x2518,  # BOX DRAWINGS LIGHT UP AND LEFT
    0x251C,  # BOX DRAWINGS LIGHT VERTICAL AND RIGHT
    0x2524,  # BOX DRAWINGS LIGHT VERTICAL AND LEFT
    0x252C,  # BOX DRAWINGS LIGHT DOWN AND HORIZONTAL
    0x2534,  # BOX DRAWINGS LIGHT UP AND HORIZONTAL
    0x253C,  # BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL
}

SCAN_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".sh"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def scan_file(path: str) -> list[tuple[int, int, str, str]]:
    """Return list of (line_no, col_no, char, char_name) for non-ASCII chars."""
    violations: list[tuple[int, int, str, str]] = []
    
    if "ascii-only.md" in path:
        return violations
        
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return violations

    for lineno, line in enumerate(lines, start=1):
        for i, ch in enumerate(line, start=1):
            if ord(ch) > 127 and ord(ch) not in ALLOW_LIST:
                name = unicodedata.name(ch, f"U+{ord(ch):04X}")
                violations.append((lineno, i, ch, name))

    return violations


def scan_dir(root: str) -> dict[str, list]:
    results: dict[str, list] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if any(fname.endswith(ext) for ext in SCAN_EXTENSIONS):
                full = os.path.join(dirpath, fname)
                violations = scan_file(full)
                if violations:
                    results[full] = violations
    return results


def main() -> int:
    args = sys.argv[1:]
    root = args[0] if args else os.path.dirname(os.path.abspath(__file__))

    if os.path.isfile(root):
        violations = scan_file(root)
        results = {root: violations} if violations else {}
    else:
        results = scan_dir(root)

    if not results:
        print("All clean -- no non-ASCII characters found.")
        return 0

    total = 0
    for filepath, violations in sorted(results.items()):
        rel = os.path.relpath(filepath)
        for lineno, col, ch, name in violations:
            print(f"{rel}:{lineno}:{col}: U+{ord(ch):04X} {name}  ({ch!r})")
            total += 1

    print(f"\nFound {total} violation(s) in {len(results)} file(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
