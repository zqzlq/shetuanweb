DEFAULT_GITHUB_URL = 'https://github.com/GUET1-304A'

DEFAULT_SITE_CONFIG = {
    'about': {
        'description': '我们相信真正有生命力的社团，不只是活动的集合，而是由一群愿意一起学习、一起做事、一起把成果分享出去的人组成。',
        'items': [
            {
                'description': '星雨作坊围绕产品构思、视觉设计、前后端开发与内容传播开展协作，鼓励成员从真实需求出发，完成从调研、原型、实现到发布的完整项目链路。',
                'title': '我们在做什么'
            },
            {
                'description': '适合热爱互联网、愿意表达、乐于合作，也愿意花时间打磨作品的人。无论你更偏创意、设计、技术还是运营，都能在这里找到一起成长的伙伴。',
                'title': '我们适合谁'
            },
            {
                'description': '做出被同学真实使用的产品，沉淀可复用的协作经验，并通过开源文档、代码仓库和项目复盘，把经验继续传递给下一届成员。',
                'title': '我们的目标'
            }
        ],
        'title': '社团简介'
    },
    'footer': {
        'brand': '星雨作坊 Xingyu Studio',
        'logo': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/5ab0547bffef4a0986baac8e245c4401.png',
        'slogan': '以协作连接灵感，以开源延续成长。'
    },
    'hero': {
        'description': '星雨作坊是一个面向产品、设计与技术协作的校园创意社团。我们围绕真实项目进行学习、共创和开源，把想法一步步做成可被看见、可被使用、可持续迭代的作品。',
        'eyebrow': 'XINGYU STUDIO',
        'signalCard': {
            'description': '产品策划 / 设计实现 / 持续开源',
            'eyebrow': '协作 · 创造 · 分享',
            'title': '从 0 到 1'
        },
        'stats': [
            {'label': '核心方向', 'value': '4'},
            {'label': '协作项目', 'value': '10+'},
            {'label': '鼓励开源', 'value': '100%'},
            {'label': '参与开源社区', 'value': '5+'},
            {'label': '合作社区', 'value': '1+'},
            {'label': '参与比赛', 'value': '2+'}
        ],
        'title': '把灵感变成作品，把热爱做成长期主义。'
    },
    'members': {
        'description': '我们鼓励跨方向协作，每个人都能在自己的主线能力之外，接触更完整的产品流程。',
        'groups': [
            {
                'description': '负责需求洞察、功能设计、项目推进与版本规划，把零散想法整理成可执行的产品方案。',
                'name': '流光组',
                'tag': '产品策划'
            },
            {
                'description': '负责品牌视觉、界面设计与交互体验，让产品不仅可用，也更有辨识度和表达力。',
                'name': '星绘组',
                'tag': '视觉设计'
            },
            {
                'description': '负责前端、后端与部署实现，把设计和需求转化为真正可运行、可交付、可维护的系统。',
                'name': '逐云组',
                'tag': '技术开发'
            },
            {
                'description': '负责活动记录、产品推广、社媒运营与社区维护，让作品被更多人看到，也让成员经验持续沉淀。',
                'name': '回声组',
                'tag': '内容传播'
            }
        ],
        'title': '人员介绍'
    },
    'openSource': {
        'description': '对星雨作坊来说，开源不只是把代码放出来，更是把过程、思考和经验主动分享出去。',
        'items': [
            {
                'description': '把文档、教程、设计稿和项目复盘留下来，让后来者可以站在前人的经验上继续前进。',
                'title': '共享知识'
            },
            {
                'description': '欢迎成员互相 review、共同维护项目，也欢迎外部同学提出 issue、建议和改进方案。',
                'title': '鼓励协作'
            },
            {
                'description': '开源意味着作品不是一次性交付，而是会随着需求、反馈与技术演进不断完善。',
                'title': '持续迭代'
            }
        ],
        'joinBanner': {
            'eyebrow': 'JOIN US',
            'primaryButton': {
                'link': '/join',
                'text': '加入我们'
            },
            'secondaryButton': {
                'link': '/recruitment',
                'text': '招新信息'
            },
            'title': '如果你也相信"做作品比只谈想法更重要"，欢迎加入星雨作坊。'
        },
        'title': '开源精神'
    },
    'products': {
        'categories': [
            '精选总览',
            '网站平台',
            '效率工具',
            '品牌内容'
        ],
        'description': '以下内容为社团真实项目名称、截图、简介与仓库链接。',
        'slides': [
            {
                'description': '星雨作坊的产品并不是孤立存在的单点项目，而是围绕真实需求持续迭代的作品群。我们希望每一项作品都能成为下一项作品的起点。',
                'metrics': [
                    {'label': '核心章节', 'value': '03'},
                    {'label': '示例作品', 'value': '06'},
                    {'label': '持续迭代', 'value': '∞'}
                ],
                'projects': [
                    {
                        'category': '网站平台',
                        'coverClass': 'aurora',
                        'description': '为新成员与访客整理社团资讯、活动日历与学习路线的门户网站。',
                        'featured': True,
                        'link': '/onboarding',
                        'name': '星图导航',
                        'slug': 'star-chart',
                        'techStack': ['Vue 3', 'Tailwind CSS', 'Flask']
                    },
                    {
                        'category': '效率工具',
                        'coverClass': 'meteor',
                        'description': '支持任务拆分、进度同步与复盘记录的轻量化协作工具。',
                        'featured': True,
                        'link': '/yuji',
                        'name': '雨记协作板',
                        'slug': 'rain-note',
                        'techStack': ['Vue 3', 'Rust', 'WebSocket']
                    },
                    {
                        'category': '品牌内容',
                        'coverClass': 'nebula',
                        'description': '沉淀年度作品、社团故事和成员成长轨迹的数字刊物与视觉专题。',
                        'link': '/timeline',
                        'name': '星雨年刊',
                        'slug': 'xingyu-annual',
                        'techStack': ['设计', '内容策划']
                    }
                ],
                'tag': '精选总览',
                'title': '从灵感、工具到传播，形成完整作品链路'
            },
            {
                'description': '这一类项目强调信息组织、交互体验与系统稳定性，通常会面向成员、访客或校园用户提供长期使用的服务入口。',
                'metrics': [],
                'projects': [
                    {
                        'category': '网站平台',
                        'coverClass': 'aurora',
                        'description': '为新成员与访客整理社团资讯、活动日历与学习路线的门户网站。',
                        'featured': True,
                        'link': '/onboarding',
                        'name': '星图导航',
                        'slug': 'star-chart',
                        'techStack': ['Vue 3', 'Tailwind CSS', 'Flask']
                    },
                    {
                        'category': '网站平台',
                        'coverClass': 'cosmos',
                        'description': '用于活动预告、报名管理和数据统计，帮助组织流程更顺畅。',
                        'link': '',
                        'name': '活动报名系统',
                        'slug': 'event-system',
                        'techStack': ['Vue 3', 'Flask']
                    }
                ],
                'tag': '网站平台',
                'title': '把服务入口和活动体验做成可持续迭代的平台'
            },
            {
                'description': '这类作品更关注成员内部的协同、记录与复盘，希望通过轻量工具减少沟通成本，让创作和执行更流畅。',
                'metrics': [],
                'projects': [
                    {
                        'category': '效率工具',
                        'coverClass': 'meteor',
                        'description': '支持任务拆分、进度同步与复盘记录的轻量化协作工具。',
                        'featured': True,
                        'link': '/yuji',
                        'name': '雨记协作板',
                        'slug': 'rain-note',
                        'techStack': ['Vue 3', 'Rust', 'WebSocket']
                    },
                    {
                        'category': '效率工具',
                        'coverClass': 'pulse',
                        'description': '面向社团成员的灵感归档空间，方便记录选题、链接和碎片创意。',
                        'link': '',
                        'name': '灵感收集箱',
                        'slug': 'idea-box',
                        'techStack': ['Vue 3']
                    }
                ],
                'tag': '效率工具',
                'title': '把协作过程也设计成产品，让创作效率持续提升'
            },
            {
                'description': '这一部分更关注视觉表达、内容包装和公开传播，让社团成果能够以更完整、更动人的方式被外界感知。',
                'metrics': [],
                'projects': [
                    {
                        'category': '品牌内容',
                        'coverClass': 'nebula',
                        'description': '沉淀年度作品、社团故事和成员成长轨迹的数字刊物与视觉专题。',
                        'link': '/timeline',
                        'name': '星雨年刊',
                        'slug': 'xingyu-annual',
                        'techStack': ['设计', '内容策划']
                    },
                    {
                        'category': '品牌内容',
                        'coverClass': 'horizon',
                        'description': '将讲座回顾、教程文章和项目经验整理成公开可访问的内容合集。',
                        'link': '/blog',
                        'name': '开放分享计划',
                        'slug': 'open-sharing',
                        'techStack': ['内容', '社媒']
                    }
                ],
                'tag': '品牌内容',
                'title': '让作品被看见，也让社团的成长被长久保存'
            }
        ],
        'title': '产品展示'
    },
    'sections': {
        'hero': True,
        'about': True,
        'members': True,
        'products': True,
        'awards': True,
        'openSource': True
    },
    'system': {
        'feishuAppChatId': '',
        'feishuAppId': '',
        'feishuAppSecret': '',
        'feishuAppVerificationToken': '',
        'feishuAppEncryptKey': '',
        'feishuMode': 'webhook',
        'feishuWebhookUrl': '',
        'siteIcon': '',
        'mailEnabled': False,
        'smtpHost': '',
        'smtpPort': 465,
        'smtpUsername': '',
        'smtpPassword': '',
        'mailFromEmail': '',
        'mailFromName': '星雨作坊',
        'smtpUseSsl': True,
        'smtpUseTls': False,
        'groupChatInviteLink': '',
    }
}

