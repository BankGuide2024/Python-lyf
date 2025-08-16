#!/usr/bin/env python3
# coding: utf-8

"""
@File   : app01.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
import os.path
from typing import List

from fastapi import File, UploadFile, APIRouter,Request

app01 = APIRouter()

@app01.post("/items")
async def items(request:Request): #
    print("URL",request.url)
    print("客户端IP地址",request.client.host)
    print("客户端IP地址",request.headers.get("user-agent"))
    print("cookie",request.cookies)

    return {"URL":request.url,
            "IP":request.client.host,
            "Cookie":request.cookies,
            "User-Agent":request.headers.get("user-agent"),}