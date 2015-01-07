from flask.ext.login import UserMixin


class User(UserMixin):
    users = {}

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        User.users[self.get_id()] = self