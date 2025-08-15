import uvicorn
from fastapi import FastAPI

app = FastAPI()

# 启动方式
# uvicorn 10-quickstart:app

@app.get("/")
async def home():
    return {"hello": "world"}


if __name__ == '__main__':
    # uvicorn.run("10-quickstart:app", port=8000, reload=True)
    # 简略写法
    uvicorn.run(app)