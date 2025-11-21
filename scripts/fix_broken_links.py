#!/usr/bin/env python3
"""
Conservative fixer for broken internal links reported in
`scripts/reports/links_validation.json`.

Usage:
  python3 scripts/fix_broken_links.py --report scripts/reports/links_validation.json [--apply]

Dry-run by default: prints proposed changes. Use `--apply` to modify files (writes files in-place).
"""
import argparse
import json
import os
import re
import unicodedata
from pathlib import Path


def ascii_normalize(s: str) -> str:
    """Normalize accented characters to ASCII equivalents."""
    nkfd = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in nkfd if not unicodedata.combining(ch))


def find_best_microservice_match(name: str, ms_root: Path) -> str:
    # name like 'MS15-REGISTRY' -> try to find a folder ending with 'REGISTRY'
    suffix = name.split("-", 1)[-1] if "-" in name else name
    for p in ms_root.iterdir():
        if p.is_dir() and p.name.upper().endswith(suffix.upper()):
            return p.name
    return name


def apply_corrections_for_target(target: str, src_path: Path, repo_root: Path) -> str:
    # Conservative transformations observed in report
    orig = target
    t = target.strip()

    # If link points to a docs/ path but the source is under docs/, strip leading docs/
    if t.startswith("docs/") and "docs" in src_path.parts:
        t = t[len("docs/"):]

    # If link starts with '../' and source is under docs/, remove leading '../'
    if t.startswith("../") and "docs" in src_path.parts:
        t = t[3:]

    # Normalize accents in filename components
    parts = t.split("/")
    parts = [ascii_normalize(p) for p in parts]
    t = "/".join(parts)

    # Fix double 'docs/docs' that sometimes appears
    t = t.replace("docs/docs/", "docs/")

    # Fix microservice placeholder names (e.g. MS15-REGISTRY -> MS16-REGISTRY)
    if "/microservices/" in t:
        ms_root = repo_root / "docs" / "microservices"
        try:
            segs = t.split("/")
            # find segment that looks like MSxx-...
            for i, seg in enumerate(segs):
                if seg.upper().startswith("MS") and '-' in seg:
                    corrected = find_best_microservice_match(seg, ms_root)
                    segs[i] = corrected
                    break
            t = "/".join(segs)
        except Exception:
            pass

    # If link points to repo-level folders like 'scripts/' or '.github/workflows/'
    # from inside docs/, change to '../scripts/' etc.
    repo_level_candidates = ["scripts/", ".github/workflows/"]
    if any(t.startswith(c) for c in repo_level_candidates) and "docs" in src_path.parts:
        t = "../" + t

    # Map likely Italian-English filename pairs (conservative)
    italian_to_english = {
        "ARCHITETTURA-PANORAMICA.md": "ARCHITECTURE-OVERVIEW.md",
    }
    if t in italian_to_english:
        t = italian_to_english[t]

    # Map some known missing filenames to existing equivalents
    known_mappings = {
        'MS15-REGISTRY': 'MS16-REGISTRY',
        'GUIDA-SVILUPPO.md': 'DEVELOPMENT-GUIDE.md',
    }
    for k, v in known_mappings.items():
        if k in t:
            t = t.replace(k, v)

    # If the corrected target corresponds to an existing file under docs/,
    # rewrite as a relative path from the source file directory (conservative).
    try:
        # Compute absolute candidate inside docs
        candidate_abs = repo_root / 'docs' / t
        if candidate_abs.exists():
            # Source absolute path
            src_abs = repo_root / src_path
            if not src_abs.exists():
                src_abs = repo_root / 'docs' / src_path
            src_dir = src_abs.parent
            rel = os.path.relpath(candidate_abs, start=src_dir)
            # Use POSIX style for markdown links
            t = rel.replace(os.path.sep, '/')
    except Exception:
        pass

    # If target ends with '/' and README.md exists, point to README.md
    if t.endswith('/'):
        candidate = repo_root / "docs" / t
        if (candidate / "README.md").exists():
            t = t.rstrip('/') + '/README.md'
        else:
            # try without leading docs/
            candidate2 = repo_root / t
            if (candidate2 / "README.md").exists():
                t = t.rstrip('/') + '/README.md'

    return t if t != orig else orig


def replace_in_line(line: str, old: str, new: str) -> (str, bool):
    # Replace first exact occurrence of old in line; return (new_line, changed)
    idx = line.find(old)
    if idx == -1:
        return line, False
    return line[:idx] + new + line[idx + len(old):], True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", default="scripts/reports/links_validation.json")
    p.add_argument("--apply", action="store_true", help="Apply changes (writes files in-place)")
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    with open(args.report, 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    errors = data.get('errors', [])
    if not errors:
        print("No broken-link errors found in report.")
        return

    # Parse errors lines like: "docs/FILE.md:123 - Link rotto: TARGET (risolverebbe: /abs/path)"
    changes = {}
    to_skip = []
    for e in errors:
        m = re.match(r"(?P<src>[^:]+):(?P<line>\d+) - Link rotto: (?P<target>[^ ]+)", e)
        if not m:
            # fallback: try to extract before ' - '
            parts = e.split(' - ')
            src = parts[0].split(':')[0]
            # try to grab a token after 'Link rotto:'
            targ = None
            if 'Link rotto:' in e:
                targ = e.split('Link rotto:')[1].split('(')[0].strip()
            if not targ:
                continue
            m = {'src': src, 'line': '0', 'target': targ}
            src_path = Path(m['src'])
        else:
            src_path = Path(m.group('src'))

        target = m['target'] if isinstance(m, dict) else m.group('target')
        # Compute correction
        corrected = apply_corrections_for_target(target, src_path, repo_root)
        if corrected == target:
            to_skip.append((src_path, target))
            continue

        changes.setdefault(src_path, []).append((target, corrected))

    if not changes:
        print("No safe automatic corrections identified. Candidates to review:")
        for s, t in to_skip:
            print(f"- {s}: {t}")
        return

    print("Proposed automatic corrections (dry-run):")
    for src, edits in changes.items():
        print(f"\nFile: {src}")
        for old, new in edits:
            print(f"  {old}  =>  {new}")

    if not args.apply:
        print("\nRun with --apply to write changes (files will be overwritten in-place).")
        return

    # Apply edits
    for src, edits in changes.items():
        src_path = repo_root / src
        if not src_path.exists():
            print(f"Skipping missing source file: {src_path}")
            continue
        with open(src_path, 'r', encoding='utf-8') as fh:
            lines = fh.readlines()

        # Write edited content in-place (no .bak backups)
        content_lines = lines

        made_changes = False
        # Apply edits line-by-line conservatively: only first occurrence per edit
        for i, line in enumerate(content_lines):
            for old, new in edits:
                new_line, changed = replace_in_line(line, old, new)
                if changed:
                    content_lines[i] = new_line
                    made_changes = True
                    # once replaced this old in this file, avoid replacing same old again
                    edits = [(o, n) for (o, n) in edits if o != old]
                    break

        if made_changes:
            with open(src_path, 'w', encoding='utf-8') as fh:
                fh.writelines(content_lines)
            print(f"Applied changes to {src_path}")
        else:
            print(f"No changes applied to {src_path}")


if __name__ == '__main__':
    main()
