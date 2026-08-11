# 协作规范（必读）

本文件是四人团队的协作约定，开工前请通读一遍。

## 1. 三种必须遵守的规则

1. **永远只改自己目录里的文件**（见第 4 节所有权表）。改别人目录 = 制造合并冲突。
2. **开工前先 `git pull`**，避免基于过期代码开发。
3. **提交信息带前缀**：`feat:`（新功能）/ `fix:`（修 bug）/ `docs:`（文档）/ `refactor:`（重构）/ `chore:`（杂项）。

## 2. 基本 Git 流程（不会的按下面抄）

每次开工：

```bash
git pull                       # 1. 拿最新代码
git checkout -b feature/text-annotation   # 2. 建自己的分支（文本组示例）
# ... 写代码 ...
git add .                      # 3. 暂存改动
git commit -m "feat: 完成 NER 标注编辑"   # 4. 提交
git push -u origin feature/text-annotation  # 5. 推送到 GitHub
```

然后到 GitHub 网页上：找到自己的分支 → 点 **Pull Request** → 描述改动 → 创建 → 等骨架负责人合并。

每天结束前（避免冲突堆积）：

```bash
git pull origin main           # 把 main 的新改动拉到自己分支
# 如果有冲突，只解决自己目录里的冲突，共享文件冲突立即找负责人
git push
```

常用命令速查：

```bash
git status                     # 看哪些文件改了
git diff                       # 看改动内容
git log --oneline -10          # 看最近提交
git branch -a                  # 看所有分支
```

## 3. 分支规范

| 分支 | 用途 | 谁可以合并 |
|---|---|---|
| `main` | 稳定可运行代码 | 骨架负责人（PR） |
| `feature/text-annotation` | 文本组 A/B | 自己 PR |
| `feature/image-annotation` | 图像组 C/D | 自己 PR |

分支命名：`feature/<功能名>`。**一个功能一个分支，做完就删。**

## 4. 目录所有权表（冲突最小化的关键）

| 路径 | 所有者 | 说明 |
|---|---|---|
| `frontend/src/layouts/` | 骨架负责人 | 统一布局，其他人别动 |
| `frontend/src/router/` | 骨架负责人 | 路由注册，标注页路由已占位 |
| `frontend/src/api/` | 骨架负责人 | 统一 HTTP 客户端；自己新建 `textApi.ts` / `imageApi.ts` 属于自己 |
| `frontend/src/components/` | 共享 | 新增组件前先问一句有没有重名 |
| `frontend/src/views/annotate/text/**` | **A + B** | 文本标注全权 |
| `frontend/src/views/annotate/image/**` | **C + D** | 图像标注全权 |
| `frontend/src/views/` 其余 | 骨架负责人 | 登录/数据集/任务页 |
| `backend/app/models/` | 骨架负责人 | 数据模型已定，加字段需 PR 讨论 |
| `backend/app/schemas/` | 骨架负责人 | 同上 |
| `backend/app/schemas/text_annotation.py` | **A + B** | 文本 payload 结构定义 |
| `backend/app/schemas/image_annotation.py` | **C + D** | 图像 payload 结构定义 |
| `backend/app/routers/annotations.py` | 负责人维护 | 统一标注接口，payload 校验自动走各组 schema |
| `backend/app/routers/` 其余 | 骨架负责人 | auth/datasets/tasks |
| `docs/` | 全部 | 改文档直接小 PR |

### 共享文件的黄金法则

以下文件**骨架阶段已定死，任何人不准改**，改前必须先问负责人：

- `frontend/src/router/index.ts`、`frontend/src/layouts/**`
- `backend/app/models/annotation.py`（Annotation 统一模型）
- `docs/api.md` 中带 `[约定]` 标记的接口

## 5. 合并冲突怎么办（每个开发都会遇到）

1. 冲突只发生在**同一文件被两人改了**——所以遵守所有权表就很少遇到
2. 遇到时：`git pull origin main` → 用编辑器打开冲突文件 → 保留两个版本中正确的部分 → 删掉 `<<<<<<<` `=======` `>>>>>>>` 标记 → `git add .` → `git commit`
3. 拿不准怎么保留就截图发群里，别乱删

## 6. 提交规范

- 一个小功能一个小提交，别攒一堆一次性提交
- 消息模板：`feat: <做什么>`，例如 `feat: 添加 NER 标签面板`、`fix: 修复标注保存失败`
- 不提交：`node_modules/`、`.env`、数据库文件（`.gitignore` 已处理）

## 7. 骨架合并说明

同伴已有的简单前端页面尚未入库。骨架负责人收齐后，将把它合并进 main（替换对应占位页），
其余三人先基于当前骨架开发，页面合入后只需 `git pull` 即可拿到最新版。
