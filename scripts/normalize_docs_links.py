#!/usr/bin/env python3
"""
Normalize markdown links that start with `docs/` by replacing them with a correct
relative path from the source file to the target file under `docs/`.

Behavior:
- Scans all `.md` files under `docs/` (recursively).
- Skips content inside fenced code blocks.
- For each link target `(docs/...)`, if the target file exists under `docs/`,
  replace the link with the computed relative path from the source file.
- Creates a `.bak` backup for any file that is modified.

Run from repo root: `python3 scripts/normalize_docs_links.py`
"""
import re
from pathlib import Path
import os


LINK_PATTERN = re.compile(r"\]\(docs/([^\)#]+)(#[^\)]*)?\)")


def normalize_file(path: Path, docs_root: Path) -> bool:
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

        def repl(m):
            target = m.group(1)
            anchor = m.group(2) or ""
            target_abs = docs_root / target
            if not target_abs.exists():
                # don't change if target doesn't exist
                return m.group(0)
            rel = os.path.relpath(str(target_abs), start=str(path.parent))
            return f']({rel}{anchor})'

        new_line = LINK_PATTERN.sub(repl, line)
        if new_line != line:
            changed = True
        out_lines.append(new_line)

    if changed:
        bak = path.with_suffix(path.suffix + ".bak")
        path.rename(bak)
        path.write_text(''.join(out_lines), encoding="utf-8")
        print(f"Normalized links: {path} -> backup {bak}")
    return changed


def main():
    docs_root = Path('docs')
    if not docs_root.exists():
        print('No docs/ found. Exiting.')
        return

    md_files = list(docs_root.rglob('*.md'))
    print(f"Scanning {len(md_files)} markdown files under {docs_root}/")
    total_fixed = 0
    for p in md_files:
        try:
            if normalize_file(p, docs_root):
                total_fixed += 1
        except Exception as e:
            print(f"Error processing {p}: {e}")

    print(f"Done. Files modified: {total_fixed}")


if __name__ == '__main__':
    main()
