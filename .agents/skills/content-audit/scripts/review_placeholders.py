#!/usr/bin/env python3
"""
Interactive script to review and prune placeholder images in markdown files.
Scans for images that are either missing or valid placeholders (<1KB),
shows them in context, and allows the user to keeps or delete them.

Usage:
    python3 review_placeholders.py [docs_dir]
"""

import sys
import re
from pathlib import Path

# Configuration
DOCS_DIR = "docs"
PLACEHOLDER_SIZE_THRESHOLD = 1024
CONTEXT_LINES = 5

# Regex to find markdown images: ![alt](path)
# Capture groups: 1=alt, 2=path
IMAGE_PATTERN = re.compile(r"(!\[([^\]]*)\]\(([^)]+)\))")

def get_context(content, match_start, match_end, lines=3):
    """Extract surrounding lines of text for context."""
    before = content[:match_start].splitlines()
    after = content[match_end:].splitlines()
    
    # Get last N lines from before
    ctx_before = "\n".join(before[-lines:]) if before else ""
    # Get first N lines from after
    ctx_after = "\n".join(after[:lines]) if after else ""
    
    return ctx_before, ctx_after

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else DOCS_DIR
    root = Path(target_dir).resolve()
    
    if not root.is_dir():
        print(f"Error: {root} is not a directory.")
        sys.exit(1)
        
    md_files = sorted(root.rglob("*.md"))
    candidates = []

    print(f"Scanning {len(md_files)} files in {root}...\n")

    # 1. Scan phase
    for original_filepath in md_files:
        # Skip plans
        if "plans" in original_filepath.parts:
            continue
            
        try:
            content = original_filepath.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Skipping {original_filepath}: {e}")
            continue

        for match in IMAGE_PATTERN.finditer(content):
            full_tag = match.group(1) # ![alt](path)
            alt_text = match.group(2)
            img_path = match.group(3)
            
            # Skip external links
            if img_path.startswith(("http://", "https://")):
                continue
                
            # Resolve path
            # Markdown paths are relative to the file
            abs_img_path = (original_filepath.parent / img_path).resolve()
            
            is_candidate = False
            reason = ""
            
            if not abs_img_path.exists():
                is_candidate = True
                reason = "Detailed: MISSING FILE"
            else:
                try:
                    size = abs_img_path.stat().st_size
                    if size < PLACEHOLDER_SIZE_THRESHOLD:
                        is_candidate = True
                        reason = f"Detailed: PLACEHOLDER ({size} bytes)"
                except OSError:
                    pass
            
            if is_candidate:
                candidates.append({
                    "file": original_filepath,
                    "full_tag": full_tag,
                    "alt": alt_text,
                    "path": img_path,
                    "reason": reason,
                    "start": match.start(),
                    "end": match.end()
                })

    if not candidates:
        print("No placeholder or missing images found.")
        return

    print(f"Found {len(candidates)} candidates. Starting review...\n")
    
    # 2. Review phase
    # We process file by file to handle offsets correctly if we modify
    # However, easy way: Read file fresh each time? No, inefficient.
    # Group by file
    
    from collections import defaultdict
    files_map = defaultdict(list)
    for c in candidates:
        files_map[c["file"]].append(c)
        
    total_processed = 0
    total_deleted = 0
    
    for filepath, items in files_map.items():
        # Read content fresh for each file
        content = filepath.read_text(encoding="utf-8")
        new_content = content
        
        # Sort items by position descending so deletions don't mess up earlier offsets?
        # Actually string replacement is safer if we have unique tags.
        # But image tags might be identical.
        # Let's iterate and ask user. If delete, we mark for deletion.
        # Then regenerate file content.
        
        valid_items = []
        # Re-find items in current content to be sure of context
        # This is safer than relying on old offsets
        
        # We will iterate through current matches in the file
        # If a match corresponds to a candidate, we ask.
        
        # Creating a list of exact strings to look for might be ambiguous if same image used twice.
        # But in this project context, that's rare or okay.
        
        # Let's just process the list we found.
        # To avoid offset issues, we can just replace the exact string if unique, 
        # or rebuild the file line by line?
        # Simplest robust way: Split into lines.
        
        lines = content.splitlines()
        # We need to map our candidates to line numbers to show context better?
        # Regex finditer gives character offsets.
        
        # Let's stick to the character offset approach but be careful.
        # Actually, simpler: prompt for all, store decisions, then apply all changes to file at once.
        # Reverse order application ensures offsets remain valid for earlier items.
        
        items.sort(key=lambda x: x["start"], reverse=True)
        
        modified = False
        
        for item in items:
            total_processed += 1
            
            # Extract context from CURRENT content (in memory, unchanged yet)
            # wait, if we iterate reverse, the context for earlier items is fine.
            
            ctx_start = max(0, item["start"] - 200)
            ctx_end = min(len(content), item["end"] + 200)
            
            display_context = content[ctx_start:ctx_end]
            # Highlight the tag
            display_context = display_context.replace(item["full_tag"], f"\033[93m{item['full_tag']}\033[0m")
            
            print(f"\n[{total_processed}/{len(candidates)}] File: {filepath}")
            print(f"Image: {item['path']}")
            print(f"Alt: {item['alt']}")
            print(f"Reason: {item['reason']}")
            print("-" * 40)
            print(display_context.strip())
            print("-" * 40)
            
            while True:
                choice = input("Action (k=keep, d=delete, q=quit) [k]: ").strip().lower()
                if choice == '' or choice == 'k':
                    print("Keeping.")
                    break
                elif choice == 'd':
                    print("Deleting...")
                    # We will apply this deletion to 'new_content'
                    # Since we are iterating reverse, we can cut out the slice
                    # text[:start] + text[end:]
                    # But wait, 'content' is the reference for offsets.
                    # 'new_content' needs to be mutable or reconstructed.
                    
                    # Reconstruction approach:
                    # We are in a loop iterating REVERSE.
                    # content (original) is static.
                    # We can build a list of deletion ranges.
                    pass 
                    break
                elif choice == 'q':
                    print("Quitting.")
                    sys.exit(0)
                else:
                    print("Invalid choice.")
            
            if choice == 'd':
                # Apply deletion
                # Re-read content into a mutable structure? 
                # Since we process reverse, we can just slice the string that accumulates changes?
                # Actually, if we just keep `content` as the source of truth for offsets...
                # We can't slice `content` because that would shift offsets for the *next* item (which is previous in file).
                # Wait, if we iterate reverse (end of file -> start),
                # Deleting the end DOES NOT affect offsets of the start.
                # So we can just modify `content` directly!
                
                content = content[:item["start"]] + content[item["end"]:]
                modified = True
                total_deleted += 1
        
        if modified:
            filepath.write_text(content, encoding="utf-8")
            print(f"Updated {filepath}")

    print(f"\nDone. Processed {total_processed} images. Deleted {total_deleted}.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
