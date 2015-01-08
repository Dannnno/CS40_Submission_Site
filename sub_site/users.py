from sub_site.handle_database import main as db_main


class User(object):
    users = {}

    @classmethod
    def get(cls, userid):
        userid = unicode(userid)
        return cls.users.get(userid, None)

    def __init__(self, app, username=None, userid=None):
        query_db = db_main(app)
        if username is not None:
            self._id = query_db("SELECT userid FROM users WHERE username=?",
                                [username])
        else:
            self._id = userid
        self._id = unicode(self._id)
        User.users[self._id] = self

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self._id