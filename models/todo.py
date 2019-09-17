from time import time

from models.__init__ import SQLModel


class Todo(SQLModel):
    sql_create = '''
        CREATE TABLE `todo` (
            `id`        INT NOT NULL AUTO_INCREMENT,
            `title`     VARCHAR(255) NOT NULL,
            `user_id`   INT NOT NULL,
            PRIMARY KEY (`id`)
        );
        '''

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)

