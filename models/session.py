import time
import uuid

from models.__init__ import SQLModel
from utils import log


# Session 是用来保存 session 的 model
class Session(SQLModel):

    sql_create = '''
    CREATE TABLE `session` (
        `id`            INT NOT NULL AUTO_INCREMENT,
        `session_id`    CHAR(36) NOT NULL,
        `user_id`       INT NOT NULL,
        `expired_time`  INT NOT NULL,
        PRIMARY KEY (`id`),
        INDEX `session_id_index` (`session_id`)
    );
    '''

    def __init__(self, form):
        super().__init__(form)
        self.session_id = form.get('session_id', '')
        self.user_id = form.get('user_id', -1)
        self.expired_time = form.get('expired_time', time.time() + 3600)

    def expired(self):
        now = time.time()
        result = self.expired_time < now
        # log('expired', result, self.expired_time, now)
        return result

    @classmethod
    def add(cls, user_id):
        # 把用户名存入 cookie 中
        # headers['Set-Cookie'] = 'user={}'.format(u.username)
        session_id = str(uuid.uuid4())
        # log('session_id~', session_id, type(session_id), len(session_id))
        form = dict(
            session_id=session_id,
            user_id=user_id,
        )
        s = Session.new(form)
        return session_id
