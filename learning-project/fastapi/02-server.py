import socket

sock = socket.socket()

sock.bind(('127.0.0.1', 8080))
sock.listen(5)

while True:
    conn,addr = sock.accept() # 阻塞等待客户端链接
    data = conn.recv(1024)
    print("客户端发送的请求信息：\n",data)

    conn.send(b"HTTP/1.1 200 ok\r\nserver:yuan\r\n\r\nhello world")
    # HTTP/1.1 200 ok -> 请求首行
    # server:yuan -> 请求头
    # hello world -> 请求体
    conn.close()
