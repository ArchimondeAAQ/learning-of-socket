import pymysql
import config
import secret


class SQLModel(object):
    connection = None

    @classmethod
    def init_db(cls):
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password=secret.mysql_password,
            db=config.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def __init__(self, form):
        # 因为 id 是数据库给的，所以最开始初始化的时候必须是 None
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        return '`{}`'.format(cls.__name__.lower())

    @classmethod
    def new(cls, form):
        # cls(form) 相当于 User(form)
        m = cls(form)
        id = cls.insert(m.__dict__)
        m.id = id
        return m

    @classmethod
    def insert(cls, form):

        form.pop('id')

        sql_keys = ', '.join(['`{}`'.format(k) for k in form.keys()])
        sql_values = ', '.join(['%s'] * len(form))
        sql_insert = 'INSERT INTO {} ({}) VALUES ({})'.format(
            cls.table_name(),
            sql_keys,
            sql_values,
        )

        values = tuple(form.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            _id = cursor.lastrowid
        cls.connection.commit()

        return _id

    @classmethod
    def delete(cls, id):
        sql_delete = 'DELETE FROM {} WHERE `id`=%s'.format(cls.table_name())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_delete, (id,))
        cls.connection.commit()

    @classmethod
    def update(cls, id, **kwargs):

        sql_set = ', '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_update = 'UPDATE {} SET {} WHERE `id`=%s'.format(
            cls.table_name(),
            sql_set,
        )

        values = list(kwargs.values())
        values.append(id)
        values = tuple(values)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_update, values)
        cls.connection.commit()

    @classmethod
    def all(cls, **kwargs):
        sql_select = 'SELECT * FROM \n\t{}'.format(cls.table_name())

        if len(kwargs) > 0:
            sql_where = ' AND '.join(
                ['`{}`=%s'.format(k) for k in kwargs.keys()]
            )
            sql_where = '\nWHERE\n\t{}'.format(sql_where)
            sql_select = '{}{}'.format(sql_select, sql_where)

        values = tuple(kwargs.values())

        ms = []
        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select, values)
            result = cursor.fetchall()
            for row in result:
                m = cls(row)
                ms.append(m)
            return ms

    @classmethod
    def one(cls, **kwargs):

        sql_where = 'WHERE {}=%s'.format([k for k in kwargs.keys()][0])
        sql_select = 'SELECT * FROM {} {} '.format(
            cls.table_name(),
            sql_where
        )

        values = tuple(kwargs.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select, values)
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                return cls(result)

    def __repr__(self):
        name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(name, s)

    def json(self):
        return self.__dict__
