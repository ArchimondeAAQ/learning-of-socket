import socket
import _thread

from request import Request
from utils import log

from models.__init__ import SQLModel
'''
使用单例（mysql connection）时，from models.__init__ import SQLModel 与 from models import SQLModel 有区别...
'''
from routes import error
from routes.routes_todo_ajax import route_dict as todo_ajax_routes
from routes.routes_weibo import route_dict as weibo_routes
from routes.routes_user import route_dict as user_routes
from routes.routes_public import route_dict as public_routes


def response_for_path(request):
    r = {}

    # 注册其他模块的路由
    r.update(weibo_routes())
    r.update(user_routes())
    r.update(public_routes())
    r.update(todo_ajax_routes())
    response = r.get(request.path, error)

    return response(request)


def request_from_connection(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            request = request.decode()
            return request


def process_request(connection):
    with connection:
        r = request_from_connection(connection)
        # log('request log:\n <{}>'.format(r))
        # 把原始请求数据传给 Request 对象
        if len(r) > 0:
            request = Request(r)
            # 用 response_for_path 函数来得到 path 对应的响应内容
            response = response_for_path(request)
            # log("response log:\n <{}>".format(response))
            # 把响应发送给客户端
            connection.sendall(response)


def run(host, port):

    # 初始化数据库
    SQLModel.init_db()

    # 初始化socket
    log('开始运行于', 'http://{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        # 无限循环来处理请求
        while True:
            # accept()为阻塞函数
            connection, address = s.accept()
            log('ip {}'.format(address))
            # 多线程
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    # 生成配置，运行程序
    config = dict(
        host='127.0.0.1',
        port=3000,
    )
    run(**config)
