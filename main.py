from fastapi import FastAPI
from routers.build import router as build_router
from common.logger import logger
from common.middleware import add_trace_id_middleware

# 创建 FastAPI 实例
app = FastAPI()

# 添加中间件
app.middleware("http")(add_trace_id_middleware)

app.include_router(build_router, prefix="/api", tags=["build"])

@app.get("/", tags=["root"])
async def read_root():
    logger.info("Received request for root")
    return {"message": "successfully!"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host='0.0.0.0', port=8080, reload=True)
