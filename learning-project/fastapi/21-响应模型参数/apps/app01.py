#!/usr/bin/env python3
# coding: utf-8

"""
@File   : app01.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
import os.path
from typing import List, Union

from fastapi import File, UploadFile, APIRouter,Request
from pydantic import BaseModel

app01 = APIRouter()

class UserIn(BaseModel): # 输入模型
    name: str
    age: int
    password: str

class UserOut(BaseModel): # 输出模型
    name: str
    age: int


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
@app01.post("/user02",response_model=UserOut)
async def user02(user:UserIn): #
    return user

@app01.get("/items/{item_id}", response_model=Item, response_model_exclude_none=True)
async def read_item(item_id: str):
    # 如果值是None的不返回
    return items[item_id]

@app01.get("/items02/{item_id}", response_model=Item, response_model_include={"name","price"})
async def read_item(item_id: str):
    # 只展示 "name","price" 两个字段
    return items[item_id]

@app01.get("/items03/{item_id}", response_model=Item, response_model_exclude={"name","price"})
async def read_item(item_id: str):
    # 只展示 "name","price" 两个字段
    return items[item_id]