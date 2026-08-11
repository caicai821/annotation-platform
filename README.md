# 数据标注平台（Annotation Platform）

四人协作开发的数据标注平台，MVP 目标：

> 登录 → 数据集 → 创建标注任务 → 文本/图像标注 → 保存标注结果

## 技术架构（已定案）

| 层 | 技术栈 |
|---|---|
| Frontend | Vue 3 + TypeScript + Vite + Element Plus + Pinia + Vue Router |
| Backend | FastAPI + SQLAlchemy 2.0 + Pydantic v2 |
| Database | MySQL（开发可用 SQLite，通过 `DATABASE_URL` 切换） |

## 项目结构

```text
annotation-platform/
├── frontend/          # Vue 3 前端
├── backend/           # FastAPI 后端
├── docs/              # 需求、数据库、API 约定文档
├── scripts/           # 开发/初始化脚本
├── .gitignore
├── CONTRIBUTING.md    # ★ 协作规范（必读）
└── README.md
```

## 核心业务模型

```text
User
  ↓
Dataset
  ↓
DataItem
  ↓
Task
  ↓
Annotation（type: text | image，content: JSON）
```

文本和图像标注统一保存为 `Annotation` 表，两组只差 `type` 和 `content` 结构，
各自独立开发、通过统一 API 约定合并，互不冲突。

- 模型定义与 API 约定见 `docs/database.md`、`docs/api.md`

## 四人分工（文件所有权）

| 人 | 职责 | 拥有的目录 |
|---|---|---|
| 骨架负责人 | 布局/路由/登录/数据集/任务 + API 约定 | 共享目录（维护者） |
| A + B | 文本标注（NER） | `frontend/src/views/annotate/text/**`、`backend/app/routers/text_annotation.py` |
| C + D | 图像标注（Bounding Box） | `frontend/src/views/annotate/image/**`、`backend/app/routers/image_annotation.py` |

详细规则见 `CONTRIBUTING.md`。

## Git 协作规范（摘要）

- `main`：稳定、可运行代码，禁止直接开发
- 每人从 main 拉取，在 `feature/xxx` 分支开发，完成后 PR 合并
- Commit 格式：`feat:` / `fix:` / `docs:` / `refactor:` / `chore:`
- 完整教程见 `CONTRIBUTING.md`

## 本地开发

### 后端

```bash
cd backend
pip install -r requirements.txt
copy .env.example .env        # 修改数据库连接
uvicorn app.main:app --reload --port 8000
```

API 文档：http://localhost:8000/docs

### 前端

```bash
cd frontend
npm install
npm run dev                   # http://localhost:5173
```

## 当前阶段

骨架阶段已完成：布局、路由、登录/数据集/任务页面、统一 Annotation 模型与 API 约定。
下一步：文本组与图像组基于骨架各自开分支开发标注功能。
