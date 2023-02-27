class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./movies.db'
    PWD_HASH_SALT = b'SEEdd&*#GDJSBJKSFH#IY&fgiudgsg37$&*Fg'
    PWD_HASH_ITERATIONS = 100_000
    secret = 'S443@@#dd!wwqsASSDds'
    algo = 'HS256'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

