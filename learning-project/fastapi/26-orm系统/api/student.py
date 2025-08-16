#!/usr/bin/env python3
# coding: utf-8

"""
@File   : student.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from typing import List
from fastapi import APIRouter, HTTPException
from models import *
from pydantic import BaseModel, field_validator

student_api = APIRouter()

@student_api.get('/')
async def getAllStudent():
    # 1、查询所有 all()
    students = await Student.all() # Query_set类型 返回的是[Student(),Student(),Student()]

    # for stu in students:
    #     print(stu.name)
    # 2、过滤查询
    # students = await Student.filter(clas_id=1) # Query_set类型 返回的是[Student(),Student(),Student()]

    # 3、指定查询
    # students = await Student.get(clas_id=1) # Student()

    # 4、模糊查询
    # __gt表示大于
    # students = await Student.filter(sno__gt=1234)  # [Student()]
    # __range 表示查询范围
    # students = await Student.filter(sno__range=[1,1235])  # [Student()]
    # students2 = await Student.filter(sno__in=[1,1235])  # [Student()]

    # 5、value查询
    students = await Student.all().values("name")  # [{"name":name1},{"name":name2}]
    students2 = await Student.all().values("name","sno")  # [{"name":name1},{"name":name2}]

    print(students2)
    return {
        "操作":students
    }

class StudentIn(BaseModel):
    sno: int
    pwd: str
    name: str
    courses : List[int]
    clas_id: int

    @field_validator("name")
    def name_must_alpha(cls, value):
        assert value.isalpha,"姓名必须是英文字母"
        return value

@student_api.post('/')
async def getAllStudent(student_in: StudentIn):

    # 插入到数据库
    # 方式1
    # student = Student(name=student_in.name, sno=student_in.sno, pwd=student_in.pwd,clas_id=student_in.clas_id)
    # await student.save() # 插入数据库

    # 方式2
    # student = await Student.create(name=student_in.name, sno=student_in.sno, pwd=student_in.pwd,clas_id=student_in.clas_id)

    # 多对多的关系绑定
    student = await Student.create(name=student_in.name, sno=student_in.sno, pwd=student_in.pwd,clas_id=student_in.clas_id)
    # ??
    return {
        "操作": "查看所有的学生"
    }

@student_api.get('/{student_id}')
async def getOneStudent(student_id: int):
    students = await Student.get(id=student_id)  # [{"name":name1},{"name":name2}]
    return {
        "操作": f"查看id={student_id}所有的学生"
    }

@student_api.delete('/{student_id}')
async def deleteOneStudent(student_id: int):
    deleteCount = await Student().filter(id=student_id).delete()
    if not deleteCount:
        raise HTTPException(status_code=404, detail=f"主键为{student_id}的不存在")
    return {
        "操作": f"删除id={student_id}所有的学生"
    }

@student_api.put('/{student_id}')
async def putOneStudent(student_id: int, student_in: StudentIn):
    student = await Student().filter(id=student_id).update(**student_in.model_dump())

    return {
        "操作": f"更新id={student_id}所有的学生"
    }