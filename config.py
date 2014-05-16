import os

DEBUG = False

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'muaychampionpurpsh1rt'
 
ADMINS = frozenset(['ba@luckypupil.com'])
SECRET_KEY = '0penw@ter'

if os.environ.get('DATABSE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blake:bloopers@localhost/foodo'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#APPLICATION_URL = '0.0.0.0'


