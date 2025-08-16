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

from fastapi import File, UploadFile, APIRouter

app01 = APIRouter()

@app01.post("/file")
async def login(file:List[bytes] = File()): # 接受字节流文件
    print(file)
    return {"file": len(file)}


@app01.post("/uploadFile")
async def get_file(file:UploadFile): # UploadFile 文件对象
    print(file)
    path = os.path.join("imgs",file.filename)
    with open(path, "wb") as f:
        for line in file.file:
            f.write(line)
    return {
        "file": file.filename
    }

@app01.post("/uploadFiles")
async def get_files(files: List[UploadFile]): # UploadFile 文件对象
    return {
        "names": [file.filename for file in files]
    }