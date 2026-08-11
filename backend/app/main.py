from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import Base, engine
from .routers import annotations_router, auth_router, datasets_router, tasks_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="数据标注平台 API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(datasets_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(annotations_router, prefix="/api")


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": detail.get("code", 40000), "message": detail.get("message", "请求失败"), "data": None},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": 40000, "message": str(detail), "data": None},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"code": 50001, "message": f"服务器内部错误: {exc}", "data": None},
    )


@app.get("/api/health")
def health():
    return {"code": 0, "message": "ok", "data": {"status": "up"}}
