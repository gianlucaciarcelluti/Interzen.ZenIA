#!/usr/bin/env python3
"""
Safely auto-fix common mermaid and heading issues in `docs/` markdown files.

Actions performed:
- Remove mermaid fenced blocks that are empty or have no meaningful nodes/states.
- Convert code-like headings into fenced code blocks (HTTP methods, JSON, inline code).
- Deduplicate repeated auto-generated headings like '[auto-generated heading level 2]'

Backups:
- Writes changes in-place (no `.bak` copies are created).

Run from repo root: `python3 scripts/auto_fix_mermaid_headings.py`
"""
import re
from pathlib import Path
import shutil


MERMAID_FENCE_RE = re.compile(r"^```(?:mermaid)?\s*$", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,6})\s*(.*)$")
AUTO_GEN_HEADING_RE = re.compile(r"^\[auto-generated heading level \d+\]$")
HTTP_VERBS = ("GET","POST","PUT","DELETE","PATCH","OPTIONS","HEAD")


def is_mermaid_empty_or_invalid(block_lines):
    # Heuristics: empty or only whitespace/comments OR no arrows/nodes/states
    content = "\n".join(block_lines).strip()
    if not content:
        return True
    # remove comment lines starting with %% or //
    non_comment = [ln for ln in block_lines if not ln.strip().startswith(('%%','//')) and ln.strip()]
    if not non_comment:
        return True
    # if stateDiagram present but no '-->' or ':' or 'state' tokens, consider invalid
    lower = content.lower()
    if 'statediagram' in lower or 'stateDiagram' in content:
        if '-->' not in content and '->' not in content and 'state' not in content:
            return True
    # if flowchart/graph but no node arrows
    if any(k in lower for k in ('flowchart','graph','graph td','graph lr')):
        if '-->' not in content and '->' not in content and '--' not in content:
            return True
    return False


def process_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)

    changed = False
    out = []
    i = 0
    seen_auto_generated = set()

    while i < len(lines):
        line = lines[i]

        # detect fence start
        if MERMAID_FENCE_RE.match(line):
            # capture fence block
            fence_start = i
            fence_lang = line.strip()
            i += 1
            block = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                block.append(lines[i].rstrip('\n'))
                i += 1
            # now lines[i] is closing fence or EOF
            fence_end = i
            closing = lines[i] if i < len(lines) else ''

            # decide whether to keep or drop
            if is_mermaid_empty_or_invalid(block):
                # drop the entire fence (skip closing fence too)
                changed = True
                # skip closing fence
                i += 1
                # do not append anything to out (effectively removed)
                continue
            else:
                # keep original block
                out.append(line)
                for ln in block:
                    out.append(ln + '\n')
                if i < len(lines):
                    out.append(lines[i])
                i += 1
                continue

        # headings handling
        m = HEADING_RE.match(line)
        if m:
            hashes, content = m.group(1), m.group(2).strip()
            # dedupe auto-generated headings (keep first occurrence per file)
            if AUTO_GEN_HEADING_RE.match(content):
                if content in seen_auto_generated:
                    changed = True
                    # skip this line (remove duplicate)
                    i += 1
                    continue
                else:
                    seen_auto_generated.add(content)
                    out.append(line)
                    i += 1
                    continue

            # code-like heading: starts with HTTP verb or contains JSON-like patterns
            first_word = content.split(' ',1)[0].strip().upper()
            if first_word in HTTP_VERBS or ('{' in content and '}' in content) or (':' in content and '"' in content):
                # convert to fenced code block
                changed = True
                out.append('```\n')
                out.append(content + '\n')
                out.append('```\n')
                i += 1
                continue

        # default: copy
        out.append(line)
        i += 1

    if changed:
        # Write changes in-place (no .bak backups)
        path.write_text(''.join(out), encoding='utf-8')
        print(f"Modified {path}")

    return changed


def main():
    root = Path('docs')
    if not root.exists():
        print('No docs/ directory found. Exiting.')
        return

    md_files = list(root.rglob('*.md'))
    print(f"Scanning {len(md_files)} markdown files under {root}/")
    total = 0
    for p in md_files:
        try:
            if process_file(p):
                total += 1
        except Exception as e:
            print(f"Error processing {p}: {e}")

    print(f"Done. Files modified: {total}")


if __name__ == '__main__':
    main()
