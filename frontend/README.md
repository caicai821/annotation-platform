# Frontend

Vue 3 + TypeScript + Vite + Element Plus + Pinia + Vue Router。

## 目录约定（与 CONTRIBUTING.md 一致）

```text
src/
├── api/                  # 统一 HTTP 客户端（负责人维护）
│   ├── http.ts           # axios 实例、统一返回处理
│   ├── auth.ts / datasets.ts / tasks.ts
│   ├── textApi.ts        # 文本组 API（A + B 所有）
│   └── imageApi.ts       # 图像组 API（C + D 所有）
├── components/           # 共享组件
├── layouts/              # 统一布局（负责人维护）
├── router/               # 路由（负责人维护，标注页路由已占位）
├── stores/               # Pinia
├── types/                # 共享类型
└── views/
    ├── auth/ dashboard/ datasets/ tasks/
    └── annotate/
        ├── text/         # ★ A + B 全权
        └── image/        # ★ C + D 全权
```

## 开发

```bash
npm install
npm run dev       # http://localhost:5173，/api 代理到 8000
npm run build     # vue-tsc 类型检查 + 打包
```
