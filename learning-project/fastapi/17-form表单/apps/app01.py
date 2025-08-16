#!/usr/bin/env python3
# coding: utf-8

"""
@File   : app01.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from fastapi import APIRouter, Form
from pydantic import BaseModel, Field, field_validator

app01 = APIRouter()

@app01.post("/login")
async def login(username: str = Form(), password: str = Form()): # 加上form就不是查询参数了，变成了请求体参数
    print(username, password)
    return {"username": username}