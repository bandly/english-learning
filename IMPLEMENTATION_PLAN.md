# 英语学习软件实现计划

## Context

用户要开发一个英语学习Web应用，用于日常单词/句子的录入和练习。核心需求：
- 手动录入单词/句子到云端数据库
- 四种练习模式：听、说、读、写
- 艾宾浩斯遗忘曲线复习机制
- 简单账号系统用于数据隔离
- 线上部署

技术栈：Vue 3 + Python FastAPI + PostgreSQL

---

## 项目结构

```
english/
├── frontend/                    # Vue 3 前端
│   ├── src/
│   │   ├── components/         # 组件
│   │   │   ├── vocabulary/     # 词汇管理：WordCard, WordForm, WordList
│   │   │   ├── practice/       # 练习模块：Listening, Speaking, Reading, Writing
│   │   │   └── review/         # 复习模块：ReviewCard, ReviewSchedule
│   │   ├── composables/        # 组合式函数
│   │   │   ├── useAudio.ts            # 音频播放
│   │   │   ├── useSpeechRecognition.ts # 语音识别
│   │   │   └── useReviewAlgorithm.ts   # 复习算法
│   │   ├── stores/             # Pinia状态管理
│   │   │   ├── vocabulary.ts
│   │   │   ├── practice.ts
│   │   │   ├── review.ts
│   │   ├── views/              # 页面视图
│   │   │   ├── VocabularyView.vue     # 词汇管理页
│   │   │   ├── PracticeView.vue       # 练习中心
│   │   │   ├── ReviewView.vue         # 复习中心
│   │   ├── api/                # API封装
│   │   ├── router/             # 路由配置
│   │   └── types/              # TypeScript类型定义
│   └── vite.config.ts
│
├── backend/                     # FastAPI 后端
│   ├── app/
│   │   ├── main.py             # 应用入口
│   │   ├── config.py           # 配置管理
│   │   ├── database.py         # 数据库连接
│   │   ├── models/             # SQLAlchemy模型
│   │   │   ├── user.py
│   │   │   ├── vocabulary.py
│   │   │   ├── sentence.py
│   │   │   ├── learning_record.py
│   │   │   └── review_schedule.py
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── api/routes/         # API路由
│   │   │   ├── auth.py         # 认证
│   │   │   ├── vocabulary.py   # 词汇CRUD
│   │   │   ├── practice.py     # 练习
│   │   │   ├── review.py       # 复习
│   │   ├── services/           # 业务逻辑
│   │   │   ├── review_algorithm.py    # 艾宾浩斯算法 ⭐核心
│   │   │   ├── speech_service.py      # 语音服务
│   │   ├── core/               # 安全、异常处理
│   ├── alembic/                # 数据库迁移
│   ├── requirements.txt
│   └── .env
│
├── docs/
│   ├── API.md                  # API文档
│   └── DATABASE.md             # 数据库设计
│
└── docker-compose.yml          # Docker编排
```

---

## 数据库设计

### 核心表结构

| 表名 | 用途 | 关键字段 |
|------|------|----------|
| **users** | 用户表 | username, password_hash(可选), settings |
| **words** | 单词表 | word, phonetic, meaning, part_of_speech, example_sentence, difficulty_level, tags, user_id |
| **sentences** | 句子表 | sentence, translation, difficulty_level, user_id |
| **learning_records** | 学习记录 | item_type, item_id, practice_type, score, is_correct, time_spent |
| **review_schedules** | 复习计划 ⭐ | next_review_date, review_count, ease_factor, interval_days, status |
| **word_progress** | 进度跟踪 | mastery_level, total_practice_count, 各模式正确率 |

### 复习计划表详解（艾宾浩斯核心）

```sql
CREATE TABLE review_schedules (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    item_type VARCHAR(20),        -- 'word' or 'sentence'
    item_id INTEGER,
    next_review_date TIMESTAMP,   -- 下次复习时间 ⭐
    review_count INTEGER,         -- 已复习次数
    ease_factor DECIMAL(3,2),     -- 难度因子（SM-2算法）默认2.5
    interval_days INTEGER,        -- 当前间隔天数
    last_review_date TIMESTAMP,
    status VARCHAR(20)            -- 'learning', 'review', 'mastered'
);
```

---

## API 设计

### 认证 API
- `POST /api/auth/register` - 注册（username可选密码）
- `POST /api/auth/login` - 登录，返回JWT token
- `GET /api/auth/me` - 获取当前用户

### 词汇 API
- `POST /api/words` - 添加单词
- `GET /api/words?skip=0&limit=20&tag=高频` - 获取单词列表
- `PUT /api/words/{id}` - 更新单词
- `DELETE /api/words/{id}` - 删除单词
- `POST /api/words/batch` - 批量导入

### 练习 API
- `GET /api/practice/words?count=10` - 获取练习内容
- `POST /api/practice/listening` - 提交听力结果 {item_type, item_id, user_answer, time_spent}
- `POST /api/practice/speaking` - 提交口语（含音频文件）
- `POST /api/practice/reading` - 提交阅读结果
- `POST /api/practice/writing` - 提交写作结果

### 复习 API ⭐
- `GET /api/review/today` - 获取今日需复习内容
- `POST /api/review/submit` - 提交复习评分 {item_type, item_id, score: 0-5}
- `GET /api/review/stats` - 获取复习统计

---

## 艾宾浩斯算法实现（SM-2改进版）

