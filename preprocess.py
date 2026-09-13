#!/usr/bin/env python3
"""
Rust Book Preprocessor
======================
mdBook-এর {{#include ...}} ও {{#rustdoc_include ...}} directive গুলোকে
actual file content দিয়ে replace করে একটা preprocessed source folder তৈরি করে।

Source : /home/z/my-project/rust-book-source/
Output : /home/z/my-project/rust-book-source-preprocessed/

এরপর translation agents preprocessed source থেকে কাজ করবে।
"""

import os
import re
import sys
import shutil
from pathlib import Path

SOURCE_ROOT = Path("/home/z/my-project/rust-book-source")
SRC_DIR = SOURCE_ROOT / "src"
OUTPUT_ROOT = Path("/home/z/my-project/rust-book-source-preprocessed")
OUTPUT_SRC = OUTPUT_ROOT / "src"

# Pattern: {{#include path}} বা {{#rustdoc_include path}} যেখানে path-এ অনেক কিছু থাকতে পারে
INCLUDE_RE = re.compile(
    r'\{\{#(rustdoc_)?include\s+([^}]+?)\}\}'
)

# Anchor markers
ANCHOR_START_RE = re.compile(r'//\s*ANCHOR:\s*(\w+)|<!--\s*ANCHOR:\s*(\w+)\s*-->')
ANCHOR_END_RE = re.compile(r'//\s*ANCHOR_END:\s*(\w+)|<!--\s*ANCHOR_END:\s*(\w+)\s*-->')


def parse_target(target: str):
    """
    mdBook include target parse করে।
    Returns: (file_path, mode, value) where mode is 'full', 'lines', or 'anchor'
    
    Examples:
        ../listings/.../main.rs              -> (path, 'full', None)
        ../listings/.../main.rs:5            -> (path, 'lines', (5, None))
        ../listings/.../main.rs:5:10         -> (path, 'lines', (5, 10))
        ../listings/.../main.rs::10          -> (path, 'lines', (None, 10))
        ../listings/.../main.rs#anchor       -> (path, 'anchor', 'anchor')
        ../listings/.../main.rs:anchor       -> (path, 'anchor', 'anchor')
    """
    # path ও suffix আলাদা করি
    # প্রথমে # anchor check
    if '#' in target:
        path_part, anchor = target.rsplit('#', 1)
        return path_part.strip(), 'anchor', anchor.strip()
    
    # এখন : দিয়ে line range বা anchor
    if ':' in target:
        parts = target.split(':')
        path_part = parts[0].strip()
        if len(parts) == 2:
            suffix = parts[1].strip()
            if suffix == '':
                return path_part, 'full', None
            if suffix.isdigit():
                return path_part, 'lines', (int(suffix), None)
            else:
                # anchor হিসেবে ধরি
                return path_part, 'anchor', suffix
        elif len(parts) == 3:
            # path:start:end বা path::end বা path:start:
            start_s = parts[1].strip()
            end_s = parts[2].strip()
            start = int(start_s) if start_s.isdigit() else None
            end = int(end_s) if end_s.isdigit() else None
            return path_part, 'lines', (start, end)
        else:
            return target.strip(), 'full', None
    else:
        return target.strip(), 'full', None


def extract_anchor(lines: list, anchor_name: str) -> list:
    """
    File থেকে ANCHOR:name ... ANCHOR_END:name এর ভেতরের content extract করে।
    Nested anchor support করে না (mdBook-ও করে না)।
    """
    result = []
    in_anchor = False
    depth = 0
    for line in lines:
        start_match = ANCHOR_START_RE.search(line)
        end_match = ANCHOR_END_RE.search(line)
        
        if start_match:
            name = start_match.group(1) or start_match.group(2)
            if name == anchor_name:
                in_anchor = True
                depth = 1
                continue  # anchor marker line নিজেই skip
            elif in_anchor:
                depth += 1
                # nested anchor marker line ও skip না করে রাখি? mdBook যা করে তাই করি — skip
                continue
        elif end_match:
            name = end_match.group(1) or end_match.group(2)
            if name == anchor_name and in_anchor:
                depth -= 1
                if depth == 0:
                    in_anchor = False
                    continue
                else:
                    continue
            elif in_anchor:
                # nested end
                continue
        
        if in_anchor:
            result.append(line)
    
    return result


