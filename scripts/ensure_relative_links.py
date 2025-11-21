#!/usr/bin/env python3
"""Convert absolute/Internal repo links in Markdown files to relative links.

Usage:
  python3 scripts/ensure_relative_links.py --root . --apply --include "**/*.md"

By default this script runs in dry-run mode and prints proposed replacements.
Use `--apply` to write changes in-place.

It converts links of these forms into relative links when target exists inside
the repository:
- Links starting with `/` (repo-root absolute), e.g. `/docs/FILE.md`
- Links starting with `docs/` (repo-root relative)
- GitHub blob/raw links that point to this repo (owner/repo/blob/<branch>/path)
- Absolute filesystem links that fall under the repository root

It preserves external links (other domains), mailto:, anchors, and fragments.
"""

import argparse
import os
import re
from pathlib import Path
from urllib.parse import urlparse


LINK_RE = re.compile(r"(?P<prefix>!?)\[(?P<label>[^\]]*)\]\((?P<target>[^)]+)\)")


def is_external(url: str) -> bool:
    if url.startswith("mailto:") or url.startswith("tel:"):
        return True
    p = urlparse(url)
    return bool(p.scheme and p.scheme in ("http", "https") and p.netloc)


def try_resolve_repo_url(url: str, repo_root: Path, repo_owner: str = None, repo_name: str = None):
    """If the url is a github blob/raw link pointing inside this repo, return the local path.
    Otherwise return None.
    """
    # Examples:
    # https://github.com/<owner>/<repo>/blob/main/docs/FILE.md
    # https://raw.githubusercontent.com/<owner>/<repo>/main/docs/FILE.md
    p = urlparse(url)
    if p.netloc not in ("github.com", "raw.githubusercontent.com"):
        return None
    parts = p.path.strip("/").split("/")
    if p.netloc == "github.com":
        # /<owner>/<repo>/blob/<branch>/path
        if len(parts) >= 5 and parts[2] in ("blob", "raw"):
            path_parts = parts[4:]
            candidate = repo_root.joinpath(*path_parts)
            return candidate if candidate.exists() else None
    else:
        # raw.githubusercontent.com/<owner>/<repo>/<branch>/path
        if len(parts) >= 4:
            path_parts = parts[3:]
            candidate = repo_root.joinpath(*path_parts)
            return candidate if candidate.exists() else None
    return None


def convert_target(target: str, src_file: Path, repo_root: Path):
    # split fragment
    if "#" in target:
        base, frag = target.split("#", 1)
        frag = "#" + frag
    else:
        base, frag = target, ""

    # don't touch purely anchor links
    if base.strip() == "":
        return target

    # external schemes we don't change (unless they point to this repo)
    if base.startswith("http://") or base.startswith("https://"):
        maybe = try_resolve_repo_url(base, repo_root)
        if maybe is None:
            return target
        target_path = maybe
    elif base.startswith("/"):
        # repo-root absolute
        candidate = repo_root.joinpath(base.lstrip("/"))
        if not candidate.exists():
            return target
        target_path = candidate
    elif base.startswith("docs/"):
        candidate = repo_root.joinpath(base)
        if not candidate.exists():
            return target
        target_path = candidate
    elif os.path.isabs(base):
        candidate = Path(base)
        # only convert if inside repo
        try:
            candidate_rel = candidate.relative_to(repo_root)
        except Exception:
            return target
        if not candidate.exists():
            return target
        target_path = candidate
    else:
        # already relative or other scheme; leave unchanged
        return target

    # compute relative path from src_file.parent to target_path
    rel = os.path.relpath(str(target_path), start=str(src_file.parent))
    # normalize to posix separators for markdown
    rel_posix = Path(rel).as_posix()
    return rel_posix + frag


def process_file(path: Path, repo_root: Path, apply: bool) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0

    def repl(m):
        nonlocal changed
        prefix = m.group("prefix")
        label = m.group("label")
        target = m.group("target").strip()
        new_target = target

        # Skip if link is external but may point to repo
        # If it's a URL to repository files, convert; otherwise ignore.
        if target.startswith("http://") or target.startswith("https://"):
            maybe = try_resolve_repo_url(target, repo_root)
            if maybe:
                new_target = convert_target(target, path, repo_root)
            else:
                return m.group(0)
        else:
            new_target = convert_target(target, path, repo_root)

        if new_target != target:
            changed += 1
            return f"{prefix}[{label}]({new_target})"
        return m.group(0)

    new_text = LINK_RE.sub(repl, text)

    if changed > 0:
        print(f"{path}: {changed} link(s) converted")
        if apply:
            path.write_text(new_text, encoding="utf-8")
    return changed


def main():
    p = argparse.ArgumentParser(description="Convert absolute repo links in Markdown to relative links")
    p.add_argument("--root", default='.', help="Repository root path")
    p.add_argument("--apply", action="store_true", help="Write changes in-place")
    p.add_argument("--include", default='**/*.md', help="Glob pattern to include (relative to root)")
    args = p.parse_args()

    repo_root = Path(args.root).resolve()

    files = list(repo_root.glob(args.include))
    total_changes = 0
    for f in files:
        if f.is_file():
            total_changes += process_file(f, repo_root, args.apply)

    if total_changes == 0:
        print("No changes proposed.")
    else:
        if args.apply:
            print(f"Applied {total_changes} change(s) across markdown files.")
        else:
            print(f"Proposed {total_changes} change(s) across markdown files (dry-run).")


if __name__ == '__main__':
    main()
