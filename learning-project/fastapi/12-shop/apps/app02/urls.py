#!/usr/bin/env python3
# coding: utf-8

"""
@File   : urls.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from fastapi import APIRouter

user = APIRouter()


@user.get("/login")
def shop_food():
    return {"shop": "food"}


@user.get("/reg")
def shop_food():
    return {"shop": "bed"}