DEFAULT_PAGES = {
    'about': {
        'content': {
            'cta': {
                'description': '我们始终在寻找具有远见卓识的头脑，以帮助我们绘制数字领域的下一个前沿。',
                'primaryButton': {
                    'link': '/recruitment',
                    'text': '查看开放职位'
                },
                'secondaryButton': {
                    'link': '/join',
                    'text': '咨询作坊'
                },
                'title': '渴望加入这片星群？'
            },
            'groups': {
                'items': [
                    {
                        'description': '掌控光影与运动的物理法则，打造触动感官的沉浸式数字品牌体验。',
                        'name': '流光',
                        'tag': '视觉与动效'
                    },
                    {
                        'description': '架构的脊梁。构建可扩展、低延迟的系统，驱动高性能的 Web 与移动应用。',
                        'name': '星辉',
                        'tag': '核心工程'
                    },
                    {
                        'description': '优化数字平流层。托管基础设施，自动化部署，以及坚不可摧的安全协议。',
                        'name': '筑云',
                        'tag': '云端与运维'
                    },
                    {
                        'description': '用户之声。将深度的心理学研究转化为直观的流程与共鸣驱动的交互模型。',
                        'name': '回声',
                        'tag': '体验与研究'
                    }
                ],
                'subtitle': '环绕同一颗创意太阳运转的专业智慧节点。',
                'title': '四大星系'
            },
            'hero': {
                'badges': [
                    {'icon': 'stars', 'text': '始于 2018'},
                    {'icon': 'hub', 'text': '四大核心矩阵'}
                ],
                'eyebrow': '星辰传承',
                'subtitle': '一个重塑代码与设计边界的精英数字共同体',
                'title': '星雨作坊'
            },
            'timeline': {
                'eyebrow': '演进',
                'items': [
                    {
                        'description': '起初，这只是由一个帅气的老师和一群志趣相投的学生组成的公会。使命很简单：创造兼具美感与坚不可摧的事物。',
                        'title': '奇点降临',
                        'year': '2024'
                    },
                    {
                        'description': '采用学生自荐的方法继续扩张。这个时代见证了我们四大核心智慧星系的诞生。',
                        'title': '全球扩张',
                        'year': '2025'
                    },
                    {
                        'description': '转向融合 AI 的生态系统与高度个性化的数字环境。当我们探索可能性的边缘时，这段旅程仍在继续。',
                        'title': '深入云海',
                        'year': '2026'
                    }
                ],
                'title': '我们的星际航行'
            },
            'values': {
                'items': [
                    {
                        'description': '像素级的精准。代码级的稳健。我们将每一款产品视为数字宇宙中永恒的艺术品。',
                        'icon': 'diamond',
                        'image': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/ac946e8302ad4dd2b454f01122425783.png',
                        'title': '匠心独运'
                    },
                    {
                        'description': '知识属于共同体。我们回馈那些支撑我们创新的代码库，孕育透明开放的文化。',
                        'icon': 'public',
                        'image': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/8e16c7d80d124d88820fcdeb94a93d32.png',
                        'title': '开源精神'
                    },
                    {
                        'description': '打破工程与艺术的壁垒。我们如同一个统一的神经系统般运转，让个体的光芒放大集体的力量。',
                        'icon': 'group_work',
                        'image': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/25beb52172114113aaf865f3a57c3fd3.png',
                        'title': '极致协作'
                    }
                ],
                'subtitle': '源于对极致的渴望，以及对科技生态共同成长的坚定承诺。',
                'title': '我们的星辰法则'
            }
        },
        'title': '关于我们'
    },
    'blog': {
        'content': {
            'categories': [
                '全部',
                '技术',
                '设计',
                '开源',
                '活动'
            ],
            'hero': {
                'eyebrow': '数字纪事',
                'subtitle': '分享我们的技术探索、设计思考和社团故事。',
                'title': '博客与动态'
            },
            'posts': [
                {
                    'category': '技术',
                    'date': '2024-12-15',
                    'excerpt': '回顾我们这一年采用的技术选型和实践经验',
                    'link': '',
                    'readTime': '8 分钟',
                    'title': '2024 年度技术栈回顾'
                },
                {
                    'category': '设计',
                    'date': '2024-11-20',
                    'excerpt': '分享我们如何为社团项目建立统一的设计语言',
                    'link': '',
                    'readTime': '12 分钟',
                    'title': '从零搭建设计系统'
                },
                {
                    'category': '开源',
                    'date': '2024-10-08',
                    'excerpt': '我们在开源项目中总结的协作流程与规范',
                    'link': '',
                    'readTime': '6 分钟',
                    'title': '开源协作的最佳实践'
                }
            ]
        },
        'title': '开源动态'
    },
    'join': {
        'content': {
            'applyCta': {
                'buttonText': '提交申请',
                'description': '填写申请表，开启你的星雨之旅',
                'link': '#',
                'title': '准备好了吗？'
            },
            'benefits': [
                {
                    'description': '参与从 0 到 1 的完整产品开发流程',
                    'title': '真实项目经验'
                },
                {
                    'description': '接触产品、设计、技术、运营各个方向',
                    'title': '跨领域学习'
                },
                {
                    'description': '为开源社区贡献代码，积累 GitHub 履历',
                    'title': '开源贡献'
                }
            ],
            'faq': [
                {
                    'answer': '我们欢迎所有热爱创造的同学，没有硬性技能要求。只要你愿意学习、乐于协作，就能在这里找到成长的空间。',
                    'question': '需要什么基础才能加入？'
                },
                {
                    'answer': '根据项目阶段不同，一般每周 4-8 小时。我们尊重每个人的学业和生活节奏。',
                    'question': '每周需要投入多少时间？'
                },
                {
                    'answer': '可以根据自己的兴趣和特长选择主要方向，同时也鼓励跨组协作和学习。',
                    'question': '如何选择加入哪个小组？'
                }
            ],
            'form': {
                'defaultGithubUrl': '',
                'groups': [
                    {'id': 'liuguang', 'name': '流光组', 'tag': '产品策划'},
                    {'id': 'xinghui', 'name': '星绘组', 'tag': '视觉设计'},
                    {'id': 'zhuyun', 'name': '逐云组', 'tag': '技术开发'},
                    {'id': 'huisheng', 'name': '回声组', 'tag': '内容传播'}
                ],
                'steps': [
                    '基本信息',
                    '选择方向',
                    '完成提交'
                ]
            },
            'hero': {
                'subtitle': '与志同道合的伙伴一起，把想法变成现实。',
                'title': '加入星雨作坊'
            },
            'sections': {
                'faqTitle': '常见问题',
                'groupsTitle': '选择你的方向'
            }
        },
        'title': '加入我们'
    },
    'members': {
        'content': {
            'hero': {
                'eyebrow': '核心星群',
                'subtitle': '每一颗星都有独特的光芒，共同组成星雨的银河。',
                'title': '认识我们的团队'
            },
            'joinCta': {
                'description': '我们欢迎志同道合的伙伴加入星雨作坊',
                'primaryButton': {
                    'link': '/join',
                    'text': '加入我们'
                },
                'secondaryButton': {
                    'link': '/recruitment',
                    'text': '查看招新'
                },
                'title': '想成为我们的一员？'
            },
            'members': [
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/b1ea77c6543a47769ee76f228a1f52a4.jpg',
                    'description': '专注于产品战略与用户体验设计，擅长将复杂需求转化为清晰的产品方案',
                    'group': '流光组',
                    'links': {'github': DEFAULT_GITHUB_URL, 'portfolio': ''},
                    'name': '陶星宇',
                    'projects': [],
                    'role': '指导老师',
                    'skills': ['产品设计', '用户研究', '项目管理']
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/37f42d36f6c342dc8cee28929fcf69e4.jpg',
                    'description': '全栈工程师，热衷于开源项目，主导多个核心系统的架构设计',
                    'group': '逐云组',
                    'links': {'github': DEFAULT_GITHUB_URL, 'portfolio': ''},
                    'name': '穆天宇',
                    'projects': [],
                    'role': '技术负责人',
                    'skills': ['Vue', 'Python', 'Rust', 'DevOps']
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/15769f6271cf40bc99fe0ed8d241cde2.jpg',
                    'description': 'UI/UX 设计师，追求像素完美，负责社团整体视觉语言',
                    'group': '星绘组',
                    'links': {'github': DEFAULT_GITHUB_URL, 'portfolio': ''},
                    'name': '梁天音',
                    'projects': [],
                    'role': '设计负责人',
                    'skills': ['UI设计', '品牌设计', '动效设计']
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/d8bdadf92b734d408f263d28e2ec1e71.jpg',
                    'description': '全栈工程师，热衷于开源项目，主导多个核心系统的架构设计',
                    'group': '',
                    'links': {'github': 'https://github.com/zqzlq', 'portfolio': ''},
                    'name': '曾麒兆',
                    'projects': [],
                    'role': '技术人员',
                    'skills': ['Vue', 'Python，java']
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/6fcbad9787534795a51b77b9b9d41652.jpg',
                    'description': 'UI/UX 设计师，追求像素完美，负责社团整体视觉语言',
                    'group': '',
                    'links': {'github': '', 'portfolio': ''},
                    'name': '兀泉晶',
                    'projects': [],
                    'role': '技术人员',
                    'skills': []
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/03b91cdef85047e4899889d2e8b5933d.jpg',
                    'description': '擅长前端开发',
                    'group': '',
                    'links': {'github': '', 'portfolio': ''},
                    'name': '温慧珍',
                    'projects': [],
                    'role': '技术人员',
                    'skills': ['Vue']
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/19dab2798001478b9c22271bc9239d6d.jpg',
                    'description': '喜欢安卓开发',
                    'group': '',
                    'links': {'github': '', 'portfolio': ''},
                    'name': '丁林云',
                    'projects': [],
                    'role': '技术人员',
                    'skills': []
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/5e715eb2010746f7bdfed6c575a5ebc5.jpg',
                    'description': '热衷于后端开发',
                    'group': '',
                    'links': {'github': '', 'portfolio': ''},
                    'name': '张自强',
                    'projects': [],
                    'role': '技术人员',
                    'skills': ['java，go']
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/eecfbdf0f2a848c78805f1470ce7fc80.jpg',
                    'description': '擅长安卓开发',
                    'group': '',
                    'links': {'github': '', 'portfolio': ''},
                    'name': '郑承睿',
                    'projects': [],
                    'role': '技术人员',
                    'skills': []
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/b14bd369469b4cd5a86547702ee82415.jpg',
                    'description': '',
                    'group': '',
                    'links': {'github': '', 'portfolio': ''},
                    'name': '莫玉妃',
                    'projects': [],
                    'role': '技术人员',
                    'skills': []
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/26d6c11cd5ee4579b1a71b0e7d25f1d1.jpg',
                    'description': '',
                    'group': '',
                    'links': {'github': '', 'portfolio': ''},
                    'name': '赵欣苗',
                    'projects': [],
                    'role': '技术人员',
                    'skills': []
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/50771bec14b04ac38bf00405b63c426c.jpg',
                    'description': '',
                    'group': '',
                    'links': {'github': '', 'portfolio': ''},
                    'name': '江昊宸',
                    'projects': [],
                    'role': '技术人员',
                    'skills': []
                }
            ],
            'stats': [
                {'label': '核心成员', 'value': '11+'},
                {'label': '活跃贡献者', 'value': '11+'},
                {'label': '代码行数', 'value': '156k'}
            ]
        },
        'title': '成员介绍'
    },
    'onboarding': {
        'content': {
            'faq': [
                {
                    'answer': '一般 2-4 周，根据项目情况灵活调整。',
                    'question': '试用期多长时间？'
                },
                {
                    'answer': '入职后会收到环境配置指南，导师会协助你完成设置。',
                    'question': '如何获取开发环境？'
                },
                {
                    'answer': '可以在 Discord 提问，或直接联系你的导师。',
                    'question': '遇到问题找谁？'
                }
            ],
            'hero': {
                'eyebrow': '入职指南',
                'subtitle': '这份指南将帮助你快速融入团队，开始你的星际之旅。',
                'title': '欢迎加入星雨'
            },
            'mentors': [
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/8f0d23d5bc8b4b89a489e302f708b091.jpg',
                    'description': '帮助你理解产品思维',
                    'name': '导师 A',
                    'role': '产品方向'
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/93c99f4e41d94fc081b3242b6726daa0.jpg',
                    'description': '指导技术成长路径',
                    'name': '导师 B',
                    'role': '技术方向'
                },
                {
                    'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/6bbe90798c344b9d8518be7958f36cf8.jpg',
                    'description': '提升设计审美与技能',
                    'name': '导师 C',
                    'role': '设计方向'
                }
            ],
            'resources': [
                {
                    'description': '项目文档、规范指南、学习资料',
                    'icon': 'book',
                    'title': '内部维基'
                },
                {
                    'description': '品牌素材、UI 组件、设计模板',
                    'icon': 'palette',
                    'title': '设计资产'
                },
                {
                    'description': '技术栈入门、最佳实践、代码规范',
                    'icon': 'code',
                    'title': '代码教程'
                },
                {
                    'description': '日常交流、问题讨论、活动通知',
                    'icon': 'chat',
                    'title': 'Discord 社区'
                }
            ],
            'sections': {
                'faqTitle': '常见问题',
                'mentorsTitle': '你的导师',
                'resourcesTitle': '资源中心',
                'stepsTitle': '入职流程'
            },
            'steps': [
                {
                    'description': '填写申请表，介绍自己',
                    'title': '提交申请'
                },
                {
                    'description': '轻松聊天，互相了解',
                    'title': '面试交流'
                },
                {
                    'description': '参与小项目，感受氛围',
                    'title': '试用期'
                },
                {
                    'description': '欢迎加入星雨大家庭',
                    'title': '正式成员'
                }
            ]
        },
        'title': '新手指南'
    },
    'open-source': {
        'content': {
            'community': {
                'description': '欢迎贡献代码、提交 Issue 或参与讨论',
                'discord': 'https://discord.gg/xingyu',
                'discordText': 'Discord',
                'github': DEFAULT_GITHUB_URL,
                'githubText': 'GitHub',
                'title': '加入我们的开源社区'
            },
            'contributors': [
                {
                    'avatar': '',
                    'commits': 100,
                    'name': '穆天宇'
                }
            ],
            'hero': {
                'eyebrow': '开源生态系统',
                'subtitle': '代码是我们的语言，开源是我们的信仰。',
                'title': '我们的开源世界'
            },
            'repos': [
                {
                    'description': '星雨作坊的设计系统与 UI 组件库',
                    'language': 'TypeScript',
                    'link': DEFAULT_GITHUB_URL,
                    'name': 'Star-Chart UI',
                    'stars': 128
                },
                {
                    'description': '雨记协作板的核心引擎',
                    'language': 'Rust',
                    'link': DEFAULT_GITHUB_URL,
                    'name': 'Rain-Note Core',
                    'stars': 89
                },
                {
                    'description': '项目脚手架与开发工具集',
                    'language': 'Go',
                    'link': DEFAULT_GITHUB_URL,
                    'name': 'Celestial CLI',
                    'stars': 56
                }
            ],
            'sections': {
                'contributorsTitle': '核心贡献者',
                'reposTitle': '开源仓库',
                'techStackTitle': '技术栈'
            },
            'techStack': [
                'Vue',
                'React',
                'TypeScript',
                'Python',
                'Rust',
                'PostgreSQL',
                'Docker'
            ]
        },
        'title': '开源精神'
    },
    'projects': {
        'content': {
            'cta': {
                'description': '我们欢迎各种形式的贡献，从代码到设计，从文档到创意。',
                'primaryButton': {
                    'link': '/open-source',
                    'text': '查看贡献指南'
                },
                'secondaryButton': {
                    'link': '/join',
                    'text': '加入社团'
                },
                'title': '想要参与我们的项目？'
            },
            'filters': [
                '全部',
                '精选',
                '网站平台',
                '效率工具',
                '品牌内容',
                '比赛奖项'
            ],
            'hero': {
                'eyebrow': '策展阶段 04',
                'subtitle': '探索我们精心打造的数字作品集，每一件都承载着创新与匠心。',
                'title': '产品画廊'
            },
            'projects': [
                {
                    'category': '精选',
                    'contributors': [
                        {
                            'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/15769f6271cf40bc99fe0ed8d241cde2.jpg',
                            'name': '梁天音',
                            'role': '主要负责人'
                        }
                    ],
                    'coverClass': 'aurora',
                    'coverImage': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/d58a28af24684340a70a153cb1dfa131.png',
                    'demoUrl': 'xinliang0917/tourism-wechat-miniprogram_guizhoulvwenhui',
                    'description': '一款与桂林文旅有关的小程序',
                    'featured': True,
                    'githubUrl': '',
                    'link': '',
                    'longDescription': '基于微信小程序的桂林旅游服务平台，提供旅游产品与文创周边商品浏览购买、AI智能客服导览、文物扫描视频介绍、订单管理及多语言切换（中文/英文/泰语/越南语）等功能。',
                    'name': '桂林文旅小程序',
                    'screenshots': [
                        'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/4d21c71a77664f2d891345c3623f6e10.png'
                    ],
                    'slug': '桂林文旅小程序',
                    'startDate': '',
                    'status': 'active',
                    'tags': [],
                    'techStack': []
                },
                {
                    'category': '精选',
                    'contributors': [
                        {
                            'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/15769f6271cf40bc99fe0ed8d241cde2.jpg',
                            'name': '梁天音',
                            'role': '主要负责人'
                        }
                    ],
                    'coverClass': 'aurora',
                    'coverImage': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/ff3bacce49574d7d8033214f8207e5a2.png',
                    'demoUrl': 'https://www.bilibili.com/video/BV1r2YbzJE9E/',
                    'description': '当空-气象爱好者社区',
                    'featured': True,
                    'githubUrl': '',
                    'link': '',
                    'longDescription': '"当空"是一个基于气象美学的AI赋能社区，核心功能是利用AI Agent精准预测晚霞等气象景观出现的概率，并结合实时天气数据与地理位置，为用户提供最佳拍摄时间、地点及构图建议。',
                    'name': '当空-气象爱好者社区',
                    'screenshots': [],
                    'slug': '当空-气象爱好者社区',
                    'startDate': '',
                    'status': 'active',
                    'tags': [],
                    'techStack': []
                },
                {
                    'category': '效率工具',
                    'contributors': [
                        {
                            'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/15769f6271cf40bc99fe0ed8d241cde2.jpg',
                            'name': '梁天音',
                            'role': '技术负责任人'
                        }
                    ],
                    'coverClass': 'aurora',
                    'coverImage': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/333407d63f554aa586718bdd337b235c.jpg',
                    'demoUrl': 'xinliang0917/ai-interview-wechat-miniprogram',
                    'description': '星讯智面——ai面试微信小程序',
                    'featured': True,
                    'githubUrl': '',
                    'link': '',
                    'longDescription': '通过AI技术模拟面试场景并进行智能评估，系统根据用户面试的岗位生成相应面试题，用户上传回答文件，面试完成后调用Coze接口进行分析评估，最终生成面试报告展示评估结果',
                    'name': '星讯智面——ai面试微信小程序',
                    'screenshots': [
                        'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/51d9264e016540c4b96deb24c265d138.jpg',
                        'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/2bcea1bd0ed74f0d86ef5adabe557956.jpg'
                    ],
                    'slug': '星讯智面ai面试微信小程序',
                    'startDate': '',
                    'status': 'active',
                    'tags': [],
                    'techStack': []
                },
                {
                    'category': '精选',
                    'contributors': [
                        {
                            'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/19dab2798001478b9c22271bc9239d6d.jpg',
                            'name': '丁林云',
                            'role': '开发人员'
                        }
                    ],
                    'coverClass': 'aurora',
                    'coverImage': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/b0c6a758d4aa40859a82ffaae4abf5a8.png',
                    'demoUrl': '',
                    'description': 'AI语音交互机器人',
                    'featured': False,
                    'githubUrl': 'https://github.com/qingfeng19491001/VoiceRobot',
                    'link': '',
                    'longDescription': '基于 Volc Dialog SDK 的Android AI 语音对话APP',
                    'name': 'AI语音交互机器人',
                    'screenshots': [],
                    'slug': 'ai语音交互机器人',
                    'startDate': '',
                    'status': 'active',
                    'tags': [],
                    'techStack': []
                },
                {
                    'category': '效率工具',
                    'contributors': [
                        {
                            'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/37f42d36f6c342dc8cee28929fcf69e4.jpg',
                            'name': '穆天宇',
                            'role': ''
                        },
                        {
                            'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/d8bdadf92b734d408f263d28e2ec1e71.jpg',
                            'name': '曾麒兆',
                            'role': ''
                        }
                    ],
                    'coverClass': 'meteor',
                    'coverImage': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/bfecd03d3cbb4fa8abfe251dfe751887.png',
                    'demoUrl': '',
                    'description': '',
                    'featured': False,
                    'githubUrl': 'https://github.com/MU-ty/AI-Office-Assistant',
                    'link': '',
                    'longDescription': '',
                    'name': 'AI科研&办公助手',
                    'screenshots': [],
                    'slug': 'ai-office',
                    'startDate': '',
                    'status': 'active',
                    'tags': ['python，agent'],
                    'techStack': ['python，agent']
                },
                {
                    'category': '网站平台',
                    'contributors': [
                        {
                            'avatar': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/37f42d36f6c342dc8cee28929fcf69e4.jpg',
                            'name': '穆天宇',
                            'role': ''
                        }
                    ],
                    'coverClass': 'aurora',
                    'coverImage': 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/1d31a7aa06214fc0a26b20d0b92f8c8e.png',
                    'demoUrl': 'https://mu-ty.github.io/Minecraft-Guilin-City-Walk-TRAE/',
                    'description': '',
                    'featured': False,
                    'githubUrl': 'https://github.com/MU-ty/Minecraft-Guilin-City-Walk-TRAE',
                    'link': '',
                    'longDescription': '',
                    'name': '像素桂林',
                    'screenshots': [],
                    'slug': 'x',
                    'startDate': '',
                    'status': 'active',
                    'tags': ['Javascript，CSS，HTML'],
                    'techStack': ['Javascript，CSS，HTML']
                }
            ],
            'awards': {
                'title': '比赛奖项',
                'description': '社团成员在各类比赛中获得的荣誉与成果。',
                'items': [
                    {
                        'slug': 'ccc-2024',
                        'title': '2024 中国大学生计算机设计大赛 省级一等奖',
                        'shortDesc': '作品《星图导航》获得省级一等奖。',
                        'description': '作品《星图导航》在2024年中国大学生计算机设计大赛中获得省级一等奖。该项目以校园信息聚合与导航为核心，采用 Vue 3 + Flask 技术栈，实现了社团资讯、活动日历、学习路线的一站式整合。',
                        'longDescription': '中国大学生计算机设计大赛是由教育部高等学校计算机类专业教学指导委员会等主办的全国性赛事，旨在激发学生学习计算机知识和技能的兴趣与潜能。\n\n星雨作坊参赛作品《星图导航》以校园信息聚合与导航为核心功能，面向新成员与外部访客提供一站式信息服务。项目采用 Vue 3 + Tailwind CSS 构建前端，Flask 提供后端 API，MySQL 存储数据。\n\n作品从需求分析、原型设计到开发部署均由社团成员独立完成，经过校赛选拔后推荐至省级评审，最终获得省级一等奖。',
                        'level': '省级一等奖',
                        'date': '2024-08',
                        'category': '计算机设计',
                        'participants': ['陈星宇', '林悦', '赵鹏程'],
                        'projectSlug': 'star-chart',
                        'image': '',
                        'screenshots': [],
                    },
                    {
                        'slug': 'aic-2024',
                        'title': '2024 全国大学生人工智能创新大赛 优秀奖',
                        'shortDesc': '基于 AI 的智能问答原型获全国优秀奖。',
                        'description': '社团团队以雨记协作板为原型，加入 AI 智能问答模块，在2024年全国大学生人工智能创新大赛中获得优秀奖。',
                        'longDescription': '全国大学生人工智能创新大赛面向全国高校学生，鼓励将人工智能技术应用于实际场景。\n\n星雨作坊团队在雨记协作板的基础上，集成了基于大语言模型的智能问答功能，能够根据项目上下文自动生成任务建议、复盘总结和知识检索结果。\n\n该项目展示了社团在 AI 应用方向的探索能力，虽未进入决赛，但获得了评审专家的肯定与优秀奖。',
                        'level': '全国优秀奖',
                        'date': '2024-10',
                        'category': '人工智能',
                        'participants': ['赵鹏程', '王思远', '陈星宇'],
                        'projectSlug': 'rain-note',
                        'image': '',
                        'screenshots': [],
                    },
                    {
                        'slug': 'design-2024',
                        'title': '2024 校园新媒体设计大赛 最佳视觉奖',
                        'shortDesc': '星雨年刊视觉设计获校级最佳视觉奖。',
                        'description': '社团以《星雨年刊》的设计方案参加校园新媒体设计大赛，凭借统一的视觉语言和精致的排版获得最佳视觉奖。',
                        'longDescription': '校园新媒体设计大赛由校团委主办，面向全校学生征集优秀的新媒体视觉作品。\n\n星雨作坊以年度数字刊物《星雨年刊》参赛，作品涵盖完整的品牌视觉体系：色彩规范、字体搭配、版式设计、插图风格等。评委对刊物的整体一致性、信息层次和视觉美感给予了高度评价。\n\n该奖项是对社团设计能力的认可，也推动了我们在品牌设计方向的持续投入。',
                        'level': '校级最佳视觉奖',
                        'date': '2024-11',
                        'category': '设计',
                        'participants': ['林悦', '张雨桐', '周涵'],
                        'projectSlug': 'xingyu-annual',
                        'image': '',
                        'screenshots': [],
                    },
                ],
            },
            'cta': {
                'title': '想要参与我们的项目？',
                'description': '我们欢迎各种形式的贡献，从代码到设计，从文档到创意。',
                'primaryButton': {'text': '查看贡献指南', 'link': '/open-source'},
                'secondaryButton': {'text': '加入社团', 'link': '/join'},
            },
        },
        'title': '项目展示'
    },
    'recruitment': {
        'content': {
            'cta': {
                'buttonLink': '/join',
                'buttonText': '立即投递申请',
                'title': '准备好加入了吗？'
            },
            'groups': [
                {
                    'description': '如果你善于洞察需求、组织思路、推动项目落地，这里是你的舞台。',
                    'name': '流光组',
                    'requirements': [
                        '对互联网产品有热情',
                        '良好的逻辑思维',
                        '沟通协调能力'
                    ],
                    'tag': '产品策划'
                },
                {
                    'description': '如果你追求像素完美、热爱视觉表达，来和我们一起创造美。',
                    'name': '星绘组',
                    'requirements': [
                        '熟悉设计工具',
                        '有审美追求',
                        '愿意接受反馈'
                    ],
                    'tag': '视觉设计'
                },
                {
                    'description': '如果你热爱代码、追求技术精进，这里有真实的项目等你挑战。',
                    'name': '逐云组',
                    'requirements': [
                        '编程基础',
                        '学习能力强',
                        '喜欢解决问题'
                    ],
                    'tag': '技术开发'
                },
                {
                    'description': '如果你擅长表达、热爱分享，帮助我们让作品被更多人看见。',
                    'name': '回声组',
                    'requirements': [
                        '文字功底',
                        '社媒运营兴趣',
                        '创意思维'
                    ],
                    'tag': '内容传播'
                }
            ],
            'hero': {
                'eyebrow': '2026 年度招募',
                'subtitle': '寻找下一代数字创作者，共同书写星雨的未来篇章。',
                'title': '新星招募计划'
            },
            'process': [
                {
                    'description': '填写申请表，告诉我们你的故事',
                    'step': '投递申请'
                },
                {
                    'description': '我们会认真阅读每份申请',
                    'step': '初步筛选'
                },
                {
                    'description': '轻松的聊天，互相了解',
                    'step': '面试交流'
                },
                {
                    'description': '参与一个小项目，感受氛围',
                    'step': '试用期'
                }
            ],
            'sectionTitles': {
                'process': '招募流程'
            }
        },
        'title': '招新信息'
    },
    'timeline': {
        'content': {
            'hero': {
                'eyebrow': '星雨纪事',
                'subtitle': '记录我们的每一次探索与成长。',
                'title': '星际时间线'
            },
            'milestones': [
                {
                    'description': '全新的官网与管理系统上线',
                    'title': '星雨 3.0 发布',
                    'year': '2026'
                },
                {
                    'description': '首批开源项目发布到 GitHub',
                    'title': '开源计划启动',
                    'year': '2025-8'
                },
                {
                    'description': '组织架构正式确立',
                    'title': '四大星系成立',
                    'year': '2025'
                },
                {
                    'description': '几位志同道合的同学开始了这段旅程',
                    'title': '星雨创立',
                    'year': '2024'
                }
            ],
            'sections': {
                'milestonesTitle': '里程碑',
                'upcomingTitle': '即将到来'
            },
            'upcoming': [
                {
                    'date': '2024-12-20',
                    'description': '分享 2024 年度技术实践经验',
                    'title': '技术分享会',
                    'type': '讲座'
                },
                {
                    'date': '2024-12-25',
                    'description': '设计系统构建实战',
                    'title': '设计工作坊',
                    'type': '工作坊'
                }
            ]
        },
        'title': '时间线'
    },
    'yuji': {
        'content': {
            'cta': {
                'buttonText': '查看源码',
                'link': DEFAULT_GITHUB_URL,
                'title': '在 GitHub 上查看'
            },
            'features': [
                {
                    'description': '从社团内部需求出发，解决小团队任务管理和进度同步的痛点。',
                    'title': '设计初衷'
                },
                {
                    'description': '前端 Vue 3 + 后端 Rust，追求性能与开发体验的平衡。',
                    'tags': ['Vue 3', 'Rust', 'WebSocket'],
                    'title': '技术架构'
                },
                {
                    'description': '采用 MIT 协议开源，欢迎社区贡献和二次开发。',
                    'title': '开源协议'
                }
            ],
            'hero': {
                'metrics': [
                    {'label': 'Star', 'value': '1.2k'},
                    {'label': '贡献者', 'value': '48'},
                    {'label': '分支', 'value': '12'}
                ],
                'subtitle': '为小型团队设计的轻量级协作工具',
                'title': '雨记协作板',
                'version': 'v2.1.0'
            },
            'highlights': [
                '实时协作，多人同时编辑',
                '任务拆分与进度追踪',
                '复盘记录与知识沉淀',
                '轻量部署，开箱即用'
            ],
            'sectionTitles': {
                'features': '功能特性',
                'highlights': '核心亮点'
            }
        },
        'title': '雨记协作板'
    }
}
