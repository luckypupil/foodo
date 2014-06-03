from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, FileField
from wtforms.validators import Required

class RestSearch(Form):
    name = TextField('name',validators = [Required()],default = 'restuarant name')