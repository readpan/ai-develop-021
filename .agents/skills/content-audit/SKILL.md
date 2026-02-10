---
name: content-audit
description: Audit tutorial content for the "AI 开发 0 到 1" VitePress site. Use when checking content quality, finding missing screenshots, validating page structure, checking internal links, or reviewing content consistency before deployment. Run the audit script for automated checks, then review results and fix issues.
---

# Content Audit

Audit tutorial content quality for the "AI 开发 0 到 1" site.

## Quick Start

Run the audit script from the project root:

```bash
python3 .agents/skills/content-audit/scripts/audit.py docs/
```

The script checks all `.md` files under `docs/` and reports:
- Missing images (referenced in markdown but file doesn't exist)
- Placeholder images (file exists but is a tiny stub, not a real screenshot)
- Missing required sections per page type
- Broken internal links (links to `.md` files that don't exist)
- Image naming convention violations
- Empty or stub pages

## Interpreting Results

The script outputs categorized findings:

- **MISSING_IMAGE**: Image placeholder referenced but no file on disk. Action: screenshot needed or path typo.
- **PLACEHOLDER_IMAGE**: Image file exists but is too small to be a real screenshot (e.g., 1x1 pixel stub). Action: replace with actual screenshot.
- **MISSING_SECTION**: Page lacks a required section (本节目标, 下一步, etc.). Action: add the section or confirm it's intentionally omitted (FAQ/index pages exempt).
- **BROKEN_LINK**: Internal markdown link target doesn't exist. Action: fix the link path.
- **IMAGE_NAMING**: Image filename doesn't follow `{section}-{NN}-{description}.png` convention. Action: rename for consistency.
- **STUB_PAGE**: Page has fewer than 5 non-empty lines of content. Action: write content or remove placeholder.

## Manual Review Checklist

After running the automated audit, manually review:

1. **Writing style consistency**: 「你」not「您」, conversational tone, no unexplained jargon
2. **Prompt examples**: All prompts in `>` blockquote, complete sentences in Chinese
3. **AI response descriptions**: Describes behavior, never pastes actual AI output
4. **VitePress config sync**: Every page file has a corresponding sidebar entry in `docs/.vitepress/config.ts`
5. **Page flow**: Each non-FAQ page ends with "下一步" linking to the next logical page
6. **Comparison teaching**: Pages introducing new concepts include contrast with what students already know

## Fixing Issues

Process audit results top-to-bottom. For each category:

1. **MISSING_IMAGE**: List all for the screenshot author — these are expected during development
2. **PLACEHOLDER_IMAGE**: Same as above — list for the screenshot author to replace with real screenshots
3. **MISSING_SECTION**: Add missing sections using the tutorial-writer skill's format
3. **BROKEN_LINK**: Fix paths; use relative paths like `./page.md` or `/section/page`
4. **IMAGE_NAMING**: Rename files and update markdown references
5. **STUB_PAGE**: Write content or remove the file and its sidebar/nav entries
