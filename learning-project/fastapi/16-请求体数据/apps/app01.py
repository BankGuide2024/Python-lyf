#!/usr/bin/env python3
# coding: utf-8

"""
@File   : app01.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
import string
from datetime import datetime, date
from typing import List, Union, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

app01 = APIRouter()
class Addr(BaseModel):
    province: str
    city: str

class User(BaseModel):
    username: str
    age: int = Field(default=0,gt=0,lt=100)
    birthday: Union[date, None] = None
    friends: List[int] = []
    description : Optional[str] = None
    addr: Optional[Addr] = None # 嵌套其他类

    @field_validator("username")
    def name_must_alpha(cls, value):  # cls是约定用法，用于类本身，特别是不需要实例化的操作
        assert value.isalpha(),"必须是字母"
        return value

# 被其他类嵌套
class Data(BaseModel):
    data: List[User]

@app01.post("/user")
async def user(user:User):
    print(type(user))
    print(user.age)
    print(user.birthday)
    print(user.friends)
    print(user.model_dump())
    return user

@app01.post("/data")
async def data(data:Data):
    return data

