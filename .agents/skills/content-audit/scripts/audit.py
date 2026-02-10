#!/usr/bin/env python3
"""
Content audit script for the "AI 开发 0 到 1" tutorial site.

Scans markdown files under the docs directory and reports:
- Missing images (referenced but file doesn't exist)
- Placeholder images (file exists but is a tiny stub, not a real screenshot)
- Missing required sections per page type
- Broken internal links
- Image naming convention violations
- Empty/stub pages

Usage:
    python3 audit.py <docs_directory>

Example:
    python3 audit.py docs/
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict


def find_md_files(docs_dir: str) -> list[Path]:
    """Find all markdown files under docs directory."""
    return sorted(Path(docs_dir).rglob("*.md"))


def classify_page(filepath: Path) -> str:
    """Classify a page by its type based on path and name."""
    name = filepath.stem
    parent = filepath.parent.name

    if name == "index":
        return "index"
    if name == "faq":
        return "faq"
    if parent == "plans":
        return "plan"
    if name.startswith("intro-") or name.startswith("what-is-"):
        return "concept"
    return "tutorial"


REQUIRED_SECTIONS = {
    "tutorial": ["本节目标", "下一步"],
    "concept": ["本节目标", "下一步"],
    "faq": ["常见问题"],
    "index": [],
    "plan": [],
}

IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_PATTERN = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
HEADING_PATTERN = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)
IMAGE_NAME_CONVENTION = re.compile(r"^[a-z0-9-]+-[a-z0-9-]+\.\w+$")

# Real screenshots are typically >1KB; placeholder stubs (e.g., 1x1 PNG) are much smaller
PLACEHOLDER_SIZE_THRESHOLD = 1024


class AuditResult:
    def __init__(self):
        self.issues = defaultdict(list)

    def add(self, category: str, filepath: str, detail: str):
        self.issues[category].append((filepath, detail))

    def print_report(self):
        total = sum(len(v) for v in self.issues.values())
        if total == 0:
            print("✅ No issues found!")
            return

        print(f"\n{'='*60}")
        print(f"  AUDIT REPORT — {total} issue(s) found")
        print(f"{'='*60}\n")

        # 1. Prioritize Pending Screenshots
        pending = self.issues.get("PENDING_SCREENSHOT", [])
        if pending:
            print(f"[PENDING SCREENSHOTS] ({len(pending)} images to capture)")
            print(f"{'-'*60}")
            for filepath, info in pending:
                # info is expected to be a dict for this category
                print(f"  📄 Page: {filepath}")
                print(f"     Save to: {info['img_path']}")
                print(f"     Capture: {info['alt_text']}")
                print()
            print()

        order = [
            "MISSING_IMAGE",
            # "PENDING_SCREENSHOT" is handled separately above
            "MISSING_SECTION",
            "BROKEN_LINK",
            "IMAGE_NAMING",
            "STUB_PAGE",
        ]
        for cat in order:
            items = self.issues.get(cat, [])
            if not items:
                continue
            print(f"[{cat}] ({len(items)} issue(s))")
            print(f"{'-'*40}")
            for filepath, detail in items:
                print(f"  {filepath}")
                print(f"    → {detail}")
            print()

        # Summary
        print(f"{'='*60}")
        print("  SUMMARY")
        print(f"{'='*60}")
        
        count = len(self.issues.get("PENDING_SCREENSHOT", []))
        if count > 0:
            print(f"  PENDING_SCREENSHOT: {count}")

        for cat in order:
            count = len(self.issues.get(cat, []))
            if count > 0:
                print(f"  {cat}: {count}")
        print(f"  TOTAL: {total}")
        print()


def audit_images(filepath: Path, content: str, result: AuditResult):
    """Check for missing images and naming convention violations."""
    for match in IMAGE_PATTERN.finditer(content):
        alt_text, img_path = match.group(1), match.group(2)

        # Skip external URLs
        if img_path.startswith("http://") or img_path.startswith("https://"):
            continue

        # Resolve relative path
        img_full = (filepath.parent / img_path).resolve()
        rel_path = str(filepath)

        # Check if file exists
        if not img_full.exists():
            result.add("MISSING_IMAGE", rel_path, f"Image not found: {img_path} (alt: {alt_text})")
        else:
            # Check if file is a placeholder stub (too small to be a real screenshot)
            file_size = img_full.stat().st_size
            if file_size < PLACEHOLDER_SIZE_THRESHOLD:
                # Use a dict for structured output in the report
                result.add("PENDING_SCREENSHOT", rel_path, {
                    "img_path": img_path,
                    "alt_text": alt_text
                })

        # Check naming convention
        img_name = Path(img_path).name
        if not IMAGE_NAME_CONVENTION.match(img_name):
            result.add("IMAGE_NAMING", rel_path, f"Non-standard name: {img_name} (expected: section-description.ext)")


def audit_sections(filepath: Path, content: str, page_type: str, result: AuditResult):
    """Check for missing required sections."""
    required = REQUIRED_SECTIONS.get(page_type, [])
    if not required:
        return

    headings = [m.group(1).strip() for m in HEADING_PATTERN.finditer(content)]
    rel_path = str(filepath)

    for section in required:
        if not any(section in h for h in headings):
            # Check if section text appears anywhere (could be inline)
            if section not in content:
                result.add("MISSING_SECTION", rel_path, f"Missing required section: '{section}' (page type: {page_type})")


def audit_links(filepath: Path, content: str, docs_dir: Path, result: AuditResult):
    """Check for broken internal links."""
    for match in LINK_PATTERN.finditer(content):
        link_text, link_path = match.group(1), match.group(2)

        # Skip external URLs, anchors, and special links
        if link_path.startswith(("http://", "https://", "#", "mailto:")):
            continue

        # Strip anchor from path
        clean_path = link_path.split("#")[0]
        if not clean_path:
            continue

        # Resolve the link
        if clean_path.startswith("/"):
            # Absolute path from docs root
            target = docs_dir / clean_path.lstrip("/")
        else:
            # Relative path
            target = (filepath.parent / clean_path).resolve()

        # VitePress links: /guide/foo → docs/guide/foo.md or docs/guide/foo/index.md
        if not target.suffix:
            md_target = target.with_suffix(".md")
            index_target = target / "index.md"
            if not md_target.exists() and not index_target.exists() and not target.exists():
                result.add("BROKEN_LINK", str(filepath), f"Link target not found: {link_path} (text: {link_text})")
        elif not target.exists():
            result.add("BROKEN_LINK", str(filepath), f"Link target not found: {link_path} (text: {link_text})")


def audit_stub(filepath: Path, content: str, result: AuditResult):
    """Check for stub/empty pages."""
    lines = [line for line in content.strip().splitlines() if line.strip()]
    if len(lines) < 5:
        result.add("STUB_PAGE", str(filepath), f"Only {len(lines)} non-empty line(s) of content")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 audit.py <docs_directory>")
        sys.exit(1)

    docs_dir = Path(sys.argv[1]).resolve()
    if not docs_dir.is_dir():
        print(f"Error: {docs_dir} is not a directory")
        sys.exit(1)

    md_files = find_md_files(docs_dir)
    result = AuditResult()

    # Make paths relative to cwd for cleaner output
    cwd = Path.cwd()

    for filepath in md_files:
        # Skip plans directory
        if "plans" in filepath.parts:
            continue

        content = filepath.read_text(encoding="utf-8")
        page_type = classify_page(filepath)

        # Make filepath relative for display
        try:
            display_path = filepath.relative_to(cwd)
        except ValueError:
            display_path = filepath

        audit_images(display_path, content, result)
        audit_sections(display_path, content, page_type, result)
        audit_links(filepath, content, docs_dir, result)
        audit_stub(display_path, content, result)

    result.print_report()

    # Exit with non-zero if issues found
    total = sum(len(v) for v in result.issues.values())
    sys.exit(1 if total > 0 else 0)


if __name__ == "__main__":
    main()
