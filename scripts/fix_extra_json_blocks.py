#!/usr/bin/env python3
"""
Fix JSON code fences that contain 'extra data' by extracting the first balanced
JSON object and replacing the fence content with it. Operates conservatively:
- Only touches fences explicitly labeled ```json
- Attempts to parse the first balanced {...} object
- Writes changes in-place (no .bak backups)
- Reports files changed
"""

import re
import json
from pathlib import Path
import argparse

ROOT = Path(__file__).parent.parent
DOCS = ROOT / 'docs'
FENCE_RE = re.compile(r'```json\s*\n(.*?)\n```', re.DOTALL)


def extract_first_object(s: str):
    # find first '{' and parse until balanced
    start = s.find('{')
    if start == -1:
        return None
    stack = 0
    for i in range(start, len(s)):
        ch = s[i]
        if ch == '{':
            stack += 1
        elif ch == '}':
            stack -= 1
            if stack == 0:
                candidate = s[start:i+1]
                try:
                    parsed = json.loads(candidate)
                    return json.dumps(parsed, ensure_ascii=False, indent=2)
                except json.JSONDecodeError:
                    return None
    return None


def process_file(path: Path):
    content = path.read_text(encoding='utf-8')
    changed = False
    new_parts = []
    last = 0
    for m in FENCE_RE.finditer(content):
        new_parts.append(content[last:m.start()])
        body = m.group(1)
        # if body contains multiple json objects or trailing non-json, try to extract
        try:
            json.loads(body)
            # valid as-is
            new_parts.append(content[m.start():m.end()])
        except json.JSONDecodeError as e:
            first = extract_first_object(body)
            if first is None:
                # can't salvage, keep original
                new_parts.append(content[m.start():m.end()])
            else:
                # replace fence with first object
                new_block = '```json\n' + first + '\n```'
                new_parts.append(new_block)
                changed = True
        last = m.end()
    new_parts.append(content[last:])
    if changed:
        # Write changes in-place (no .bak backups)
        path.write_text(''.join(new_parts), encoding='utf-8')
        return str(path.relative_to(DOCS)), None
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='Files (relative to docs/) to process; if empty, process all')
    args = parser.parse_args()

    if args.files:
        targets = [DOCS / f for f in args.files]
    else:
        targets = list(DOCS.rglob('*.md'))

    changed = []
    for t in targets:
        if not t.exists():
            print('Missing:', t)
            continue
        res = process_file(t)
        if res:
            changed.append(res)

    if not changed:
        print('No files changed')
    else:
        print('Changed files:')
        for f,b in changed:
            if b:
                print(' -', f, 'backup:', b)
            else:
                print(' -', f)
