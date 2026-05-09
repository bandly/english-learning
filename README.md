# 英语学习软件

一个用于英语单词/句子学习的Web应用，支持录入、练习（听说读写）和艾宾浩斯复习机制。

## 项目结构

```
english/
├── backend/          # FastAPI 后端
│   ├── app/          # 应用代码
│   │   ├── models/   # 数据模型
│   │   ├── schemas/  # API schemas
│   │   ├── api/      # 路由
│   │   ├── services/ # 业务逻辑（含艾宾浩斯算法）
│   │   └── core/     # 安全模块
│   └── requirements.txt
│
├── frontend/         # Vue 3 前端
│   ├── src/
│   │   ├── views/    # 页面组件
│   │   ├── stores/   # Pinia状态管理
│   │   ├── api/      # API封装
│   │   └── router/   # 路由
│   └── package.json
│
└── IMPLEMENTATION_PLAN.md  # 实现计划文档
```

## 快速启动

### 1. 启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
cp .env.example .env

# 初始化数据库
python -m app.init_db

# 启动服务器
python run_server.py
```

后端运行在 http://localhost:8000

API文档: http://localhost:8000/docs

### 2. 启动前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 http://localhost:5173

## 功能清单

### 后端 API

| 功能 | API |
|------|-----|
| 用户注册 | POST /api/auth/register |
| 用户登录 | POST /api/auth/login |
| 添加单词 | POST /api/words |
| 获取单词列表 | GET /api/words |
| 批量导入 | POST /api/words/batch |
| 听力练习 | POST /api/practice/listening |
| 阅读练习 | POST /api/practice/reading |
| 写作练习 | POST /api/practice/writing |
| 今日复习 | GET /api/review/today |
| 提交复习 | POST /api/review/submit |
| 复习统计 | GET /api/review/stats |

### 前端页面

- **登录/注册页**: 简单账号系统
- **词汇管理页**: 添加、查看、删除单词
- **练习中心**: 听力、阅读、写作三种练习模式
- **复习中心**: 今日复习列表、艾宾浩斯评分

## 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: Vue 3 + TypeScript + Element Plus + Pinia
- **算法**: 艾宾浩斯遗忘曲线 + SM-2算法

## 下一步

1. 安装依赖并启动服务
2. 打开浏览器访问 http://localhost:5173
3. 注册账号并开始添加单词
4. 在练习中心进行练习
5. 在复习中心按艾宾浩斯曲线复习