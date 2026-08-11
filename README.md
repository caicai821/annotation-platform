# 数据标注平台（Annotation Platform）

四人协作开发的数据标注平台，第一版目标：

> 登录 → 数据集 → 创建标注任务 → 文本/图像标注 → 保存标注结果

## 技术架构

- Frontend: 待确定（建议 Vue 3 + TypeScript）
- Backend: 待确定（建议 FastAPI）
- Database: 待确定（建议 MySQL）

## 项目结构

```text
annotation-platform/
├── frontend/          # 前端
├── backend/           # 后端
├── docs/              # 需求、数据库、API、设计文档
├── scripts/           # 开发/初始化脚本
├── .gitignore
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
Annotation
```

文本和图像标注最终统一保存为 `Annotation`，从而支持两组并行开发并最终合并。

## Git 协作规范

- `main`: 稳定、可运行代码，禁止直接开发
- `feature/*`: 功能开发分支
- 完成功能后通过 Pull Request 合并到 `main`
- Commit 推荐格式：`feat:` / `fix:` / `docs:` / `refactor:` / `chore:`

示例：

```bash
git checkout -b feature/text-annotation
git add .
git commit -m "feat: add text annotation editor"
git push -u origin feature/text-annotation
```

## 当前阶段

第一阶段先完成平台骨架、统一页面布局、数据集页面和基础 API 约定；之后分成：

- A + B：文本标注
- C + D：图像标注
