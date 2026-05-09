# English Learning Frontend

Vue 3 + TypeScript frontend for English learning application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

## Features

- **词汇管理**: 添加、编辑、删除单词
- **练习中心**: 听力、阅读、写作练习
- **复习中心**: 艾宾浩斯复习计划

## Project Structure

```
src/
├── api/          # API封装
├── assets/       # 样式和图片
├── components/   # 公共组件
├── router/       # 路由配置
├── stores/       # Pinia状态管理
├── types/        # TypeScript类型
├── views/        # 页面组件
└── main.ts       # 应用入口
```

## Development

The frontend runs on http://localhost:5173
Proxy to backend API at http://localhost:8000