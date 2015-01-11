class User(object):
    users = {}
    users_by_name = {}

    @classmethod
    def get(cls, userid):
        userid = unicode(userid)
        return cls.users.get(userid, None)

    @classmethod
    def get_id_by_name(cls, username):
        return cls.users_by_name.get(username, None)

    def __init__(self, userid, username):
        self._id = unicode(userid)
        self.username = username
        User.users[self._id] = self
        User.users_by_name[self.username] = self._id

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