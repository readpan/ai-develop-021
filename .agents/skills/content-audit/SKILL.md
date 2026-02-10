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

- Missing images (referenced in markdown but file doesn't exist) -> Reported as PENDING
- Placeholder images (file exists but is a tiny stub) -> Reported as PENDING
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
- **IMAGE_NAMING**: Image filename doesn't follow `{section}-{description}.png` convention. Action: rename for consistency.
- **STUB_PAGE**: Page has fewer than 5 non-empty lines of content. Action: write content or remove placeholder.

## Manual Review Checklist

After running the automated audit, manually review:

1. **Writing style consistency**: 「你」not「您」, conversational tone, no unexplained jargon
2. **Prompt examples**: All prompts in `>` blockquote, complete sentences in Chinese
3. **AI response descriptions**: Describes behavior, never pastes actual AI output
4. **VitePress config sync**: Every page file has a corresponding sidebar entry in `docs/.vitepress/config.ts`
5. **Page flow**: Each non-FAQ page ends with "下一步" linking to the next logical page
6. **Comparison teaching**: Pages introducing new concepts include contrast with what students already know
7. **Writing quality**: Check for awkward phrasing, forced humor, or confusing expressions (see details below)

## Writing Quality Review

Read each page and flag expressions that would make a beginner pause or feel confused. The tutorial tone should be **warm and encouraging, but not gimmicky**.

### Rules

1. **No forced humor or slang**: Jokes that require cultural context or feel out of place break trust with beginners. Keep humor natural and light.
2. **No disruptive parenthetical asides**: Parenthetical expressions that contradict or undercut the main sentence confuse readers.
3. **Metaphors must be self-explanatory**: If a metaphor needs its own explanation, replace it with plain language.
4. **Consistent register**: Don't mix formal explanations with overly casual interjections in the same paragraph.

### Examples

| ❌ 有问题                | ✅ 改后                          | 原因                                 |
| ------------------------ | -------------------------------- | ------------------------------------ |
| 你刚刚亲手（用嘴）做到的 | 你刚刚通过和 AI 对话，亲手做到的 | 括号里的"用嘴"打断阅读、语义奇怪     |
| 恭喜你成为了一个码农！   | 恭喜你完成了第一个应用！         | "码农"是圈内自嘲用语，初学者可能困惑 |
| 这就像给代码吃了炫迈     | 这会让页面的响应速度明显变快     | 广告梗不是所有读者都能理解           |
| AI 这波操作很秀          | AI 会自动帮你完成这些步骤        | 网络用语在教程中显得不专业           |

## Fixing Issues

Process audit results top-to-bottom. For each category:

1. **MISSING_IMAGE**: List all for the screenshot author — these are expected during development
2. **PLACEHOLDER_IMAGE**: Same as above — list for the screenshot author to replace with real screenshots
3. **MISSING_SECTION**: Add missing sections using the tutorial-writer skill's format
4. **BROKEN_LINK**: Fix paths; use relative paths like `./page.md` or `/section/page`
5. **IMAGE_NAMING**: Rename files and update markdown references (remove sequential numbering)
6. **STUB_PAGE**: Write content or remove the file and its sidebar/nav entries
