var e = function (selector) {
    return document.querySelector(selector)
}


/*
1. 给 add button 绑定事件
2. 在事件处理函数中，获取 input 的值
3. 用获取的值，组装一个 todo-cell HTML 字符串
4. 插入 todo-list 中
*/

var todoTemplate = function (todo) {
    var t = `
    <div class="todo-cell">
        <span>${todo}</span>
    </div>
    `
    return t
}

var insertTodo = function (todoCell) {
    // todoCell是HTML字符串
    var form = document.querySelector('#id-todo-list')
    form.insertAdjacentHTML('beforeEnd', todoCell)
}

var loadTodos = function () {
    ajax('POST', '/todo/ajax/all', {}, function (json) {
        log('get_ajax_response')
        log('response data json', json)
        for (var i = 0; i < json.length; i++) {
            log('json for', json[i], json)
            var todo = json[i].title
            var todoCell = todoTemplate(todo)
            log(todoCell)
            insertTodo(todoCell)
        }
    })
}

var bindEvents = function () {
    var b = e('#id-button-add')
    b.addEventListener('click', function () {
    log('click')
    var input = e('#id-input-todo')
    var todo_title = input.value
    var todoCell = todoTemplate(todo_title)

    var data = {
        title: todo_title
    }

    ajax('POST', '/todo/ajax/add', data, function (json) {
        log('拿到ajax响应')
    })

    // 先将todoCell插入页面中，添加到数据库的后端操作可通过ajax异步处理
    insertTodo(todoCell)

    })
}

var main = function () {
    loadTodos()
    bindEvents()
}

main()