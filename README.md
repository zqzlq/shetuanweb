# 星雨作坊官网 (Xingyu Studio)

星雨作坊社团官网，一个集内容管理、招新管理、作品展示于一体的校园社团网站系统。

## 技术栈

### 前端
- **框架**: Vue 3 (Composition API + `<script setup>`)
- **构建**: Vite 6
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **UI**: Tailwind CSS 4 + 自定义 CSS 变量
- **动画**: GSAP 3
- **图标**: lucide-vue-next
- **Markdown**: marked

### 后端
- **框架**: Flask (Python 3)
- **ORM**: Flask-SQLAlchemy (SQLite / MySQL)
- **认证**: Flask-JWT-Extended
- **文件存储**: 阿里云 OSS (回退到本地存储)
- **通知**: 飞书 Webhook / SMTP 邮件

### 部署
- **容器化**: Docker + Docker Compose
- **前端服务器**: Nginx (多阶段构建)
- **后端服务器**: Gunicorn

## 功能特性

### 官网展示
- 首页产品轮播展示
- 成员展示（头像、技能、社交链接）
- 项目展示（分类筛选、搜索、分页）
- 比赛奖项展示（详情页、截图轮播）
- 博客动态、开源贡献、时间线等页面

### 管理后台
- **可视化页面编辑**: 所有页面支持可视化编辑 + JSON 编辑
- **首页配置**: Hero、简介、成员、产品轮播、开源精神、页脚
- **分类管理**: 产品分类标签增删改，联动项目展示
- **招新管理**: 申请审核（待处理/审核中/已通过/已拒绝/已归档），批量通过，届数分组
- **用户管理**: 注册用户审核，添加到成员展示
- **提交审核**: 审核用户提交的奖状/作品，同步到官网页面

### 用户系统
- **注册/登录**: 用户名 + 密码 + 姓名 + 邮箱，管理员审核通过后启用
- **个人中心**: 资料编辑、头像上传、社交链接管理、组别选择、密码修改
- **奖状提交**: 支持完整字段（名称、级别、日期、参与者、描述、截图等）
- **作品提交**: 支持完整字段（名称、分类、GitHub、技术栈、描述、截图等）

### 通知系统
- SMTP 邮件通知（审核结果、群聊邀请链接、群二维码）
- 飞书 Webhook 通知

## 快速开始 (Docker)

### 前置要求
- Docker & Docker Compose

### 启动

```bash
# 克隆项目
git clone https://github.com/zqzlq/shetuanweb.git
cd shetuanweb

# 启动所有服务
docker compose up -d --build

# 访问
# 官网: http://localhost
# 管理后台: http://localhost/admin
```

### 默认管理员账号


## 开发环境

### 前端

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 启动
python app.py
```

## 项目结构

```
├── backend/                  # Flask 后端
│   ├── app.py               # 应用工厂、数据库迁移、邮件配置
│   ├── config.py            # 环境配置
│   ├── models.py            # 数据模型
│   ├── defaults.py          # 默认数据
│   ├── application_flow.py  # 通知流程 (飞书/邮件)
│   ├── oss_service.py       # 阿里云 OSS 服务
│   ├── routes/
│   │   └── api.py           # 全部 API 端点
│   └── requirements.txt     # Python 依赖
├── src/                      # Vue 3 前端
│   ├── components/
│   │   ├── admin/            # 管理后台组件
│   │   ├── layout/           # 布局组件 (Navbar, Footer)
│   │   ├── sections/         # 首页区块组件
│   │   ├── user/             # 用户端组件 (登录/注册弹窗)
│   │   └── ui/               # 通用 UI 组件
│   ├── views/                # 页面视图
│   ├── router/               # 路由配置
│   ├── services/             # API 调用
│   ├── stores/               # Pinia 状态管理
│   └── data/                 # 默认数据文件
├── docker-compose.yml        # Docker 编排
├── Dockerfile                # 前端构建镜像
└── nginx.conf                # Nginx 配置
```

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `PORT` | 前端端口映射 | `80` |
| `SECRET_KEY` | Flask 密钥 | `xingyu-studio-secret-2026` |
| `JWT_SECRET_KEY` | JWT 密钥 | `xingyu-jwt-secret-2026` |
| `DATABASE_URL` | 数据库连接 | `sqlite:///data/xingyu_cms.db` |
| `CORS_ORIGINS` | CORS 允许域名 | `http://localhost` |
| `ALIYUN_ACCESS_KEY_ID` | 阿里云 OSS AccessKey |
| `ALIYUN_ACCESS_KEY_SECRET` | 阿里云 OSS AccessSecret |
| `ALIYUN_OSS_ENDPOINT` | OSS Endpoint |
| `ALIYUN_OSS_BUCKET_NAME` | OSS Bucket 名称 |
| `ALIYUN_OSS_CDN_URL` | OSS CDN 域名 |
| `FEISHU_WEBHOOK_URL` | 飞书 Webhook 地址 |
| `MAIL_ENABLED` | 是否启用邮件 | `false` |
| `SMTP_HOST` | SMTP 服务器 |
| `SMTP_PORT` | SMTP 端口 | `465` |
| `SMTP_USERNAME` | SMTP 用户名 |
| `SMTP_PASSWORD` | SMTP 密码 |
| `MAIL_FROM_EMAIL` | 发件人邮箱 |

## 许可证

MIT
