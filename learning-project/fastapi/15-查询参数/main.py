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

from apps.app01 import app01
from apps.app02 import app02

app = FastAPI()

app.include_router(app01,tags=["01-查询参数"])
app.include_router(app02, tags=["02-查询参数"])

if __name__ == '__main__':
    uvicorn.run(app)