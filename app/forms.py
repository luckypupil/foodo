from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, FileField, StringField, IntegerField, validators
from wtforms.validators import Required, InputRequired, Length, Email

class RestSearch(Form):
    search = TextField('restuarant',validators = [Required(message=(u'.'))])

class SubscribeForm(Form):
    email = StringField('email',validators = [InputRequired(),Email(),Length(min=2)])
    zipcd = IntegerField('zipcd',validators = [Required()])
    first_name = TextField('first')
    last_name = TextField('last')