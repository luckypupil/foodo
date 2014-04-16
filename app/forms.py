from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, FileField
from wtforms.validators import Required

class HomeSearch(Form):
    name = TextField('name',default = 'restuarant name')
    hood = TextField('hood', default = 'neighborhood')