### 算法原理
- **评分等级**：0-5（0=完全忘记，5=完美记忆）
- **难度因子**：默认2.5，根据评分动态调整
- **间隔计算**：
  - 评分<3：重置，间隔=1天
  - 首次复习：间隔=1天
  - 第二次：间隔=2天
  - 之后：interval = ceil(上次间隔 × 难度因子)

### 核心代码结构

```python
# backend/app/services/review_algorithm.py
class EbbinghausAlgorithm:
    def calculate_next_review(
        self, quality: int,      # 用户评分 0-5
        review_count: int,       # 已复习次数
        ease_factor: float,      # 当前难度因子
        last_interval: int       # 上次间隔天数
    ) -> Tuple[datetime, int, float]:
        """
        返回：(下次复习时间, 间隔天数, 新难度因子)

        难度因子更新公式（SM-2）：
        EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        """
        # 评分低于3则重置学习
        if quality < 3:
            return datetime.now() + timedelta(days=1), 1, 2.5

        # 计算新难度因子
        new_ef = max(1.3, ease_factor + 0.1 - (5-quality)*(0.08+(5-quality)*0.02))

        # 计算间隔
        if review_count == 0:
            interval = 1
        elif review_count == 1:
            interval = 2
        else:
            interval = ceil(last_interval * new_ef)

        return datetime.now() + timedelta(days=interval), interval, new_ef
```

---

## 实现步骤（6周计划）

### 阶段一：基础架构（第1-2周）

**第1周 - 后端基础**
1. 项目初始化：FastAPI + SQLAlchemy + Alembic
2. 数据模型实现 + 数据库迁移
3. 用户认证系统（JWT）
4. 词汇/句子 CRUD API

**第2周 - 前端基础**
1. Vue 3 + Vite + Element Plus + Pinia 初始化
2. 用户状态管理 + API客户端封装
3. 登录/注册页面
4. 词汇管理界面（列表、表单、批量导入）

### 阶段二：练习功能（第3-4周）

**第3周 - 听力和阅读**
1. 语音服务集成：
   - TTS：pyttsx3（离线免费）或 Azure Speech（高质量）
   - 音频文件存储
2. 听力练习：播放 → 选择/拼写 → 反馈
3. 阅读练习：看词选义 → 填空 → 统计

**第4周 - 口语和写作**
1. 语音识别：
   - 前端：Web Speech API（免费）
   - 后端评分：文本匹配 或 Azure/百度语音
2. 口语练习：录音 → 识别 → 评分
3. 写作练习：拼写/造句 → 自动评分

### 阶段三：复习机制（第5周）

1. 艾宾浩斯算法实现（review_algorithm.py）
2. 复习API开发（review.py路由）
3. 复习界面：今日复习列表、评分卡片、统计图表
4. 复习提醒（可选）

### 阶段四：部署优化（第6周）

1. 性能优化：代码分割、懒加载、API缓存
2. 测试：后端单元测试、前端组件测试
3. 部署：
   - 后端：Gunicorn + Uvicorn → 云服务器
   - 前端：Vercel/Netlify 或 Nginx
   - 数据库：PostgreSQL云服务

---

## 关键技术点

### 语音功能方案
| 功能 | 方案1（免费） | 方案2（高质量付费） |
|------|---------------|---------------------|
| TTS（文字转语音） | pyttsx3本地 / Web Speech API | Azure Speech Service |
| STT（语音识别） | Web Speech API前端 | Azure/百度语音API |
| 发音评分 | 简单文本匹配 | Azure Pronunciation Assessment |

### 前端语音处理

```typescript
// 播放音频
const utterance = new SpeechSynthesisUtterance(word)
utterance.lang = 'en-US'
speechSynthesis.speak(utterance)

// 语音识别
const recognition = new webkitSpeechRecognition()
recognition.lang = 'en-US'
recognition.onresult = (e) => transcript = e.results[0][0].transcript
recognition.start()
```

---

## 验证与测试

### 功能验证清单
- [ ] 用户注册登录，数据隔离正常
- [ ] 单词/句子录入、编辑、删除
- [ ] 听力练习：播放音频，答案判断正确
- [ ] 口语练习：录音、识别、评分反馈
- [ ] 阅读练习：选义、填空功能正常
- [ ] 写作练习：拼写判断、造句评分
- [ ] 复习算法：间隔计算符合艾宾浩斯曲线
- [ ] 今日复习列表准确显示待复习内容
- [ ] 复习评分后更新下次复习时间

### 部署验证
- [ ] 后端API可访问，返回正确响应
- [ ] 前端页面加载正常，样式正确
- [ ] 语音功能在生产环境可用
- [ ] 数据库连接稳定
- [ ] HTTPS配置正确

---

## 核心文件清单

实现时优先关注以下5个关键文件：

1. **backend/app/services/review_algorithm.py** - 艾宾浩斯算法核心
2. **backend/app/models/vocabulary.py** - 词汇数据模型
3. **backend/app/api/routes/practice.py** - 练习API路由
4. **frontend/src/components/practice/ListeningPractice.vue** - 听力练习组件（前端模式参考）
5. **frontend/src/stores/review.ts** - 复习状态管理

---

## 后续优化方向

1. 数据可视化：学习曲线、记忆保持率图表
2. 社交功能：学习打卡、排行榜
3. AI辅助：智能推荐学习内容、生成例句
4. 离线支持：PWA离线学习
5. 多端扩展：微信小程序、移动App