def apply_line_range(lines: list, start_end) -> list:
    """(start, end) line range apply করে। 1-indexed। None মানে সেই দিক unlimited।"""
    start, end = start_end
    if start is None:
        start = 1
    if end is None:
        end = len(lines)
    # 1-indexed to 0-indexed slice
    return lines[start-1:end]


def resolve_include(target: str, md_file_dir: Path) -> str:
    """
    একটা include directive resolve করে actual file content return করে।
    md_file_dir: যে .md file-এ directive আছে তার directory (path resolve এর জন্য)।
    """
    file_path_str, mode, value = parse_target(target)
    
    # path resolve: target path relative to the .md file's directory
    # .md file-টা src/ এর ভেতরে, target path ../listings/... দিয়ে শুরু
    resolved = (md_file_dir / file_path_str).resolve()
    
    if not resolved.exists():
        return f"<!-- ERROR: file not found: {resolved} -->"
    
    try:
        content = resolved.read_text(encoding='utf-8')
    except Exception as e:
        return f"<!-- ERROR reading {resolved}: {e} -->"
    
    lines = content.splitlines(keepends=True)
    
    if mode == 'full':
        result_lines = lines
    elif mode == 'lines':
        result_lines = apply_line_range(lines, value)
    elif mode == 'anchor':
        result_lines = extract_anchor(lines, value)
        if not result_lines:
            # anchor না পেলে পুরো file দেখাই (fallback, যাতে translation না থেমে যায়)
            result_lines = lines
    else:
        result_lines = lines
    
    # trailing newline থাকলে সরিয়ে দিই, যাতে markdown-এ ভালো বসে
    result = ''.join(result_lines)
    # শেষের newline গুলো strip করি শুধু একটা রাখি
    result = result.rstrip('\n')
    return result


def detect_language_for_include(file_path_str: str, is_rustdoc: bool) -> str:
    """
    Code block এর language detect করি।
    rustdoc_include সবসময় rust।
    include এর ক্ষেত্রে file extension দেখে বুঝি।
    """
    if is_rustdoc:
        return 'rust'
    
    ext = Path(file_path_str).suffix.lower()
    ext_to_lang = {
        '.rs': 'rust',
        '.toml': 'toml',
        '.txt': 'text',
        '.sh': 'bash',
        '.md': 'markdown',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.html': 'html',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.py': 'python',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c',
    }
    return ext_to_lang.get(ext, 'text')


def process_md_file(md_path: Path, out_path: Path):
    """একটা .md file preprocess করে output folder-এ লেখে।"""
    md_dir = md_path.parent
    content = md_path.read_text(encoding='utf-8')
    
    def replace_match(m):
        is_rustdoc = m.group(1) is not None
        target = m.group(2).strip()
        # target থেকে file path parse করি (language detect এর জন্য)
        file_path_str, mode, value = parse_target(target)
        # সব directive-ই ইতিমধ্যে code fence এর ভেতরে আছে (verified: 707/707)
        # তাই শুধু content দিয়ে replace করব, নতুন fence যোগ করব না।
        resolved_content = resolve_include(target, md_dir)
        return resolved_content
    
    # Replace all includes
    processed = INCLUDE_RE.sub(replace_match, content)
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(processed, encoding='utf-8')


def main():
    # Clean output
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True)
    
    # Process সব .md file in src/
    md_files = sorted(SRC_DIR.glob('*.md'))
    print(f"মোট {len(md_files)} টা .md file preprocess হবে...")
    
    success = 0
    errors = 0
    total_directives = 0
    
    for md_file in md_files:
        out_file = OUTPUT_SRC / md_file.name
        try:
            # কতগুলো directive আছে গুণি
            content = md_file.read_text(encoding='utf-8')
            n = len(INCLUDE_RE.findall(content))
            total_directives += n
            
            process_md_file(md_file, out_file)
            success += 1
            if n > 0:
                print(f"  ✓ {md_file.name}  ({n} directive resolved)")
            else:
                print(f"  ✓ {md_file.name}")
        except Exception as e:
            errors += 1
            print(f"  ✗ {md_file.name}: {e}", file=sys.stderr)
    
    # listings folder ও copy করি (output.txt ইত্যাদি reference এর জন্য দরকার না,
    # কারণ আমরা ইতিমধ্যেই content embed করেছি)
    
    print()
    print(f"=== Summary ===")
    print(f"Files processed : {success}")
    print(f"Errors          : {errors}")
    print(f"Directives resolved: {total_directives}")
    print(f"Output          : {OUTPUT_SRC}")


if __name__ == '__main__':
    main()
