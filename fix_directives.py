#!/usr/bin/env python3
"""
Rust Book Translation — Directive Fixer
========================================
আগে অনুবাদ করা .md ফাইলগুলোতে যে {{#include ...}} directive গুলো এখনও
unresolved আছে, সেগুলোকে actual code content দিয়ে replace করে।
বাকি বাংলা অনুবাদ অপরিবর্তিত থাকে।

Target: /home/z/my-project/rust-book-bn/*.md
Source for resolution: /home/z/my-project/rust-book-source/  (original repo)
"""

import re
import sys
from pathlib import Path

# import preprocessing functions
sys.path.insert(0, '/home/z/my-project')
from preprocess import INCLUDE_RE, parse_target, resolve_include

TRANSLATED_DIR = Path("/home/z/my-project/rust-book-bn")
SOURCE_SRC_DIR = Path("/home/z/my-project/rust-book-source/src")


def fix_file(translated_path: Path) -> int:
    """একটা translated .md file-এ সব directive resolve করে। Return: কতগুলো fix হলো।"""
    content = translated_path.read_text(encoding='utf-8')
    md_dir = SOURCE_SRC_DIR  # directive path ../listings/... resolve করার জন্য source src dir
    
    count = 0
    
    def replace_match(m):
        nonlocal count
        count += 1
        target = m.group(2).strip()
        # সব directive-ই code fence এর ভেতরে — শুধু content দিয়ে replace
        return resolve_include(target, md_dir)
    
    fixed = INCLUDE_RE.sub(replace_match, content)
    
    if count > 0:
        translated_path.write_text(fixed, encoding='utf-8')
    
    return count


def main():
    md_files = sorted(TRANSLATED_DIR.glob('*.md'))
    # _TRANSLATION_GUIDE.md skip করি
    md_files = [f for f in md_files if not f.name.startswith('_')]
    
    total_fixed = 0
    files_fixed = 0
    
    print(f"Checking {len(md_files)} translated files for unresolved directives...")
    print()
    
    for md_file in md_files:
        n = fix_file(md_file)
        if n > 0:
            files_fixed += 1
            total_fixed += n
            print(f"  ✓ {md_file.name}  ({n} directive fixed)")
    
    print()
    print(f"=== Summary ===")
    print(f"Files fixed         : {files_fixed}")
    print(f"Directives resolved : {total_fixed}")
    
    # verify কোনো directive বাকি আছে কিনা
    remaining = 0
    for md_file in md_files:
        content = md_file.read_text(encoding='utf-8')
        remaining += len(INCLUDE_RE.findall(content))
    print(f"Remaining directives: {remaining}")


if __name__ == '__main__':
    main()
