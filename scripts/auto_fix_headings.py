#!/usr/bin/env python3
"""
Auto-fix Markdown heading hierarchy issues.
Fixes:
  - H1 -> H3 jumps (adds missing H2)
  - H1 -> H4+ jumps (adds missing intermediate headers)
"""

import re
from pathlib import Path

def fix_heading_hierarchy(file_path):
    """Fix heading hierarchy in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False, "Cannot read"
    
    original_content = content
    lines = content.split('\n')
    fixed_lines = []
    prev_level = None
    inserted = 0
    
    for i, line in enumerate(lines):
        # Match heading lines
        match = re.match(r'^(#+)\s', line)
        
        if match:
            curr_level = len(match.group(1))
            
            # Check if there's a jump > 1
            if prev_level is not None and curr_level - prev_level > 1:
                # Insert missing intermediate headers
                for missing_level in range(prev_level + 1, curr_level):
                    # Create placeholder heading
                    hashes = '#' * missing_level
                    placeholder = f"{hashes} [Auto-generated heading level {missing_level}]"
                    fixed_lines.append(placeholder)
                    inserted += 1
            
            fixed_lines.append(line)
            prev_level = curr_level
        else:
            fixed_lines.append(line)
    
    fixed_content = '\n'.join(fixed_lines)
    
    # Write back if changed
    if fixed_content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True, f"Fixed {inserted} heading jumps"
        except:
            return False, "Cannot write"
    
    return False, "No changes"

def main():
    docs_dir = Path('./docs')
    files_fixed = 0
    total_jumps = 0
    
    print("🔧 Fixing Markdown heading hierarchy...\n")
    
    for file_path in docs_dir.rglob('*.md'):
        fixed, msg = fix_heading_hierarchy(file_path)
        if fixed:
            # Count jumps from message
            try:
                jumps = int(msg.split()[1])
                total_jumps += jumps
                files_fixed += 1
                print(f"  ✅ {file_path.relative_to('.')}: {msg}")
            except:
                files_fixed += 1
                print(f"  ✅ {file_path.relative_to('.')}")
    
    print(f"\n✅ Fixed {files_fixed} files")
    print(f"📊 Total heading jumps corrected: {total_jumps}")

if __name__ == '__main__':
    main()
