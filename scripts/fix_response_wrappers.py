#!/usr/bin/env python3
"""
Conservative auto-fixer: wrap response JSON examples that lack standard keys
into a top-level `data` object. Works in two modes:
 - dry-run (default): show proposed file changes
 - --apply: write changes and create a `.bak` backup

Only touches fenced blocks explicitly labelled ```json``` and only when
(a) the nearby context suggests a `response` example and
(b) the block parses as a JSON object and does NOT contain one of the
    standard response keys: status, data, error, result, message

Safe-by-default: creates backups and prints a summary.
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / 'docs'
REQUIRED_KEYS = {"status", "data", "error", "result", "message"}

pattern = re.compile(r'```json\s*\n((?:[^`]|`(?!``))*?)\n```', re.DOTALL)


def detect_type(context: str) -> str:
    ctx = context.lower()
    if 'request' in ctx:
        return 'request'
    if 'response' in ctx:
        return 'response'
    if 'schema' in ctx:
        return 'schema'
    return 'example'


def process_file(p: Path, apply: bool=False, max_changes: int=0):
    content = p.read_text(encoding='utf-8')
    matches = list(pattern.finditer(content))
    if not matches:
        return None

    new_content_parts = []
    last_pos = 0
    changes = []

    for m in matches:
        start, end = m.span()
        json_text = m.group(1).strip()
        # context: 200 chars before the fence
        ctx_start = max(0, start - 200)
        context = content[ctx_start:start]
        type_label = detect_type(context)

        replacement = None
        if type_label == 'response' and json_text:
            try:
                parsed = json.loads(json_text)
            except Exception:
                parsed = None

            if isinstance(parsed, dict):
                if not any(k in parsed for k in REQUIRED_KEYS):
                    # propose wrapping
                    wrapped = {"data": parsed}
                    formatted = json.dumps(wrapped, ensure_ascii=False, indent=2)
                    replacement = formatted

        # append unchanged content from last_pos to start
        new_content_parts.append(content[last_pos:start])
        if replacement is None:
            # keep original fence
            new_content_parts.append(content[start:end])
        else:
            # build new fenced block
            new_block = '```json\n' + replacement + '\n```'
            new_content_parts.append(new_block)
            changes.append({'file': str(p.relative_to(DOCS_DIR)), 'start': m.start(), 'end': m.end(), 'old_snippet': m.group(1)[:200], 'new_snippet': replacement[:200]})
            if max_changes and len(changes) >= max_changes:
                # append the rest unchanged and break
                new_content_parts.append(content[end:])
                last_pos = len(content)
                break

        last_pos = end

    if last_pos < len(content):
        new_content_parts.append(content[last_pos:])

    if not changes:
        return None

    new_content = ''.join(new_content_parts)

    if apply:
        bak = p.with_suffix(p.suffix + '.bak')
        p.rename(bak)
        p.write_text(new_content, encoding='utf-8')
        return {'file': str(p.relative_to(DOCS_DIR)), 'changes': changes, 'bak': str(bak.relative_to(DOCS_DIR))}
    else:
        return {'file': str(p.relative_to(DOCS_DIR)), 'changes': changes}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Apply changes (create .bak backups)')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Show proposed changes (default)')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of files to change (0 = unlimited)')
    args = parser.parse_args()

    files = sorted(DOCS_DIR.rglob('SP*.md'))
    proposed = []
    for p in files:
        res = process_file(p, apply=False, max_changes=0)
        if res:
            proposed.append(res)
            if args.limit and len(proposed) >= args.limit:
                break

    if not proposed:
        print('No proposed changes found.')
        raise SystemExit(0)

    print(f'Proposed changes in {len(proposed)} file(s):')
    for item in proposed:
        print(' -', item['file'], f"(changes: {len(item['changes'])})")

    if args.apply:
        applied = []
        for p in files:
            res = process_file(p, apply=True, max_changes=0)
            if res:
                applied.append(res)
        print('\nApplied changes to', len(applied), 'file(s)')
        for a in applied:
            print(' -', a['file'], 'backup:', a['bak'], f"(changes: {len(a['changes'])})")
    else:
        print('\nRun with --apply to write changes (backups created with .bak suffix)')
