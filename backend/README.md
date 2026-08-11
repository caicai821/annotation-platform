# Backend

FastAPI + SQLAlchemy 2.0 + Pydantic v2。开发默认 SQLite，联调用 MySQL（改 `DATABASE_URL`）。

## 目录约定（与 CONTRIBUTING.md 一致）

```text
app/
├── main.py                  # 应用入口、统一返回格式、CORS
├── config.py                # 配置（.env）
├── database.py              # 引擎 / 会话 / Base
├── security.py              # 密码哈希、JWT、登录依赖
├── response.py              # 统一返回 ok()
├── models/                  # 负责人维护（Annotation 统一模型已定）
├── schemas/
│   ├── annotation.py        # 统一保存接口请求体
│   ├── text_annotation.py   # ★ 文本 payload 结构（A + B 所有）
│   └── image_annotation.py  # ★ 图像 payload 结构（C + D 所有）
└── routers/
    ├── auth.py / datasets.py / tasks.py      # 负责人维护
    └── annotations.py       # 统一标注接口 [约定]，payload 校验委托给各组 schema
```

## 开发

```bash
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

API 文档：http://localhost:8000/docs

## 测试账号

注册接口：`POST /api/auth/register`，填用户名密码即可使用。
