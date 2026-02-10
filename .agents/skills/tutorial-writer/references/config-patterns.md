# Config Patterns & Content Examples

## VitePress Config: Adding a New Project

When adding a new project section to `docs/.vitepress/config.ts`:

### Nav Entry

Add to `themeConfig.nav` array:

```ts
{ text: '项目显示名', link: '/project-slug/first-page' }
```

### Sidebar Section

Add new key to `themeConfig.sidebar`:

```ts
'/project-slug/': [
  {
    text: '项目N：项目显示名',
    items: [
      { text: '页面标题', link: '/project-slug/page-slug' },
      // ... more pages ...
      { text: '常见问题', link: '/project-slug/faq' },
    ]
  }
],
```

The FAQ page is always the last item.

## Normal Tutorial Page Example

Canonical structure based on existing pages:

```markdown
# 页面标题

## 本节目标

一句话描述。例如："从零开始，让 AI 帮你创建一个番茄时钟的网页应用，并在浏览器中看到它运行。"

## 第一个步骤标题

描述性文字。

在聊天面板中输入：

> 完整的中文 prompt 示例

![截图alt描述](./images/section-01-description.png)

## AI 做了什么

描述 AI 的行为（不粘贴实际输出）。

![截图alt描述](./images/section-02-description.png)

## 查看结果

引导学员查看效果。

![截图alt描述](./images/section-03-description.png)

::: tip 如果遇到问题
告诉 AI：

> 描述问题的 prompt 示例
:::

## 提示词对比

（可选 — 只在有教学意义时添加）

**试试这样说**：
> 模糊的 prompt

AI 可能会问你：...
你可以回复：

> 跟进的 prompt

**要点**：一句话总结对比的核心启示。

## 下一步

一句话过渡到下一节。例如："现在页面上的 25:00 还是静止的。下一节我们让它动起来——实现真正的倒计时。"
```

## FAQ Page Example

```markdown
# 常见问题

## 分类标题（如：项目创建相关）

### 具体问题描述

解释（如适用）+ 解决方式。

告诉 AI：

> 解决问题的 prompt 示例

### 另一个问题

（同样模式）
```

## Concept Page Example (intro-mcp, what-is-vibe-coding style)

```markdown
# 概念标题

## 本节目标

一句话。

## 什么是 [概念]

用类比解释，不用术语。
格式："**打个比方**：..."

## 实际体验：[动手环节名称]

引导学员动手操作，用标准的 prompt → 截图流程。

## [概念]的价值

对比"之前"和"现在"，让学员感受差异。

## 常见问题

### 问题1

告诉 AI：
> prompt

## 下一步

过渡到下一节。
```
