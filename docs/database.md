# 数据库设计（v1）

核心原则：**文本和图像标注共用 `annotations` 表**，通过 `type` 区分，`payload` 存 JSON。
这是两组并行开发能合到一起的关键，加表或改字段需 PR 讨论。

## 表结构

### users

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| username | VARCHAR(64) UNIQUE NOT NULL | 用户名 |
| password_hash | VARCHAR(255) NOT NULL | 密码哈希 |
| role | VARCHAR(16) DEFAULT 'annotator' | annotator / admin |
| created_at | DATETIME | |

### datasets

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| name | VARCHAR(128) NOT NULL | 数据集名 |
| type | VARCHAR(16) NOT NULL | text / image |
| description | TEXT | |
| created_by | BIGINT FK users.id | |
| created_at | DATETIME | |

### data_items

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| dataset_id | BIGINT FK datasets.id | |
| content | TEXT | 文本标注：原始文本；图像标注：图片相对路径 |
| meta | JSON | 扩展信息 |
| created_at | DATETIME | |

### tasks

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| dataset_id | BIGINT FK datasets.id | |
| name | VARCHAR(128) NOT NULL | |
| type | VARCHAR(16) NOT NULL | text / image，决定标注器 |
| status | VARCHAR(16) DEFAULT 'pending' | pending / in_progress / done |
| created_by | BIGINT FK users.id | |
| created_at | DATETIME | |

### annotations（统一标注表）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| task_id | BIGINT FK tasks.id | |
| item_id | BIGINT FK data_items.id | |
| annotator_id | BIGINT FK users.id | |
| type | VARCHAR(16) NOT NULL | text / image |
| payload | JSON NOT NULL | 标注内容，结构见 docs/api.md |
| status | VARCHAR(16) DEFAULT 'saved' | saved / submitted |
| created_at | DATETIME | |
| updated_at | DATETIME | |

唯一约束：`(task_id, item_id, annotator_id)` —— 同一个人对同一条目只存一份标注，重复保存即覆盖。

## 标注 payload 结构

- 文本（NER）：`{ "entities": [{ "start", "end", "label" }], "labels": [...] }`
- 图像（BBox）：`{ "boxes": [{ "x", "y", "width", "height", "label", "confidence" }], "labels": [...] }`

详细字段说明见 `docs/api.md`。

## 开发数据库

默认 `DATABASE_URL` 使用 SQLite（零配置启动）；部署/联调使用 MySQL：

```text
mysql+pymysql://user:password@localhost:3306/annotation
```

建表：后端启动时自动 `create_all`（骨架阶段够用；正式部署改用 Alembic 迁移）。
