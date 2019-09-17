import time

from models.todo_ajax import TodoAjax
from routes import (
    current_user,
    html_response,
    login_required,
    json_response)


@login_required
def index(request):
    return html_response('todo_ajax_index.html')


@login_required
def all(request):
    todos = [t.__dict__ for t in TodoAjax.all()]
    return json_response(todos)


@login_required
def add(request):
    # 测试ajax
    time.sleep(5)
    u = current_user(request)
    form = request.json()
    t = TodoAjax.add(form, u.id)
    message = dict(message='成功添加 {}'.format(t.title))
    return json_response(message)


def route_dict():
    d = {
        '/todo/ajax/add': add,
        '/todo/ajax/index': index,
        '/todo/ajax/all': all,
    }
    return d
