from submission_site.sub_site.handle_login import good_password, good_username


class TestValidPassword(object):

    @staticmethod
    def test_letters_only():
        password = "JustLetters"
        assert all(good_password.match(char) for char in password)

    @staticmethod
    def test_numbers_only():
        password = "134987"
        assert all(good_password.match(char) for char in password)

    @staticmethod
    def test_symbols_only():
        password = "!@#$%^&*-_=+"
        assert all(good_password.match(char) for char in password)

    @staticmethod
    def test_mixed():
        password = "asdEIF23##@"
        assert all(good_password.match(char) for char in password)

    @staticmethod
    def test_no_spaces():
        password = "asdf "
        assert not all(good_password.match(char) for char in password)

    @staticmethod
    def test_bad_symbols():
        password = "[]asdf"
        assert not all(good_password.match(char) for char in password)


class TestValidUsername(object):

    @staticmethod
    def test_letters_only():
        username = "JustLetters"
        assert all(good_username.match(char) for char in username)

    @staticmethod
    def test_numbers_only():
        username = "134987"
        assert all(good_username.match(char) for char in username)

    @staticmethod
    def test_bad_symbols():
        username = "!@#$%^&*=+[]{}\|()"
        assert not any(good_username.match(char) for char in username)

    @staticmethod
    def test_mixed():
        username = "asdEIF23_-"
        assert all(good_username.match(char) for char in username)

    @staticmethod
    def test_no_spaces():
        username = "asdf "
        assert not all(good_username.match(char) for char in username)


class TestUsernameCollisons(object):

    @classmethod
    def setup_class(cls):
        from submission_site.sub_site.views import app
        app.config['DATABASE'] = 'test_db.db'
        app.config['SCHEMA'] = 'test_schema.sql'
        cls.app = app