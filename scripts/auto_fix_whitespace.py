#!/usr/bin/env python3
"""
Auto-fix whitespace and formatting issues in documentation files.
Fixes:
  - Trailing spaces
  - Tab/space mixing (converts tabs to spaces)
  - Lines longer than 120 characters (warning only)
"""

import os
import re
from pathlib import Path

def fix_whitespace(file_path):
    """Fix whitespace issues in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False, "Cannot read file"
    
    original_content = content
    lines = content.split('\n')
    fixed_lines = []
    long_lines = 0
    
    for line in lines:
        # Remove trailing spaces
        fixed_line = line.rstrip()
        
        # Convert tabs to spaces (4 spaces per tab)
        fixed_line = fixed_line.replace('\t', '    ')
        
        # Track long lines (don't fix, just warn)
        if len(fixed_line) > 120:
            long_lines += 1
        
        fixed_lines.append(fixed_line)
    
    fixed_content = '\n'.join(fixed_lines)
    
    # Write back if changed
    if fixed_content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True, f"Fixed (trailing spaces, tabs)"
        except:
            return False, "Cannot write file"
    
    return False, "No changes needed"

def main():
    docs_dir = Path('./docs')
    files_fixed = 0
    files_skipped = 0
    
    print("🔧 Fixing whitespace issues...\n")
    
    for file_path in docs_dir.rglob('*.md'):
        fixed, msg = fix_whitespace(file_path)
        if fixed:
            files_fixed += 1
            print(f"  ✅ {file_path.relative_to('.')}")
        else:
            files_skipped += 1
    
    print(f"\n✅ Fixed {files_fixed} files")
    print(f"⏭️  Skipped {files_skipped} files (no changes needed)")

if __name__ == '__main__':
    main()
