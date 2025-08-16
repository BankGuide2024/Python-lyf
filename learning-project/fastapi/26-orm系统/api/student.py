#!/usr/bin/env python3
# coding: utf-8

"""
@File   : student.py
@Author : lyf
@Date   : 2025/8/16
@Desc   : 
"""
from fastapi import APIRouter
from models import *
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


@student_api.post('/')
def getAllStudent():
    return {
        "操作": "查看所有的学生"
    }

@student_api.get('/{student_id}')
def getOneStudent(student_id: int):
    return {
        "操作": f"查看id={student_id}所有的学生"
    }

@student_api.delete('/{student_id}')
def deleteOneStudent(student_id: int):
    return {
        "操作": f"删除id={student_id}所有的学生"
    }

@student_api.put('/{student_id}')
def putOneStudent(student_id: int):
    return {
        "操作": f"更新id={student_id}所有的学生"
    }