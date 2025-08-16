#!/usr/bin/env python3
# coding: utf-8

"""
@File   : urls.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from fastapi import APIRouter

shop = APIRouter()


@shop.get("/food")
def shop_food():
    return {"shop": "food"}


@shop.get("/bed")
def shop_food():
    return {"shop": "bed"}