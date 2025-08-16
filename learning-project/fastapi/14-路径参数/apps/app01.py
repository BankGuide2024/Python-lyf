#!/usr/bin/env python3
# coding: utf-8

"""
@File   : app01.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from fastapi import APIRouter

app01 = APIRouter()

@app01.get("/user/{user_id}")
def get_user(user_id:int):
    # 路径上传入的id，默认都是str
    # 如果想要传入的是int类型，就写user_id:int
    print(type(user_id))
    return {"username": user_id, "email": "123"}