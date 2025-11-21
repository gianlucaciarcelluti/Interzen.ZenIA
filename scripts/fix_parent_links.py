#!/usr/bin/env python3
"""
Fix markdown links in files directly under `docs/` that incorrectly start with `../`.

Behavior:
- Scans `.md` files whose parent is `docs/` (not nested subfolders).
- Skips content inside fenced code blocks.
- Replaces link targets of the form `(../some.md)` with `(some.md)`, preserving anchors.
- Creates a `.bak` backup for any file that is modified.

Run from repo root: `python3 scripts/fix_parent_links.py`
"""
import re
from pathlib import Path


PARENT_PATTERN = re.compile(r"\]\(\.\./([^\)#]+)(#[^\)]*)?\)")


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    in_fence = False
    changed = False
    out_lines = []

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue

        if in_fence:
            out_lines.append(line)
            continue

        new_line = PARENT_PATTERN.sub(r'](\1\2)', line)
        if new_line != line:
            changed = True
        out_lines.append(new_line)

    if changed:
        bak = path.with_suffix(path.suffix + ".bak")
        path.rename(bak)
        path.write_text(''.join(out_lines), encoding="utf-8")
        print(f"Fixed parent-link: {path} -> backup saved as {bak}")
    return changed


def main():
    root = Path("docs")
    if not root.exists():
        print("No docs/ directory found. Exiting.")
        return

    md_files = [p for p in root.glob("*.md")]
    print(f"Scanning {len(md_files)} top-level markdown files under {root}/")
    total_fixed = 0
    for p in md_files:
        try:
            if fix_file(p):
                total_fixed += 1
        except Exception as e:
            print(f"Error processing {p}: {e}")

    print(f"Done. Files modified: {total_fixed}")


if __name__ == '__main__':
    main()
