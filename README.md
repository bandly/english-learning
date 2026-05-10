# 英语学习应用

纯前端静态英语学习应用，支持词汇管理、练习和艾宾浩斯复习。

## 功能

- **词库管理**: 查看、搜索、筛选单词
- **听力练习**: 听音拼写
- **阅读练习**: 看词选义
- **写作练习**: 根据含义拼写
- **复习中心**: 艾宾浩斯遗忘曲线复习

## 添加单词

编辑 `frontend/src/data/vocabulary.json` 文件添加新单词：

```json
{
  "id": 11,
  "word": "example",
  "phonetic": "/ɪɡˈzæmpəl/",
  "meaning": "n. 例子",
  "part_of_speech": "noun",
  "example_sentence": "This is an example.",
  "difficulty_level": 2,
  "tags": ["基础"]
}
```

## 本地运行

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 技术栈

- Vue 3 + TypeScript
- Element Plus UI
- Pinia 状态管理
- Web Speech API（语音播放）
- localStorage（复习记录存储）