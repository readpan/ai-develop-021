---
name: tutorial-writer
description: Write and edit tutorial pages for the "AI 开发 0 到 1" VitePress site. Use when creating new tutorial content, adding new project sections, or editing existing tutorial pages. Enforces the project's standardized page format (本节目标 → 正常流程 → 提示词对比 → 常见问题), image placeholder conventions, writing style for zero-experience readers, and VitePress config updates.
---

# Tutorial Writer

Write tutorial pages for the "AI 开发 0 到 1" Vibe Coding教程 site.

## Target Audience

Absolute beginners: no HTML/CSS/JS knowledge, never used a terminal. Write as if explaining to a friend who has never coded. Avoid jargon; when technical terms are unavoidable, explain them in plain language inline.

## Page Types

### 1. Normal Tutorial Page (功能模块页)

Required sections in order:

```markdown
# 页面标题

## 本节目标

一句话说清楚这一节要做什么。

## [功能步骤sections — 按自然流程拆分]

每个步骤:
- 描述要做什么
- 给出 prompt 示例（用 blockquote）
- 描述 AI 的响应
- 截图占位符

## 提示词对比

（可选，在合适的页面添加）
展示不同 prompt 的效果差异，帮学员建立"怎么说决定 AI 怎么做"的核心认知。

## 常见问题 / ::: tip 内联提示

常见问题用"告诉 AI："+ blockquote prompt 的模式。

## 下一步

一句话衔接下一节内容。
```

### 2. FAQ Page (常见问题页)

Each project's last page. Structure:

```markdown
# 常见问题

## [问题分类]

### [具体问题描述]

解释 + "告诉 AI：" + blockquote prompt 模式。
```

### 3. Intro/Concept Page (概念引入页)

For pages like `intro-mcp.md`, `what-is-vibe-coding.md`:

```markdown
# 标题

## 本节目标

## [概念解释 — 用比喻，不用术语]

## 实际体验：[动手环节]

## [概念的价值总结]

## 常见问题

## 下一步
```

## Writing Rules

1. **Prompt examples**: Always use `>` blockquote, Chinese content, complete sentence
2. **AI response descriptions**: Describe what AI does, never paste actual AI output (it varies)
3. **Tone**: 「你」not「您」; conversational, encouraging; acknowledge confusion as normal
4. **Error handling**: Don't enumerate errors. Teach the pattern: describe problem to AI → AI fixes it
5. **VitePress features**: Use `::: tip` for reassuring side notes, never `::: danger` or `::: warning` (beginners scare easily)
6. **No code blocks in tutorials**: Students don't write code. Only show terminal output or URLs when needed
7. **Contrast teaching**: When a page introduces something new (e.g., Vite vs plain HTML), add explicit comparison with what they already know

## Image Placeholders

Format: `![Alt text describing the screenshot](./images/{section}-{NN}-{description}.png)`

Naming rules:
- `{section}`: slug of the page (e.g., `create-project`, `setup`, `intro-mcp`)
- `{NN}`: two-digit sequential number starting from `01`
- `{description}`: short English description (e.g., `open-folder`, `prompt`, `browser`, `result`)

Examples:
```
![创建项目后的Cursor界面](./images/create-project-03-files.png)
![终端显示开发服务器地址](./images/setup-04-dev-server.png)
```

Each image's alt text must describe what the screenshot shows in Chinese, specific enough for the screenshot author to reproduce.

## Adding a New Project Section

When adding a new project (e.g., a third tutorial project):

1. Create directory: `docs/{project-slug}/` with `images/` subfolder
2. Create pages following the standard format above
3. Create an FAQ page as the last page
4. Update `docs/.vitepress/config.ts`:
   - Add nav entry in `themeConfig.nav`
   - Add sidebar section in `themeConfig.sidebar` under `'/{project-slug}/'`
5. See [references/config-patterns.md](references/config-patterns.md) for config examples

## Content Style Reference

For detailed examples of each page type and the full VitePress config pattern, see [references/config-patterns.md](references/config-patterns.md).
