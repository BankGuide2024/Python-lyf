#!/usr/bin/env python3
# coding: utf-8

"""
@File   : 11-路径操作装饰器方法.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from typing import Union
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/get")
def get_test():
    return {"method": "get方法"}


@app.post("/post")
def post_test():
    return {"method": "post方法"}


@app.put("/put")
def put_test():
    return {"method": "put方法"}


@app.delete("/delete")
def delete_test():
    return {"method": "delete方法"}


if __name__ == '__main__':
    uvicorn.run(app)