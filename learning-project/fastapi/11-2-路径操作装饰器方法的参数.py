#!/usr/bin/env python3
# coding: utf-8

"""
@File   : 11-2-路径操作装饰器方法的参数.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from typing import Union
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.post("/items",
          tags=["这是items的测试接口"],
          summary="这是一个关于items的总结",
          description="这是一个关于items的详细描述",
          response_description="这是一个关于items的响应描述...",
          deprecated=True) # deprecated=True 表示废弃
def test_post():
    return {"items": "items数据"}

@app.get("/items",
          tags=["这是items的测试接口2"],
          summary="这是一个关于items的总结",
          description="这是一个关于items的详细描述")
def test_get():
    return {"items": "items数据"}


if __name__ == '__main__':
    uvicorn.run(app)