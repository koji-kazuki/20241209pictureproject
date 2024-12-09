import os

basedir = os.path.dirname(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) or 'sqlite:///' + os.path.join(basedir,'blog.sqlite')

SECRET_KEY = os.urandom(10)

USERNAME = 'admin'
PASSWORD = 'abcd1234'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'kazu06125420@gmail.com'
MAIL_PASSWORD = 'ylqm fdlu rhha wplm'
MAIL_DEFAULT_SENDER = 'kazu06125420@gmail.com'

