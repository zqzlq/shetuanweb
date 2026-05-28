export const defaultSiteConfig = {
  about: {
    description: '我们相信真正有生命力的社团，不只是活动的集合，而是由一群愿意一起学习、一起做事、一起把成果分享出去的人组成。',
    items: [
      {
        description: '星雨作坊围绕产品构思、视觉设计、前后端开发与内容传播开展协作，鼓励成员从真实需求出发，完成从调研、原型、实现到发布的完整项目链路。',
        title: '我们在做什么'
      },
      {
        description: '适合热爱互联网、愿意表达、乐于合作，也愿意花时间打磨作品的人。无论你更偏创意、设计、技术还是运营，都能在这里找到一起成长的伙伴。',
        title: '我们适合谁'
      },
      {
        description: '做出被同学真实使用的产品，沉淀可复用的协作经验，并通过开源文档、代码仓库和项目复盘，把经验继续传递给下一届成员。',
        title: '我们的目标'
      }
    ],
    title: '社团简介'
  },
  footer: {
    brand: '星雨作坊 Xingyu Studio',
    logo: '',
    slogan: '以协作连接灵感，以开源延续成长。'
  },
  hero: {
    description: '星雨作坊是一个面向产品、设计与技术协作的校园创意社团。我们围绕真实项目进行学习、共创和开源，把想法一步步做成可被看见、可被使用、可持续迭代的作品。',
    eyebrow: 'XINGYU STUDIO',
    signalCard: {
      description: '产品策划 / 设计实现 / 持续开源',
      eyebrow: '协作 · 创造 · 分享',
      title: '从 0 到 1'
    },
    stats: [
      { label: '核心方向', value: '4' },
      { label: '协作项目', value: '10+' },
      { label: '鼓励开源', value: '100%' },
      { label: '参与开源社区', value: '5+' },
      { label: '合作社区', value: '1+' },
      { label: '参与比赛', value: '2+' }
    ],
    title: '把灵感变成作品，把热爱做成长期主义。'
  },
  members: {
    description: '我们鼓励跨方向协作，每个人都能在自己的主线能力之外，接触更完整的产品流程。',
    groups: [
      {
        description: '负责需求洞察、功能设计、项目推进与版本规划，把零散想法整理成可执行的产品方案。',
        name: '流光组',
        tag: '产品策划'
      },
      {
        description: '负责品牌视觉、界面设计与交互体验，让产品不仅可用，也更有辨识度和表达力。',
        name: '星绘组',
        tag: '视觉设计'
      },
      {
        description: '负责前端、后端与部署实现，把设计和需求转化为真正可运行、可交付、可维护的系统。',
        name: '逐云组',
        tag: '技术开发'
      },
      {
        description: '负责活动记录、产品推广、社媒运营与社区维护，让作品被更多人看到，也让成员经验持续沉淀。',
        name: '回声组',
        tag: '内容传播'
      }
    ],
    title: '人员介绍'
  },
  openSource: {
    description: '对星雨作坊来说，开源不只是把代码放出来，更是把过程、思考和经验主动分享出去。',
    items: [
      {
        description: '把文档、教程、设计稿和项目复盘留下来，让后来者可以站在前人的经验上继续前进。',
        title: '共享知识'
      },
      {
        description: '欢迎成员互相 review、共同维护项目，也欢迎外部同学提出 issue、建议和改进方案。',
        title: '鼓励协作'
      },
      {
        description: '开源意味着作品不是一次性交付，而是会随着需求、反馈与技术演进不断完善。',
        title: '持续迭代'
      }
    ],
    joinBanner: {
      eyebrow: 'JOIN US',
      primaryButton: {
        link: '/join',
        text: '加入我们'
      },
      secondaryButton: {
        link: '/recruitment',
        text: '招新信息'
      },
      title: '如果你也相信"做作品比只谈想法更重要"，欢迎加入星雨作坊。'
    },
    title: '开源精神'
  },
  products: {
    categories: [
      '精选总览',
      '网站平台',
      '效率工具',
      '品牌内容'
    ],
    description: '以下内容为社团真实项目名称、截图、简介与仓库链接。',
    slides: [
      {
        description: '星雨作坊的产品并不是孤立存在的单点项目，而是围绕真实需求持续迭代的作品群。我们希望每一项作品都能成为下一项作品的起点。',
        metrics: [
          { label: '核心章节', value: '03' },
          { label: '示例作品', value: '06' },
          { label: '持续迭代', value: '∞' }
        ],
        projects: [
          {
            category: '网站平台',
            coverClass: 'aurora',
            description: '为新成员与访客整理社团资讯、活动日历与学习路线的门户网站。',
            featured: true,
            link: '/onboarding',
            name: '星图导航',
            slug: 'star-chart',
            techStack: ['Vue 3', 'Tailwind CSS', 'Flask']
          },
          {
            category: '效率工具',
            coverClass: 'meteor',
            description: '支持任务拆分、进度同步与复盘记录的轻量化协作工具。',
            featured: true,
            link: '/yuji',
            name: '雨记协作板',
            slug: 'rain-note',
            techStack: ['Vue 3', 'Rust', 'WebSocket']
          },
          {
            category: '品牌内容',
            coverClass: 'nebula',
            description: '沉淀年度作品、社团故事和成员成长轨迹的数字刊物与视觉专题。',
            link: '/timeline',
            name: '星雨年刊',
            slug: 'xingyu-annual',
            techStack: ['设计', '内容策划']
          }
        ],
        tag: '精选总览',
        title: '从灵感、工具到传播，形成完整作品链路'
      },
      {
        description: '这一类项目强调信息组织、交互体验与系统稳定性，通常会面向成员、访客或校园用户提供长期使用的服务入口。',
        metrics: [],
        projects: [
          {
            category: '网站平台',
            coverClass: 'aurora',
            description: '为新成员与访客整理社团资讯、活动日历与学习路线的门户网站。',
            featured: true,
            link: '/onboarding',
            name: '星图导航',
            slug: 'star-chart',
            techStack: ['Vue 3', 'Tailwind CSS', 'Flask']
          },
          {
            category: '网站平台',
            coverClass: 'cosmos',
            description: '用于活动预告、报名管理和数据统计，帮助组织流程更顺畅。',
            link: '',
            name: '活动报名系统',
            slug: 'event-system',
            techStack: ['Vue 3', 'Flask']
          }
        ],
        tag: '网站平台',
        title: '把服务入口和活动体验做成可持续迭代的平台'
      },
      {
        description: '这类作品更关注成员内部的协同、记录与复盘，希望通过轻量工具减少沟通成本，让创作和执行更流畅。',
        metrics: [],
        projects: [
          {
            category: '效率工具',
            coverClass: 'meteor',
            description: '支持任务拆分、进度同步与复盘记录的轻量化协作工具。',
            featured: true,
            link: '/yuji',
            name: '雨记协作板',
            slug: 'rain-note',
            techStack: ['Vue 3', 'Rust', 'WebSocket']
          },
          {
            category: '效率工具',
            coverClass: 'pulse',
            description: '面向社团成员的灵感归档空间，方便记录选题、链接和碎片创意。',
            link: '',
            name: '灵感收集箱',
            slug: 'idea-box',
            techStack: ['Vue 3']
          }
        ],
        tag: '效率工具',
        title: '把协作过程也设计成产品，让创作效率持续提升'
      },
      {
        description: '这一部分更关注视觉表达、内容包装和公开传播，让社团成果能够以更完整、更动人的方式被外界感知。',
        metrics: [],
        projects: [
          {
            category: '品牌内容',
            coverClass: 'nebula',
            description: '沉淀年度作品、社团故事和成员成长轨迹的数字刊物与视觉专题。',
            link: '/timeline',
            name: '星雨年刊',
            slug: 'xingyu-annual',
            techStack: ['设计', '内容策划']
          },
          {
            category: '品牌内容',
            coverClass: 'horizon',
            description: '将讲座回顾、教程文章和项目经验整理成公开可访问的内容合集。',
            link: '/blog',
            name: '开放分享计划',
            slug: 'open-sharing',
            techStack: ['内容', '社媒']
          }
        ],
        tag: '品牌内容',
        title: '让作品被看见，也让社团的成长被长久保存'
      }
    ],
    title: '产品展示'
  },
  sections: {
    hero: true,
    about: true,
    members: true,
    products: true,
    awards: true,
    openSource: true
  }
}
