#!/usr/bin/env python3
# coding: utf-8

"""
@File   : main.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
app = FastAPI()

# fastapi一旦运行，register_tortoise就会执行
register_tortoise(
    app,
    config = TORTOISE_ORM
)

if __name__ == '__main__':
    uvicorn.run(app)