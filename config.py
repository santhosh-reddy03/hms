import os


class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or b'\x96)\x89\xf9\xd5\xf9bkv\xffF\xafc\xfa\x08\xac\x9b\xba\xe07@\x97\xf4'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')
