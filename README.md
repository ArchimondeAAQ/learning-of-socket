一个简单的基于TCP的套接字，用于理解HTTP协议的原理。参照了[Python 中的 Socket 编程](https://keelii.gitbooks.io/socket-programming-in-python-cn/content/)及一些开源项目。

采用了MVC结构模式，其中routes文件夹为C（控制器)，包括了路由分发和对数据进行基本的CRUD操作；templates文件夹为V(视图）并选择了jinja2模板，包括了所有的html文件；models文件夹为M（模型）部分，对数据和数据的操作方法进行了封装，并且使用了自制的mysql ORM。另外static文件夹中保存了一些静态资源文件。

client.py是对客户端的模仿，request.py处理客户端请求并对它进行处理和保存，server.py为服务器的启动文件。
