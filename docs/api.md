# API 约定（v1）

所有接口前缀：`/api`。请求/响应均为 JSON。标注相关接口是全组协作的关键，带 `[约定]` 的**不允许擅自修改**，改前先 PR 讨论。

## 统一返回格式

```json
{ "code": 0, "message": "ok", "data": { } }
```

`code != 0` 表示失败，`message` 为错误说明。

## 鉴权

登录接口返回 `token`（JWT），其他接口请求头携带：

```
Authorization: Bearer <token>
```

## 接口清单

| 方法 | 路径 | 说明 | 状态 |
|---|---|---|---|
| POST | `/api/auth/login` | 登录，返回 token | 骨架 |
| POST | `/api/auth/register` | 注册 | 骨架 |
| GET | `/api/datasets` | 数据集列表 | 骨架 |
| POST | `/api/datasets` | 创建数据集 | 骨架 |
| GET | `/api/datasets/{id}/items` | 数据集下的数据条目 | 骨架 |
| POST | `/api/datasets/{id}/items` | 上传/添加数据条目 | 骨架 |
| GET | `/api/tasks` | 标注任务列表 | 骨架 |
| POST | `/api/tasks` | 创建标注任务 | 骨架 |
| GET | `/api/tasks/{id}` | 任务详情（含条目列表） | 骨架 |
| PUT | `/api/tasks/{id}` | 修改任务 | 骨架 |

### 标注接口 `[约定]`

文本组与图像组共用同一套接口，仅 `payload` 结构不同：

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/tasks/{task_id}/items/{item_id}/annotation` | 取该条目的已存标注（无则返回 `{"data": null}`） |
| PUT | `/api/tasks/{task_id}/items/{item_id}/annotation` | 保存/覆盖标注 |

PUT 请求体：

```json
{
  "type": "text",
  "payload": {}
}
```

- `type`：`"text"` 或 `"image"`
- `payload`：文本组存 NER 结构，图像组存 Bounding Box 结构（结构定义各自写在下方，两组互不干扰）

### 文本标注 payload（A + B 定义）

```json
{
  "entities": [
    { "start": 3, "end": 6, "label": "人名" }
  ],
  "labels": ["人名", "地名", "机构"]
}
```

`start`/`end` 为字符区间（含 start，不含 end），对应 DataItem 的原始文本。

### 图像标注 payload（C + D 定义）

```json
{
  "boxes": [
    { "x": 12, "y": 34, "width": 100, "height": 80, "label": "car", "confidence": 1.0 }
  ],
  "labels": ["car", "person"]
}
```

坐标按图片原始像素，前端标注时通过图片显示尺寸换算。

## 分页

列表接口统一支持 `?page=1&page_size=20`，返回：

```json
{ "items": [], "total": 0, "page": 1, "page_size": 20 }
```

## 错误码

| code | 含义 |
|---|---|
| 0 | 成功 |
| 40001 | 参数错误 |
| 40101 | 未登录/token 失效 |
| 40301 | 无权限 |
| 40401 | 资源不存在 |
| 50001 | 服务器内部错误 |
