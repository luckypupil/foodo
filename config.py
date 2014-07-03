import os

DEBUG = False

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'muaychampionpurpsh1rt'
 
ADMINS = frozenset(['ba@luckypupil.com'])
SECRET_KEY = '0penw@ter'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blakeadams:@localhost/tiskdb'
    DEBUG = True
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#APPLICATION_URL = '0.0.0.0'


