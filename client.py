import socket
import ssl
from utils import log


def parsed_url(url):
    # 判断协议并去掉
    if url[:5] == 'https':
        protocol = 'https'
        url = url[8:]
        port = 443
    elif url[:4] == 'http':
        protocol = 'http'
        url = url[7:]
        port = 80
    else:
        protocol = 'http'
        port = 80

    url_cut_path = url.split('/', 1)
    if (len(url_cut_path) == 1) or (len(url_cut_path[1]) == 0):
        path = '/'
    else:
        path = '/' + url_cut_path[1]
    url = url_cut_path[0]

    url_cut_port = url.split(':', 1)
    if len(url_cut_port) == 2:
        port = url_cut_port[1]
    host = url_cut_port[0]

    return protocol, host, port, path


# 函数socket_by_protocol判断http https，封装对应的socket
def socket_by_protocol(protocol):
    s = socket.socket()
    if protocol == 'https':
        s = ssl.wrap_socket(s)
    return s


def response_by_socket(s: socket.socket):
    response = b''
    while True:
        r = s.recv(1024)
        response += r
        if len(r) < 1024:
            return response.decode()


def parsed_response(r):
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = int(h[0].split()[1])

    # 将除响应行的headers部分转为字典形式

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ', 1)
        headers[k] = v

    return status_code, headers, body


def get(url):
    protocol, host, port, path = parsed_url(url)
    # 使用socket实例，其中socket_by_protocol函数封装了http/https的判断
    s = socket_by_protocol(protocol)
    s.connect((host, port))                 # 建立连接
    request = 'GET {0} HTTP/1.1\r\nHost:{1}\r\n\r\n'.format(path, host)          # 新建请求
    s.send(request.encode())                # 发送请求
    response = response_by_socket(s)        # 接收数据，其中response_by_socket封装了接收数据的流程
    status_code, headers, body = parsed_response(response)

    if status_code == 301:
        url = headers['Location']
        return get(url)
    else:
        return response, status_code


def main():
    url = 'http://movie.douban.com'
    r = get(url)
    print(r)


if __name__ == '__main__':
    main()