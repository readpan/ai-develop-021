import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'AI 开发 0 到 1',
  description: '零基础学 Vibe Coding，用 Cursor 和 AI 做出你的第一个应用',
  lang: 'zh-CN',

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '环境准备', link: '/guide/what-is-vibe-coding' },
      { text: '番茄时钟', link: '/pomodoro/create-project' },
      { text: '贪吃蛇', link: '/snake/setup-environment' },
    ],

    sidebar: {
      '/guide/': [
        {
          text: '环境准备',
          items: [
            { text: '什么是 Vibe Coding', link: '/guide/what-is-vibe-coding' },
            { text: '安装 Cursor 编辑器', link: '/guide/install-cursor' },
            { text: '第一次和 AI 对话', link: '/guide/first-chat' },
          ]
        }
      ],
      '/pomodoro/': [
        {
          text: '项目一：番茄时钟',
          items: [
            { text: '创建项目', link: '/pomodoro/create-project' },
            { text: '实现倒计时', link: '/pomodoro/countdown' },
            { text: '控制按钮', link: '/pomodoro/controls' },
            { text: '工作/休息切换', link: '/pomodoro/work-rest-cycle' },
            { text: '视觉优化', link: '/pomodoro/styling' },
            { text: '提示音与通知', link: '/pomodoro/notification' },
            { text: '常见问题', link: '/pomodoro/faq' },
          ]
        }
      ],
      '/snake/': [
        {
          text: '项目二：贪吃蛇',
          items: [
            { text: '环境升级', link: '/snake/setup-environment' },
            { text: '基础游戏', link: '/snake/basic-game' },
            { text: '游戏完善', link: '/snake/game-polish' },
            { text: '引入 MCP', link: '/snake/intro-mcp' },
            { text: '引入 Agent Skills', link: '/snake/intro-skills' },
            { text: '视觉打磨', link: '/snake/visual-polish' },
            { text: '常见问题', link: '/snake/faq' },
          ]
        }
      ],
    },

    search: {
      provider: 'local'
    },

    outline: {
      level: [2, 3],
      label: '本页目录'
    },

    docFooter: {
      prev: '上一节',
      next: '下一节'
    },

    darkModeSwitchLabel: '主题',
    sidebarMenuLabel: '菜单',
    returnToTopLabel: '回到顶部',
  }
})
