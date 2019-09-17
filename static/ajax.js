var log = console.log.bind(console)


var ajax = function(method, path, data, responseCallback) {
    log('ajax request', method, path, data, responseCallback)
    var r = new XMLHttpRequest()
    // 设置向后端发送的请求方法和地址
    r.open(method, path, true)
    // 设置发送的数据的格式
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数；每当 readyState 改变时，就会触发 onreadystatechange 事件
    r.onreadystatechange = function() {
         // 当r.readyState等于4时，将得到的响应序列化并传给回调函数
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            log('ajax response', r.response)
            var json = JSON.parse(r.response)
            log('ajax response after json.parse', json)

            responseCallback(json)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}
