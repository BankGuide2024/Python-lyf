# fastapi
## http请求
### 请求报文格式
请求首行：post /api/v1/auth/password... HTTP/1.1
请求头:
content-type:application/json -> 格式
user-agent:Chrome/...

请求体：
{
    "username":"yuan",
    "password":"123"
}
### 响应报文格式
响应首行
HTTP/1.1 200 OK
响应头
content-type:application/json -> 格式
...

响应体
{
    "username":"yuan",
    "password":"123"
}

## restful
对于数据资源分别使用POST、DELETE、GET、UPDATE等请求动作来表达对数据的增删改查

比如我的资源是 /student
POST请求 -> 增加
GET请求 -> 查询
    /student/1 表示获取id为1的学生
DELETE请求 -> 删除
PUT请求 -> 修改

## form表单数据
在OAuth规范的一种实用方式（密码流）中，需要将用户名、密码作为表单字段发送，而不是json
FastAPI 用Form组件接受表单数据
