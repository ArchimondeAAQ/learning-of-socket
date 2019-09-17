import json
import os.path
from urllib.parse import quote

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.session import Session
from models.user import User
from utils import log


def initialized_environment():
    # os.path.dirname() 返回当前文件/文件夹所在目录
    parent = os.path.dirname(os.path.dirname(__file__))
    # 设定加载模板的目录
    path = os.path.join(parent, 'templates')

    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class TestTemplate(object):
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        template = cls.e.get_template(filename)
        # 用 render() 方法渲染模板
        # 可以传递参数
        return template.render(*args, **kwargs)


def current_user(request):
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.one(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.one(id=user_id)
            if u is None:
                return User.guest()
            else:
                return u
    else:
        return User.guest()


def error(request, code=404):
    """
    根据 code 返回错误响应
    """
    # 表驱动法替代if语句
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def formatted_header(headers=None, code=200):
    # 封装header的处理部分
    if headers is None:
        headers = {}
    header = 'HTTP/1.1 {} OK TEST\r\n'.format(code)
    if headers.get('Content-Type') is None:
        headers['Content-Type'] = 'text/html'
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def redirect(url, session_id=None):
    # session_id在用户登录验证通过后的重定向会使用到
    h = {'Location': url}
    if isinstance(session_id, str):
        h.update({'Set-Cookie': 'session_id={}; path=/'.format(session_id)})
    response = formatted_header(h, 302) + '\r\n'
    return response.encode()


def html_response(filename, **kwargs):
    body = TestTemplate.render(filename, **kwargs)
    r = formatted_header() + '\r\n' + body
    # log('html_response_r', r)
    return r.encode()


def json_response(data):
    body = json.dumps(data, indent=2, ensure_ascii=False)
    headers = {'Content-Type': 'application/json'}
    r = formatted_header(headers=headers) + '\r\n' + body
    return r.encode()


def login_required(route_function):
    def f(request):
        # log('login_required')
        u = current_user(request)
        if u.is_guest():
            # log('游客用户')
            return redirect('/user/login/view')
        else:
            # log('登录用户', route_function)
            return route_function(request)
    return f