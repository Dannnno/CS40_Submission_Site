class User(object):
    users = {}

    @classmethod
    def get(cls, userid):
        userid = unicode(userid)
        return cls.users.get(userid, None)

    def __init__(self, userid, username):
        self._id = unicode(userid)
        self.username = username
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