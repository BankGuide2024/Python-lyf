#!/usr/bin/env python3
# coding: utf-8

"""
@File   : app01.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from typing import Union, Optional

from fastapi import APIRouter

app02 = APIRouter()

@app02.get("/shop/{shop_id}")
async def shop(shop_id: int):
    # 路径上传入的id，默认都是str
    # 如果想要传入的是int类型，就写user_id:int
    print(type(shop_id))
    return {"username": shop_id, "email": "123"}


@app02.get("/shop/")
async def shop(kd,xl,gj):
    # 除了{}之外的，都会被识别为查询参数
    return {"username": kd, "email": xl,"gj":gj}

@app02.get("/shop/{kd}")
async def shop(kd,xl,gj):
    # 除了{}之外的，都会被识别为查询参数
    return {"username": kd, "email": xl,"gj":gj}

# 可选参数
@app02.get("/shop2/{kd}")
async def shop(kd,xl=None,gj=None): # 有默认参数即 可选填
    # 除了{}之外的，都会被识别为查询参数
    return {"username": kd, "email": xl,"gj":gj}

# 可选参数
@app02.get("/shop3/{kd}")
async def shop(kd:int,xl:Union[str,None]=None,gj:Optional[str] = None): # 有默认参数即 可选填
    # 除了{}之外的，都会被识别为查询参数

    # xl:Union[str,None] -> 这样写，仍然是一个必选项
    # xl:Union[str,None]=None ->这样写，就是一个可选项
    # 简写 gj:Optional[str] = None
    return {"username": kd, "email": xl,"gj":gj}