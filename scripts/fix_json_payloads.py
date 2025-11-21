#!/usr/bin/env python3
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'

CODE_FENCE_RE = re.compile(r"```json\n(.*?)\n```", re.DOTALL | re.IGNORECASE)

def clean_json_text(text):
    # Remove JS-style comments // ...
    lines = text.splitlines()
    cleaned_lines = []
    for ln in lines:
        # remove // comments
        if '//' in ln:
            # if it's inside a string, skip naive removal - but simplest heuristic: remove only if // appears at line start or after optional spaces
            if re.match(r"\s*//", ln):
                continue
            else:
                # remove inline // comments
                ln = re.sub(r"//.*$", "", ln)
        cleaned_lines.append(ln)
    cleaned = '\n'.join(cleaned_lines)

    # Replace pipe-style enums like "success|warning|error" with a sensible default ("success")
    cleaned = re.sub(r'"([^"]*?)\|[^"]*?"', lambda m: '"' + m.group(1).split('|')[0] + '"', cleaned)

    # Remove trailing commas before } or ]
    cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)

    # Trim leading/trailing whitespace
    cleaned = cleaned.strip()

    # Try to balance braces: count { and }
    open_braces = cleaned.count('{')
    close_braces = cleaned.count('}')
    if open_braces > close_braces:
        cleaned += '\n' + ('}' * (open_braces - close_braces))

    open_brackets = cleaned.count('[')
    close_brackets = cleaned.count(']')
    if open_brackets > close_brackets:
        cleaned += '\n' + (']' * (open_brackets - close_brackets))

    return cleaned


def try_load(s):
    try:
        json.loads(s)
        return True, None
    except Exception as e:
        return False, str(e)


def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    changed = False
    def repl(m):
        nonlocal changed
        block = m.group(1)
        ok, err = try_load(block)
        if ok:
            return m.group(0)
        cleaned = clean_json_text(block)
        ok2, err2 = try_load(cleaned)
        if ok2:
            changed = True
            return '```json\n' + cleaned + '\n```'
        else:
            # keep original if we can't fix
            return m.group(0)
    new_text = CODE_FENCE_RE.sub(repl, text)
    if changed:
        # Write changes in-place (no .bak backups per project policy)
        path.write_text(new_text, encoding='utf-8')
    return changed


def main():
    md_files = list(DOCS.rglob('*.md'))
    fixed_files = []
    for f in md_files:
        try:
            if process_file(f):
                fixed_files.append(str(f.relative_to(ROOT)))
        except Exception as e:
            print(f"ERROR processing {f}: {e}")
    print(f"Processed {len(md_files)} markdown files")
    print(f"Fixed {len(fixed_files)} files:")
    for ff in fixed_files[:50]:
        print(' -', ff)

if __name__ == '__main__':
    main()
