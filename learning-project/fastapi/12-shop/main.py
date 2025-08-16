#!/usr/bin/env python3
# coding: utf-8

"""
@File   : main.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from typing import Union
import uvicorn
from fastapi import FastAPI
from apps.app01.urls import shop
from apps.app02.urls import user

app = FastAPI()

app.include_router(shop,prefix="/shop",tags=["购物中心接口"])
app.include_router(user,prefix="/user",tags=["用户中心接口"])


if __name__ == '__main__':
    uvicorn.run(app)